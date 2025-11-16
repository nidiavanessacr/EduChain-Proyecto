from django.db import models
from django.contrib.auth.models import AbstractUser


# -----------------------------
# USUARIO CON ROLES
# -----------------------------
class User(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante'),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='estudiante')

    def save(self, *args, **kwargs):
        # Asegurar que los superusers siempre sean admin
        if self.is_superuser:
            self.role = "admin"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"


# -----------------------------
# WALLET
# -----------------------------
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    private_key = models.CharField(max_length=200)

    def __str__(self):
        return f"Wallet de {self.user.username}"


# -----------------------------
# ALUMNO EXTRA MODEL
# -----------------------------
class Alumno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    matricula = models.CharField(max_length=50)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.matricula})"


# -----------------------------
# TRANSACCIONES EN BLOCKCHAIN
# -----------------------------
class Transaccion(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    amount = models.FloatField()

    # TXID puede ser NULL porque no existe al crear la transacción
    txid = models.CharField(max_length=200, null=True, blank=True)

    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.amount} ALGOs)"


# -----------------------------
# ACTIVIDADES CREADAS POR DOCENTE
# -----------------------------
class Actividad(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_entrega = models.DateField(null=True, blank=True)

    docente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="actividades_creadas",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titulo


# -----------------------------
# ACTIVIDADES ASIGNADAS A ESTUDIANTES
# -----------------------------
class ActividadAsignada(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)

    estudiante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    entregada = models.BooleanField(default=False)
    finalizada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.actividad.titulo} → {self.estudiante.username if self.estudiante else 'Sin asignar'}"
