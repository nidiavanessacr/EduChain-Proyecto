from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from algosdk import account
from algosdk.v2client import algod


# ==========================================================
# USUARIO CON ROLES
# ==========================================================
class User(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante'),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='estudiante')

    # ⭐ Nuevos campos:
    rfc = models.CharField(max_length=13, blank=True, null=True)
    numero_control = models.CharField(max_length=10, blank=True, null=True)

    # Email PERSONAL (no toca el email real del sistema)
    email_user = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = "admin"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"



# ==========================================================
# WALLET
# ==========================================================
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    private_key = models.CharField(max_length=200)
    saldo = models.FloatField(default=0.0)   # Se actualiza automáticamente

    def __str__(self):
        return f"Wallet de {self.user.username}"

    # ======================================================
    # CONSULTAR SALDO REAL EN ALGOD CLIENT
    # ======================================================
    @property
    def saldo_algorand(self):
        """Consulta en vivo en la blockchain."""
        client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")
        try:
            info = client.account_info(self.address)
            return info.get("amount", 0) / 1_000_000
        except:
            return 0

    # ======================================================
    # ACTUALIZAR SALDO LOCAL
    # ======================================================
    def actualizar_saldo(self):
        """Actualiza el saldo guardado en la base de datos."""
        self.saldo = self.saldo_algorand
        self.save()


# ==========================================================
# AUTO-CREAR WALLET AL CREAR USUARIO
# ==========================================================
@receiver(post_save, sender=User)
def crear_wallet_usuario(sender, instance, created, **kwargs):
    """
    Crea automáticamente una wallet Algorand real cuando
    se registra un nuevo usuario.
    """
    if created:
        private_key, address = account.generate_account()
        Wallet.objects.create(
            user=instance,
            address=address,
            private_key=private_key,
            saldo=0.0
        )


# ==========================================================
# ALUMNO (YA NO LO USAMOS, PERO LO RESPETO)
# ==========================================================
class Alumno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    matricula = models.CharField(max_length=50)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.matricula})"


# ==========================================================
# TRANSACCIONES
# ==========================================================
class Transaccion(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    amount = models.FloatField()

    txid = models.CharField(max_length=200, null=True, blank=True)
    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.amount} ALGOs)"


# ==========================================================
# ACTIVIDAD
# ==========================================================
class Actividad(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_entrega = models.DateField(null=True, blank=True)
    recompensa = models.IntegerField(default=0)

    docente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="actividades_creadas",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titulo


# ==========================================================
# ACTIVIDAD ASIGNADA
# ==========================================================
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

    evidencia_texto = models.TextField(null=True, blank=True)
    evidencia_link = models.URLField(null=True, blank=True)
    fecha_entrega_real = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.actividad.titulo} → {self.estudiante.username if self.estudiante else 'Sin asignar'}"
