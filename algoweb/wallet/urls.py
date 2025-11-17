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

    path('dashboard/admin/actividad/<int:id>/editar/', 
         views.admin_editar_actividad, 
         name='admin_editar_actividad'),

    path('dashboard/admin/actividad/<int:id>/eliminar/', 
         views.admin_eliminar_actividad, 
         name='admin_eliminar_actividad'),

    # ======================================
    # 📘 Docente: Actividades del docente
    # ======================================
    path('dashboard/docente/actividades/', 
         views.docente_actividades, 
         name='docente_actividades'),

    # ======================================
    # 📋 Docente: Revisar una actividad específica
    # ======================================
    path('dashboard/docente/actividad/<int:actividad_id>/revisar/', 
         views.docente_revisar_entregas, 
         name='docente_revisar_entregas'),

    # ======================================
    # ✅ Docente: Marcar entrega finalizada
    # ======================================
    path('dashboard/docente/marcar_finalizada/<int:asignacion_id>/', 
         views.docente_marcar_finalizada, 
         name='docente_marcar_finalizada'),

    path('dashboard/docente/marcar_finalizada/<int:asignacion_id>/confirmar/', 
         views.docente_marcar_finalizada_confirmar, 
         name='docente_marcar_finalizada_confirmar'),

    # ======================================
    # 💰 Wallet
    # ======================================
    path('miwallet/', views.mi_wallet, name='mi_wallet'),
    path('get_balance/', views.get_balance, name='get_balance'),
]
