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

    # ======================================
    # 👥 Gestión de usuarios (Admin)
    # ======================================
    path('admin/docentes/', views.admin_ver_docentes, name='admin_ver_docentes'),
    path('admin/estudiantes/', views.admin_ver_estudiantes, name='admin_ver_estudiantes'),
    path('admin/agregar_usuario/', views.admin_agregar_usuario, name='admin_agregar_usuario'),
    path('admin/eliminar_usuario/<int:user_id>/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),
    # ======================================
    # 📝 Gestión de Actividades (Admin)
    # ======================================
    path('admin/crear_actividad/', views.admin_crear_actividad, name='admin_crear_actividad'),
    path('admin/asignar_actividad/', views.admin_asignar_actividad, name='admin_asignar_actividad'),
    # ======================================
    # 📝 Gestión de docentes (Admin)
    # ======================================
    path('admin/docentes/', views.admin_docentes, name='admin_docentes'),
    path('admin/docentes/eliminar/<int:user_id>/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),
    # ======================================
    # 📝 Gestión de docentes (Admin)
    # ======================================
    path('admin/docentes/', views.admin_docentes, name='admin_docentes'),
    path('admin/estudiantes/', views.admin_estudiantes, name='admin_estudiantes'),

    path('admin/docentes/eliminar/<int:user_id>/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),
    path('admin/estudiantes/eliminar/<int:user_id>/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),


]
