from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Wallet, Alumno, Transaccion, ActividadAsignada


# =========================
# USUARIO PERSONALIZADO
# =========================
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rol en el sistema', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')


# =========================
# WALLET ADMIN
# =========================
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    search_fields = ('user__username', 'address')


# =========================
# ALUMNO ADMIN
# =========================
@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'matricula', 'wallet')
    search_fields = ('user__username', 'email', 'matricula')
    ordering = ('matricula',)


# =========================
# TRANSACCIÓN ADMIN
# =========================
@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'tipo', 'estado', 'txid')
    list_filter = ('tipo', 'estado')
    search_fields = ('sender', 'receiver', 'txid')


# =========================
# ACTIVIDAD ASIGNADA ADMIN
# =========================
@admin.register(ActividadAsignada)
class ActividadAsignadaAdmin(admin.ModelAdmin):
    list_display = ('id', 'actividad', 'estudiante', 'entregada', 'finalizada')
    list_filter = ('entregada', 'finalizada')
    search_fields = ('actividad__titulo', 'estudiante__username')
    ordering = ('id',)
