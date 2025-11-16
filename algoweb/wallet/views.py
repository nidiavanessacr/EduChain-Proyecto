from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import User, Wallet, Actividad, ActividadAsignada

import uuid
from algosdk.v2client import algod


# ======================================
#  CONFIGURACIÓN DEL CLIENTE ALGOD
# ======================================
ALGOD_CLIENT = algod.AlgodClient(
    "",  # token vacío para Algonode
    "https://testnet-api.algonode.cloud"
)


# ======================================
#  REGISTRO
# ======================================
def registro(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")  # <- Campo correcto

        if User.objects.filter(username=username).exists():
            return render(request, "wallet/registro.html", {
                "error": "El usuario ya existe"
            })

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            password=password,
            role=role
        )

        # Crear wallet automática
        Wallet.objects.create(
            user=user,
            address="ADDR-" + str(uuid.uuid4())[:12],
            private_key="PRIV-" + str(uuid.uuid4())[:12]
        )

        messages.success(request, "Cuenta creada exitosamente. Ya puedes iniciar sesión.")
        return redirect("login")

    return render(request, "wallet/registro.html")


# ======================================
#  LOGIN
# ======================================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirección según rol
            if user.role == "admin":
                return redirect("dashboard_admin")
            elif user.role == "docente":
                return redirect("dashboard_docente")
            elif user.role == "estudiante":
                return redirect("dashboard_estudiante")

            logout(request)
            return render(request, "wallet/login.html", {
                "error": "Rol inválido en el usuario."
            })

        return render(request, "wallet/login.html", {
            "error": "Usuario o contraseña incorrectos."
        })

    return render(request, "wallet/login.html")


# ======================================
#  LOGOUT
# ======================================
def logout_view(request):
    logout(request)
    return redirect("login")


# ======================================
#  DASHBOARD ADMIN
# ======================================
@login_required
def dashboard_admin(request):
    if request.user.role != "admin":
        return redirect("login")

    docentes = User.objects.filter(role="docente")
    estudiantes = User.objects.filter(role="estudiante")

    return render(request, "wallet/dashboard_admin.html", {
        "docentes": docentes,
        "estudiantes": estudiantes
    })


# ======================================
#  DASHBOARD DOCENTE
# ======================================
@login_required
def dashboard_docente(request):
    if request.user.role != "docente":
        return redirect("login")

    actividades = Actividad.objects.filter(docente=request.user)

    return render(request, "wallet/dashboard_docente.html", {
        "actividades": actividades
    })


# ======================================
#  CREAR ACTIVIDAD (DOCENTE)
# ======================================
@login_required
def crear_actividad(request):
    if request.user.role != "docente":
        return redirect("login")

    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        fecha = request.POST.get("fecha")

        Actividad.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha_entrega=fecha,
            docente=request.user
        )

        messages.success(request, "Actividad creada correctamente.")
        return redirect("dashboard_docente")

    return render(request, "wallet/crear_actividad.html")


# ======================================
#  ASIGNAR ACTIVIDAD
# ======================================
@login_required
def asignar_actividad(request, actividad_id):
    if request.user.role != "docente":
        return redirect("login")

    actividad = get_object_or_404(Actividad, id=actividad_id)
    estudiantes = User.objects.filter(role="estudiante")

    if request.method == "POST":
        ids = request.POST.getlist("estudiantes")

        for est_id in ids:
            estudiante = User.objects.get(id=est_id)

            ActividadAsignada.objects.get_or_create(
                actividad=actividad,
                estudiante=estudiante
            )

        messages.success(request, "Actividad asignada con éxito.")
        return redirect("dashboard_docente")

    return render(request, "wallet/asignar_actividad.html", {
        "actividad": actividad,
        "estudiantes": estudiantes
    })


# ======================================
#  DASHBOARD ESTUDIANTE
# ======================================
@login_required
def dashboard_estudiante(request):
    if request.user.role != "estudiante":
        return redirect("login")

    actividades = ActividadAsignada.objects.filter(estudiante=request.user)

    return render(request, "wallet/dashboard_estudiante.html", {
        "actividades": actividades
    })


# ======================================
#  CONSULTAR SALDO EN TESTNET
# ======================================
@login_required
def get_balance(request):
    address = request.GET.get("address")

    if not address:
        return JsonResponse({"error": "No se proporcionó una dirección"}, status=400)

    try:
        info = ALGOD_CLIENT.account_info(address)
        balance = info.get("amount", 0) / 1_000_000
        return JsonResponse({"balance": balance})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ======================================
#  PÁGINA DE CONSULTA DE SALDO
# ======================================
@login_required
def envio(request):
    return render(request, "wallet/envio.html")


