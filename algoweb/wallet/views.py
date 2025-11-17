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
    "",  # token vacío para Algonode (TestNet)
    "https://testnet-api.algonode.cloud"
)

# ======================================
#  REGISTRO
# ======================================
def registro(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            return render(request, "wallet/registro.html", {
                "error": "El usuario ya existe"
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            role=role
        )

        Wallet.objects.create(
            user=user,
            address="ADDR-" + str(uuid.uuid4())[:12],
            private_key="PRIV-" + str(uuid.uuid4())[:12]
        )

        messages.success(request, "Cuenta creada exitosamente.")
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

        if user:
            login(request, user)

            if user.role == "admin":
                return redirect("dashboard_admin")
            elif user.role == "docente":
                return redirect("dashboard_docente")
            elif user.role == "estudiante":
                return redirect("dashboard_estudiante")

            logout(request)
            return render(request, "wallet/login.html", {"error": "Rol inválido."})

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

    context = {
        "total_docentes": User.objects.filter(role="docente").count(),
        "total_estudiantes": User.objects.filter(role="estudiante").count(),
        "total_actividades": Actividad.objects.count(),
        "total_asignadas": ActividadAsignada.objects.count(),
    }
    return render(request, "wallet/dashboard_admin.html", context)


# ======================================
#  VER DOCENTES
# ======================================
@login_required
def admin_docentes(request):
    if request.user.role != "admin":
        return redirect("login")

    docentes = User.objects.filter(role="docente")
    return render(request, "wallet/admin_docentes.html", {"docentes": docentes})


# ======================================
#  VER ESTUDIANTES
# ======================================
@login_required
def admin_estudiantes(request):
    if request.user.role != "admin":
        return redirect("login")

    estudiantes = User.objects.filter(role="estudiante")
    return render(request, "wallet/admin_estudiantes.html", {"estudiantes": estudiantes})


# ======================================
#  AGREGAR USUARIO (ADMIN)
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

        user = User.objects.create_user(username=username, password=password, role=role)

        Wallet.objects.create(
            user=user,
            address="ADDR-" + str(uuid.uuid4())[:12],
            private_key="PRIV-" + str(uuid.uuid4())[:12]
        )

        messages.success(request, f"{role.capitalize()} creado correctamente.")
        return redirect("dashboard_admin")

    return render(request, "wallet/admin_agregar_usuario.html")


# ======================================
#  ELIMINAR USUARIO (ADMIN)
# ======================================
@login_required
def admin_eliminar_usuario(request, user_id):
    if request.user.role != "admin":
        return redirect("login")

    usuario = get_object_or_404(User, id=user_id)

    if usuario.role == "admin":
        messages.error(request, "No puedes eliminar administradores.")
        return redirect("dashboard_admin")

    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect("dashboard_admin")


# ======================================
#  CREAR ACTIVIDAD ADMIN
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

        messages.success(request, "Actividad creada exitosamente.")
        return redirect("dashboard_admin")

    return render(request, "wallet/admin_crear_actividad.html")


# ======================================
#  ASIGNAR ACTIVIDAD A DOCENTE (ADMIN)
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
#  DASHBOARD DOCENTE
# ======================================
@login_required
def dashboard_docente(request):
    if request.user.role != "docente":
        return redirect("login")

    actividades = Actividad.objects.filter(docente=request.user)
    return render(request, "wallet/dashboard_docente.html", {"actividades": actividades})


# ======================================
#  CREAR ACTIVIDAD DOCENTE
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
#  ASIGNAR A ESTUDIANTES (DOCENTE)
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

        messages.success(request, "Actividad asignada exitosamente.")
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
    wallet = Wallet.objects.filter(user=request.user).first()

    return render(request, "wallet/mi_wallet.html", {"wallet": wallet})


# ======================================
#  HISTORIAL (AÚN SIN IMPLEMENTACIÓN BLOCKCHAIN)
# ======================================
@login_required
def transacciones(request):
    return render(request, "wallet/transacciones.html", {"historial": []})

# ======================================
#  ADMIN_DOCENTES
# ======================================

@login_required
def admin_docentes(request):
    if request.user.role != "admin":
        return redirect("login")

    docentes = User.objects.filter(role="docente")
    return render(request, "wallet/admin_docentes.html", {"docentes": docentes})

# ======================================
#  ADMIN_ESTUDIANTES
# ======================================

@login_required
def admin_estudiantes(request):
    if request.user.role != "admin":
        return redirect("login")

    estudiantes = User.objects.filter(role="estudiante")
    return render(request, "wallet/admin_estudiantes.html", {"estudiantes": estudiantes})

# ======================================
#  ADMIN_AGREGAR_USUARIO
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

        messages.success(request, f"{role.capitalize()} creado correctamente.")
        return redirect("dashboard_admin")

    return render(request, "wallet/admin_agregar_usuario.html")

# ======================================
#  ADMIN_ELIMINAR_USUARIO
# ======================================

@login_required
def admin_eliminar_usuario(request, user_id):
    if request.user.role != "admin":
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if user.role == "admin":
        messages.error(request, "No puedes eliminar administradores.")
        return redirect("dashboard_admin")

    user.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect("dashboard_admin")

# ======================================
#  ADMIN_CREAR_ACTIVIDAD
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
            fecha_entrega=fecha
        )

        actividad.recompensa = recompensa
        actividad.save()

        messages.success(request, "Actividad creada correctamente.")
        return redirect("dashboard_admin")

    return render(request, "wallet/admin_crear_actividad.html")

# ======================================
#  ADMIN_ASIGNAR_ACTIVIDAD
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
#  ADMIN_VER_ACTIVIDAD_ASIGNADA
# ======================================

@login_required
def admin_ver_actividades(request):
    if request.user.role != "admin":
        return redirect("login")

    actividades = Actividad.objects.all().select_related("docente")

    return render(request, "wallet/admin_ver_actividades.html", {
        "actividades": actividades
    })
