from django.contrib import admin
from borsa.models import AcademicYear, IseeRange

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    ordering = ['academicYear']
    search_fields = ('academicYear', '')

@admin.register(IseeRange)
class IseeRangeAdmin(admin.ModelAdmin):
    readonly_fields = ('nrRange',)  # Rendi il campo non modificabile
    fields = ('iseeMin', 'iseeMax', 'academicYear', 'nrRange')  # Mostra i campi, incluso il readonly

    ordering = ['nrRange']
    search_fields = ('academicYear__academicYear', 'nrRange')
    list_display = ('nrRange', 'iseeMin', 'iseeMax', 'academicYear')