# ======================================
#  MI WALLET
# ======================================
@login_required
def mi_wallet(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = None

    return render(request, "wallet/mi_wallet.html", {
        "wallet": wallet
    })


# ======================================
#  HISTORIAL DE TRANSACCIONES
# ======================================
@login_required
def transacciones(request):
    historial = []  # Actualiza cuando agregues transacciones reales

    return render(request, "wallet/transacciones.html", {
        "historial": historial
    })

# ======================================
#  VER DOCENTES
# ======================================

@login_required
def admin_ver_docentes(request):
    if request.user.role != "admin":
        return redirect("login")

    docentes = User.objects.filter(role="docente")
    return render(request, "wallet/admin_docentes.html", {"docentes": docentes})

# ======================================
#  VER ESTUDIANTES
# ======================================

@login_required
def admin_ver_estudiantes(request):
    if request.user.role != "admin":
        return redirect("login")

    estudiantes = User.objects.filter(role="estudiante")
    return render(request, "wallet/admin_estudiantes.html", {"estudiantes": estudiantes})

# ======================================
#  Agregar usuario (admin crea docente o estudiante)
# ======================================

@login_required
def admin_agregar_usuario(request):
    if request.user.role != "admin":
        return redirect("login")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            return render(request, "wallet/admin_agregar_usuario.html", {
                "error": "El usuario ya existe."
            })

        nuevo = User.objects.create_user(username=username, password=password, role=role)

        Wallet.objects.create(
            user=nuevo,
            address="ADDR-" + str(uuid.uuid4())[:12],
            private_key="PRIV-" + str(uuid.uuid4())[:12]
        )

        messages.success(request, f"{role} creado correctamente.")
        return redirect("dashboard_admin")

    return render(request, "wallet/admin_agregar_usuario.html")

# ======================================
#  Eliminar usuario
# ======================================

@login_required
def admin_eliminar_usuario(request, user_id):
    if request.user.role != "admin":
        return redirect("login")

    usuario = get_object_or_404(User, id=user_id)
    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect("dashboard_admin")

# ======================================
#  CREACIÓN DE ACTIVIDAD (ADMIN)
# ======================================

@login_required
def admin_crear_actividad(request):
    if request.user.role != "admin":
        return redirect("login")

    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        fecha = request.POST.get("fecha")
        recompensa = request.POST.get("recompensa")

        actividad = Actividad.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha_entrega=fecha,
        )

        actividad.recompensa = recompensa
        actividad.save()

        messages.success(request, "Actividad creada correctamente.")
        return redirect("dashboard_admin")

    return render(request, "wallet/admin_crear_actividad.html")

# ======================================
#  Asignar actividad + recompensa a un docente
# ======================================

@login_required
def admin_asignar_actividad(request):
    if request.user.role != "admin":
        return redirect("login")

    actividades = Actividad.objects.all()
    docentes = User.objects.filter(role="docente")

    if request.method == "POST":
        act_id = request.POST.get("actividad")
        doc_id = request.POST.get("docente")

        actividad = Actividad.objects.get(id=act_id)
        docente = User.objects.get(id=doc_id)

        actividad.docente = docente
        actividad.save()

        messages.success(request, "Actividad asignada correctamente.")
        return redirect("dashboard_admin")

    return render(request, "wallet/admin_asignar_actividad.html", {
        "actividades": actividades,
        "docentes": docentes
    })

# ======================================
#  Lógica del rol de administrador completada
# ======================================

@login_required
def dashboard_admin(request):
    if request.user.role != "admin":
        return redirect("login")

    context = {
        "total_docentes": User.objects.filter(role="docente").count(),
        "total_estudiantes": User.objects.filter(role="estudiante").count(),
        "total_actividades": Actividad.objects.count(),
        "total_asignadas": ActividadAsignada.objects.count(),
    }

    return render(request, "wallet/dashboard_admin.html", context)

# ======================================
#  Ver gestión de docentes (admin)
# ======================================

@login_required
def admin_docentes(request):
    if request.user.role != "admin":
        return redirect("login")

    docentes = User.objects.filter(role="docente")

    return render(request, "wallet/admin_docentes.html", {
        "docentes": docentes,
    })


@login_required
def admin_eliminar_usuario(request, user_id):
    if request.user.role != "admin":
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    # Seguridad: no permitir borrar otros admins
    if user.role == "admin":
        messages.error(request, "No puedes eliminar administradores.")
        return redirect("admin_docentes")

    user.delete()
    messages.success(request, "Docente eliminado correctamente.")
    return redirect("admin_docentes")

# ======================================
#  Ver gestión de docentes2 (admin)
# ======================================

@login_required
def admin_estudiantes(request):
    if request.user.role != "admin":
        return redirect("login")

    estudiantes = User.objects.filter(role="estudiante")

    return render(request, "wallet/admin_estudiantes.html", {
        "estudiantes": estudiantes,
    })

