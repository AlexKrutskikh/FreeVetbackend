from django.db import models
from users.models import Profile  # Импортируем модель Profile


class Vetbook(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)                                # Владелец ветеринарной книжки (связь с Profile)
    animal_name = models.CharField(max_length=255)                                              # Имя животного
    animal_type = models.CharField(max_length=255)                                              # Тип животного (например, собака, кошка)
    weight = models.FloatField()                                                                # Вес животного
    breed = models.CharField(max_length=255, blank=True, null=True)                             # Порода животного
    is_homeless = models.BooleanField(default=False)                                            # Флаг домашнего или бездомного животного
    gender = models.CharField(max_length=10, choices=[('Male', 'Самец'), ('Female', 'Самка')])  # Пол животного
    photos = models.ImageField(upload_to='vetbook_photos/', blank=True, null=True)              # Фотографии животного
    videos = models.FileField(upload_to='vetbook_videos/', blank=True, null=True)               # Видео животного
    created_at = models.DateTimeField(auto_now_add=True)                                        # Дата создания записи

    chip_number = models.CharField(max_length=50, blank=True, null=True)                        # Номер чипа
    chip_install_date = models.DateField(blank=True, null=True)                                 # Дата установки чипа
    chip_install_location = models.CharField(max_length=255, blank=True, null=True)             # Место установки чипа
    clinic = models.CharField(max_length=255, blank=True, null=True)                            # Клиника установки чипа
    registration_number = models.CharField(max_length=255, blank=True, null=True)               # Регистрационный номер

    def __str__(self):
        return self.animal_name


class Vaccination(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name='vaccinations')
    name = models.CharField(max_length=255)
    batch_number = models.CharField(max_length=50, blank=True, null=True)                       # Серия
    expiration_date = models.DateField(blank=True, null=True)                                   # Срок годности
    administration_date = models.DateField(blank=True, null=True)                               # Дата вакцинации
    validity_date = models.DateField(blank=True, null=True)                                     # Срок окончания действия


class Treatment(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name='treatments')
    treatment_type = models.CharField(max_length=255, choices=[('deworming', 'Дегельминтизация'),
                                                               ('ectoparasites', 'Обработка от эктопаразитов')])
    medication_name = models.CharField(max_length=255)
    treatment_date = models.DateField()


class ClinicalExamination(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name='examinations')
    examination_date = models.DateField()
    results = models.TextField(blank=True, null=True)
    clinic = models.CharField(max_length=255, blank=True, null=True)                               # Клиника

    def __str__(self):
        return f"Examination on {self.examination_date}"


class ClinicVisit(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name='clinic_visits')
    clinic_name = models.CharField(max_length=255)
    visit_date = models.DateField()
    complaints = models.TextField(blank=True, null=True)
    doctor_conclusion = models.TextField(blank=True, null=True)
    files = models.FileField(upload_to='clinic_visits_files/', blank=True, null=True)

    def __str__(self):
        return f"Visit on {self.visit_date} at {self.clinic_name}"


class ExtendedTreatment(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name='extended_treatments')
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    missed_doses = models.CharField(max_length=100, blank=True, null=True)
    calendar = models.TextField(blank=True, null=True)