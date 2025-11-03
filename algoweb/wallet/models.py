from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=58)
    private_key = models.TextField()

    def __str__(self):
        return f"Wallet de {self.user.username}"


class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    matricula = models.CharField(max_length=50)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    def __str__(self):
        return f"Alumno: {self.nombre} ({self.wallet.user.username})"

