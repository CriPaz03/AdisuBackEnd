from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny

from .models import AcademicYear, IseeRange, Request
from .serializers import AcademicYearSerializer, IseeRangeSerializer, RequestSerializer
from rest_framework.permissions import IsAuthenticated

class AcademicYearViewSet(ModelViewSet):
    queryset = AcademicYear.objects.filter(isee_range__isnull = False).distinct()
    serializer_class = AcademicYearSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['get'], url_path='get-academic-years')
    def get_academic_years(self, request):
        # Recupera tutti gli anni accademici
        years = AcademicYear.objects.filter(isee_range__isnull=False).distinct()

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

    @action(detail=False, methods=['get'], url_path='get-isee-range-by-id')
    def get_isee_range_by_id(self, request):
        # Recupera l'academicYear dai parametri della query string
        nr = request.query_params.get('nr', None)

        if nr is None:
            return Response(
                {"error": "Parametro 'academicYear' mancante."},
                status=400
            )

        # Filtra i record per l'anno accademico specificato
        filtered_ranges = self.queryset.filter(nrRange=nr)

        # Serializza i risultati
        serializer = self.get_serializer(filtered_ranges, many=True)
        return Response(serializer.data, status=200)

class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = ([JWTAuthentication])

    @action(detail=False, methods=['get'], url_path='get-request-by-user')
    def get_request_by_user(self, request):
        nr_utente = request.query_params.get('nrUtente')  # Ottieni il parametro dall'URL

        if not nr_utente:
            return Response({"error": "nrUtente is required"}, status=400)

        # Filtra le richieste in base al numero utente
        user_requests = Request.objects.filter(studentName=nr_utente)
        # Serializza i dati
        serializer = RequestSerializer(user_requests, many=True)

        return Response(serializer.data, status=200)

    @action(detail=False, methods=['post'], url_path='post-request-by-user')
    def post_request_by_user(self, request):
        serializer = RequestSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

