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
    # 📋 Administración: Docentes / Estudiantes
    # ======================================
    path('admin/docentes/', views.admin_docentes, name='admin_docentes'),
    path('admin/estudiantes/', views.admin_estudiantes, name='admin_estudiantes'),
    path('admin/agregar_usuario/', views.admin_agregar_usuario, name='admin_agregar_usuario'),

    # ======================================
    # 🧾 Actividades (Docente y Admin)
    # ======================================
    path('crear_actividad/', views.crear_actividad, name='crear_actividad'),
    path('asignar_actividad/<int:actividad_id>/', views.asignar_actividad, name='asignar_actividad'),

    # ======================================
    # Admin: Gestión de usuarios
    # ======================================

    path('admin/docentes/', views.admin_docentes, name='admin_docentes'),
    path('admin/estudiantes/', views.admin_estudiantes, name='admin_estudiantes'),
    path('admin/agregar_usuario/', views.admin_agregar_usuario, name='admin_agregar_usuario'),

]

