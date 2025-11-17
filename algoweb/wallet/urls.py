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
    # 🧭 Dashboards por rol
    # ======================================
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/docente/', views.dashboard_docente, name='dashboard_docente'),
    path('dashboard/estudiante/', views.dashboard_estudiante, name='dashboard_estudiante'),

    # ======================================
    # 📋 Admin: Gestión de usuarios
    # ======================================
    path('dashboard/admin/docentes/', views.admin_docentes, name='admin_docentes'),
    path('dashboard/admin/estudiantes/', views.admin_estudiantes, name='admin_estudiantes'),
    path('dashboard/admin/agregar_usuario/', views.admin_agregar_usuario, name='admin_agregar_usuario'),
    path('dashboard/admin/eliminar_usuario/<int:user_id>/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),

    # ======================================
    # 📝 Admin: Actividades
    # ======================================
    path('dashboard/admin/crear_actividad/', views.admin_crear_actividad, name='admin_crear_actividad'),
    path('dashboard/admin/asignar_actividad/', views.admin_asignar_actividad, name='admin_asignar_actividad'),
    path('dashboard/admin/actividades/', views.admin_ver_actividades, name='admin_ver_actividades'),

    # ======================================
    # 📚 Docente: Crear y asignar actividades propias
    # ======================================
    path('crear_actividad/', views.crear_actividad, name='crear_actividad'),
    path('asignar_actividad/<int:actividad_id>/', views.asignar_actividad, name='asignar_actividad'),
]
