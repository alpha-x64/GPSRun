from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30, verbose_name="Nombre de Usuario")
    email = models.CharField(max_length=30, verbose_name="Correo Electrónico")
    password = models.CharField(max_length=30, verbose_name="Contraseña")
    score = models.IntegerField(default=0, verbose_name="Puntuación")
