from django.db import models

# Create your models here.

class AnnoAccademico(models.Model):
    anno = models.IntegerField(verbose_name="Anno accademico")