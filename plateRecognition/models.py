from django.db import models

# Create your models here.

class Plate(models.Model):
    plate = models.CharField(name = 'Placa', verbose_name= 'Placas', max_length= 15)