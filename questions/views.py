from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Question,QuestionFile

"""Function for saving a question"""

@csrf_exempt  # Для упрощения, но лучше использовать токены CSRF
def add_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        pet_art = request.POST.get('petArt')
        pet_weight = request.POST.get('petWeight')
        pet_gender = request.POST.get('petGender')
        is_homeless = request.POST.get('isHomeless') == 'true'

        # Создаем объект Question
        question = Question.objects.create(
            question=question_text,
            pet_art=pet_art,
            pet_weight=pet_weight,
            pet_gender=pet_gender,
            is_homeless=is_homeless,
        )

        # Получаем все загруженные файлы
        files = request.FILES.getlist('files')

        # Сохраняем загруженные файлы
        for file in files:
            QuestionFile.objects.create(question=question, file=file)

        return JsonResponse({'message': 'Вопрос успешно сохранен!'}, status=201)

    return JsonResponse({'error': 'Неверный запрос'}, status=400)



