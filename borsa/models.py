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
    academicYear = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name="Anno Accademico", primary_key=False)

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


class Scholarship(models.Model):
    scholarshipName = models.CharField(max_length=50, verbose_name="Nome Borsa di Studio")
    nrRange = models.ForeignKey(IseeRange, on_delete=models.CASCADE, verbose_name="Fascia ISEE", primary_key=False)

    class Meta:
        unique_together = (("nrRange", "scholarshipName"),)

    def __str__(self):
        return f"{self.scholarshipName}"

class Request(models.Model):
    class StudentType(models.TextChoices):
        onSite = "onSite", "In Sede"
        offSite = "offSite", "Fuorisede"
        commuter = "commuter", "Pendolare"

    class YearType(models.TextChoices):
        firstYear = "firstYear", "Primo anno"
        secondYear = "secondYear", "Secondo anno"
        thirdYear = "thirdYear", "Terzo anno"
        fourthYer = "fourthYer", "Quarto anno laurea ciclo unico"
        fifthYear = "fifthYear", "Quinto anno laurea ciclo unico"
        firstYearOffCourse = "firstYearOffCourse", "Primo Anno fuori corso"
        secondYearOffCourse = "secondYearOffCourse", "Secondo Anno fuori corso"

    physicalCondition = models.TextField(verbose_name="Condizioni fisiche")
    academicYear = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name="Anno Accademico", primary_key=False)
    studentNumber = models.ForeignKey(User, on_delete=models.CASCADE)
    nrRange = models.ForeignKey(IseeRange, on_delete=models.CASCADE, verbose_name="Fascia ISEE", primary_key=False)

    class Meta:
        unique_together = (("nrRange", "academicYear", "studentNumber"),)
