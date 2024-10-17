from rest_framework import serializers
from .models import Vetbook, Vaccination, Treatment, ClinicalExamination, ClinicVisit, ExtendedTreatment


class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = ['name', 'batch_number', 'expiration_date', 'administration_date', 'validity_date']


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['treatment_type', 'medication_name', 'treatment_date']


class ClinicalExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalExamination
        fields = ['examination_date', 'results', 'clinic']


class ClinicVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicVisit
        fields = ['clinic_name', 'visit_date', 'complaints', 'doctor_conclusion', 'files']


class ExtendedTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendedTreatment
        fields = ['medication_name', 'dosage', 'frequency', 'start_date', 'end_date', 'missed_doses', 'calendar']


class VetbookSerializer(serializers.ModelSerializer):
    vaccinations = VaccinationSerializer(many=True, read_only=True)
    treatments = TreatmentSerializer(many=True, read_only=True)
    examinations = ClinicalExaminationSerializer(many=True, read_only=True)
    clinic_visits = ClinicVisitSerializer(many=True, read_only=True)
    extended_treatments = ExtendedTreatmentSerializer(many=True, read_only=True)

    class Meta:
        model = Vetbook
        fields = [
            'animal_name', 'animal_type', 'weight', 'breed', 'is_homeless', 'gender',
            'photos', 'videos', 'chip_number', 'chip_install_date', 'chip_install_location',
            'clinic', 'registration_number', 'vaccinations', 'treatments', 'examinations',
            'clinic_visits', 'extended_treatments'
        ]
        extra_kwargs = {'owner': {'read_only': True}}

    def create(self, validated_data):
        # Извлекаем данные для связанных объектов, если они предоставлены
        vaccinations_data = validated_data.pop('vaccinations', [])
        treatments_data = validated_data.pop('treatments', [])
        examinations_data = validated_data.pop('examinations', [])
        clinic_visits_data = validated_data.pop('clinic_visits', [])
        extended_treatments_data = validated_data.pop('extended_treatments', [])

        # Создаем основную запись Vetbook
        vetbook = Vetbook.objects.create(**validated_data)

        # Создаем связанные объекты
        for vaccination_data in vaccinations_data:
            Vaccination.objects.create(vetbook=vetbook, **vaccination_data)

        for treatment_data in treatments_data:
            Treatment.objects.create(vetbook=vetbook, **treatment_data)

        for examination_data in examinations_data:
            ClinicalExamination.objects.create(vetbook=vetbook, **examination_data)

        for visit_data in clinic_visits_data:
            ClinicVisit.objects.create(vetbook=vetbook, **visit_data)

        for treatment_data in extended_treatments_data:
            ExtendedTreatment.objects.create(vetbook=vetbook, **treatment_data)

        return vetbook





