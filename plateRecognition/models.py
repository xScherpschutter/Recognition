from django.db import models
from django.core.validators import MinLengthValidator


class plate(models.Model):
    plateID = models.AutoField(primary_key=True)
    code = models.CharField(max_length=7, validators=[MinLengthValidator(7)])
