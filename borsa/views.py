from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny

from .models import AcademicYear, IseeRange, Scholarship,Request
from .serializers import AcademicYearSerializer, IseeRangeSerializer, ScholarshipSerializer, RequestSerializer
from rest_framework.permissions import IsAuthenticated

class AcademicYearViewSet(ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['get'], url_path='get-academic-years')
    def get_academic_years(self, request):
        # Recupera tutti gli anni accademici
        years = AcademicYear.objects.values_list('academicYear', flat=True)

        # Restituisci una risposta con i dati serializzati
        return Response(list(years), status=200)

class IseeRangeViewSet(ModelViewSet):
    queryset = IseeRange.objects.all()
    serializer_class = IseeRangeSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['get'], url_path='get-isee-range')
    def get_isee_range(self, request):
        # Recupera l'academicYear dai parametri della query string
        academic_year = request.query_params.get('academicYear', None)

        if academic_year is None:
            return Response(
                {"error": "Parametro 'academicYear' mancante."},
                status=400
            )

        # Filtra i record per l'anno accademico specificato
        filtered_ranges = self.queryset.filter(academicYear__academicYear=academic_year)

        # Serializza i risultati
        serializer = self.get_serializer(filtered_ranges, many=True)
        return Response(serializer.data, status=200)


    @action(detail=False, methods=['get'], url_path='get-all-isee-ranges')
    def get_isee_range(self, request):
        ranges = self.queryset.all()

        # Serializza i risultati
        serializer = self.get_serializer(ranges, many=True)
        return Response(serializer.data, status=200)

class ScholarshipViewSet(ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = (AllowAny,)

class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

