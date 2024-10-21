from rest_framework import viewsets
from django.db import transaction
from .models import Vetbook, Vaccination, Treatment, ClinicalExamination, ClinicVisit, ExtendedTreatment
from .serializers import (VetbookSerializer, VaccinationSerializer, TreatmentSerializer,
                          ClinicalExaminationSerializer, ClinicVisitSerializer, ExtendedTreatmentSerializer)
from rest_framework.permissions import IsAuthenticated


class VetbookViewSet(viewsets.ModelViewSet):
    queryset = Vetbook.objects.all()
    serializer_class = VetbookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        with transaction.atomic():
            vetbook = serializer.save(owner=self.request.user.profile)

            # Дополнительная логика
            self._save_related(vetbook)

    def _save_related(self, vetbook):
        vaccinations_data = self.request.data.get('vaccinations', [])
        treatments_data = self.request.data.get('treatments', [])
        examinations_data = self.request.data.get('examinations', [])
        clinic_visits_data = self.request.data.get('clinic_visits', [])
        extended_treatments_data = self.request.data.get('extended_treatments', [])

        for vaccination in vaccinations_data:
            Vaccination.objects.create(vetbook=vetbook, **vaccination)
        for treatment in treatments_data:
            Treatment.objects.create(vetbook=vetbook, **treatment)
        for examination in examinations_data:
            ClinicalExamination.objects.create(vetbook=vetbook, **examination)
        for visit in clinic_visits_data:
            ClinicVisit.objects.create(vetbook=vetbook, **visit)
        for ext_treatment in extended_treatments_data:
            ExtendedTreatment.objects.create(vetbook=vetbook, **ext_treatment)



