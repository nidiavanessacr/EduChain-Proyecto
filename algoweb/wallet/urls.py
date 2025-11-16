from django.urls import path
from . import views

urlpatterns = [

    # ======================================
    # 🔐 Autenticación
    # ======================================
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),

    # ======================================
    # 🧭 Dashboards según rol
    # ======================================
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/docente/', views.dashboard_docente, name='dashboard_docente'),
    path('dashboard/estudiante/', views.dashboard_estudiante, name='dashboard_estudiante'),

    # ======================================
    # 🧾 Actividades (Docente)
    # ======================================
    path('crear_actividad/', views.crear_actividad, name='crear_actividad'),
    path('asignar_actividad/<int:actividad_id>/', views.asignar_actividad, name='asignar_actividad'),

    # ======================================
    # 🧾 Funciones del Estudiante
    # ======================================
    path('envio/', views.envio, name='envio'),
    path('mi_wallet/', views.mi_wallet, name='mi_wallet'),
    path('transacciones/', views.transacciones, name='transacciones'),

    # ======================================
    # 💰 Consultar saldo en Algorand TestNet
    # ======================================
    path('get_balance/', views.get_balance, name='get_balance'),
]
