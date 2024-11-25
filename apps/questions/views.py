import json

from django.contrib.auth.models import Permission
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question, QuestionFile, QuestionReview
from .serializers import QuestionSerializer

"""Function for saving a  question"""


@csrf_exempt  # Для упрощения, но лучше использовать токены CSRF
def add_question(request):
    if request.method == 'POST':
        pet_art = request.POST.get('petArt')
        pet_weight = request.POST.get('petWeight')
        pet_gender = request.POST.get('petGender')
        is_homeless = request.POST.get('isHomeless') == 'true'
        user_id = request.POST.get('userId')

        # Создаем объект Question
        question = Question.objects.create(
            pet_art=pet_art,
            pet_weight=pet_weight,
            pet_gender=pet_gender,
            is_homeless=is_homeless,
            user_id=user_id
        )

        # Получаем все загруженные файлы
        files = request.FILES.getlist('files')

        # Сохраняем загруженные файлы
        for file in files:
            QuestionFile.objects.create(question=question, file=file)

        return JsonResponse({'message': 'Вопрос успешно сохранен!'}, status=201)

    return JsonResponse({'error': 'Неверный запрос'}, status=400)


"""Function for updating the last question for a specific user_id"""


@csrf_exempt
def update_question(request):
    if request.method == 'POST':
        try:
            # Парсим JSON из тела запроса
            data = json.loads(request.body)
            user_id = data.get('user_id')
            questions_text = data.get('questions')

            # Проверка на наличие необходимых полей
            if user_id is None or questions_text is None:
                return JsonResponse({"error": "Необходимо указать user_id и questions"}, status=400)

            # Находим последнюю запись по user_id
            question = Question.objects.filter(user_id=user_id).last()
            if question is None:
                return JsonResponse({"error": "Запись с таким user_id не найдена"}, status=404)

            # Обновляем поле question
            question.question = questions_text
            question.save()

            return JsonResponse({"message": "Запись обновлена успешно"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Ошибка в формате JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({'error': 'Неверный запрос'}, status=400)


class AllQuestionsByUser(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id is None:
            questions = Question.objects.all()
        else:
            questions = Question.objects.filter(user_id=user_id).all()

        serializer = QuestionSerializer(questions, many=True, context={'request': request})

        return JsonResponse(serializer.data, safe=False, status=200)


"""Api for answering questions on ID"""
class BookQuestionView(APIView):
    def post(self, request, pk):
        question = Question.objects.get(pk=pk)
        if question is None:
            return Response({"error": "no question with given id"}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({"error": "user_id required"}, status=status.HTTP_404_NOT_FOUND)

        question.vet_user_id = user_id
        question.save()

        return JsonResponse({'message': 'question has booked for vet'}, status=status.HTTP_200_OK)


class QuestionView(APIView):
    def get(self, request, pk):
        question = Question.objects.get(pk=pk)
        if question is None:
            return Response({"error": "no question with given id"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        text = request.data.get('text')
        score = request.data.get('score')

        question = Question.objects.get(pk=pk)
        if question is None:
            return Response({"error": "no question with given id"}, status=status.HTTP_404_NOT_FOUND)

        question.status = Question.Status.COMPLETED
        question.save()

        QuestionReview.objects.create(question=question, text=text, score=score)

        return JsonResponse({'message': 'Question completed successfully'}, status=201)

