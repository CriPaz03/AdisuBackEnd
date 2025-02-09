from django.db import models
from django.contrib.auth.models import User

class AcademicYear(models.Model):
    academicYear = models.IntegerField(primary_key=True, verbose_name="Anno Accademico")

    def __str__(self):
        return str(self.academicYear)

class IseeRange(models.Model):
    nrRange = models.DecimalField(primary_key=True, max_digits=6, decimal_places=0, verbose_name="Fascia ISEE")
    iseeMin = models.DecimalField(max_digits=6, decimal_places=0, verbose_name="Minimo ISEE")
    iseeMax = models.DecimalField(max_digits=6, decimal_places=0, verbose_name="Massimo ISEE")
    academicYear = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name="Anno Accademico", primary_key=False, related_name="isee_range", blank=True, null=True )

    class Meta:
        unique_together = (("academicYear", "nrRange"),)

    def __str__(self):
        return f"{self.nrRange} - {self.iseeMin} - {self.iseeMax}"

    def save(self, *args, **kwargs):
        # Se l'istanza è nuova, assegna un valore progressivo a nrRange
        if not self.pk:  # Solo per nuove istanze
            max_range = (
                    IseeRange.objects.filter(academicYear=self.academicYear)
                    .aggregate(max_nr=models.Max('nrRange'))['max_nr'] or 0
            )
            self.nrRange = max_range + 1

        super().save(*args, **kwargs)


class Request(models.Model):
    physicalCondition = models.BooleanField(verbose_name="Condizioni fisiche")
    studentType = models.TextField(verbose_name="Tipo studente")
    yearType = models.TextField(verbose_name="Anno di studio")
    nrStudent = models.TextField(verbose_name="Matricola")
    studentName = models.TextField(verbose_name="Studente")
    academicYear = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name="Anno Accademico", primary_key=False)
    nrRange = models.ForeignKey(IseeRange, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("academicYear", "studentName"),)
