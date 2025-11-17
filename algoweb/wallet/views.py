from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import User, Wallet, Actividad, ActividadAsignada

import uuid
from algosdk.v2client import algod



# ======================================
#  CONFIG ALGOD
# ======================================
ALGOD_CLIENT = algod.AlgodClient("", "https://testnet-api.algonode.cloud")



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
# LOGOUT
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
#  ADMIN: GESTIÓN DE USUARIOS
# ======================================
@login_required
def admin_docentes(request):
    if request.user.role != "admin":
        return redirect("login")

    return render(request, "wallet/admin_docentes.html", {
        "docentes": User.objects.filter(role="docente")
    })


@login_required
def admin_estudiantes(request):
    if request.user.role != "admin":
        return redirect("login")

    return render(request, "wallet/admin_estudiantes.html", {
        "estudiantes": User.objects.filter(role="estudiante")
    })


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
#  ADMIN: ACTIVIDADES
# ======================================
@login_required
def admin_crear_actividad(request):
    if request.user.role != "admin":
        return redirect("login")

    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        fecha = request.POST.get("fecha")  # dd/mm/aaaa
        recompensa = request.POST.get("recompensa")

        try:
            d, m, y = fecha.split("/")
            fecha_convertida = f"{y}-{m}-{d}"
        except:
            messages.error(request, "Formato de fecha inválido. Usa dd/mm/aaaa.")
            return redirect("admin_crear_actividad")

        Actividad.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha_entrega=fecha_convertida,
            recompensa=recompensa
        )

        messages.success(request, "Actividad creada exitosamente.")
        return redirect("dashboard_admin")

    return render(request, "wallet/admin_crear_actividad.html")



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



@login_required
def admin_ver_actividades(request):
    if request.user.role != "admin":
        return redirect("login")

    actividades = Actividad.objects.select_related("docente").all()

    return render(request, "wallet/admin_ver_actividades.html", {
        "actividades": actividades
    })



@login_required
def admin_editar_actividad(request, id):
    if request.user.role != "admin":
        return redirect("login")

    actividad = get_object_or_404(Actividad, id=id)

    if request.method == "POST":
        actividad.titulo = request.POST.get("titulo")
        actividad.descripcion = request.POST.get("descripcion")
        fecha = request.POST.get("fecha")

        try:
            d, m, y = fecha.split("/")
            actividad.fecha_entrega = f"{y}-{m}-{d}"
        except:
            messages.error(request, "Error: usa dd/mm/aaaa.")
            return redirect("admin_editar_actividad", id=id)

        actividad.recompensa = request.POST.get("recompensa")
        actividad.save()

        messages.success(request, "Actividad actualizada.")
        return redirect("admin_ver_actividades")

    return render(request, "wallet/admin_editar_actividad.html", {"actividad": actividad})



@login_required
def admin_eliminar_actividad(request, id):
    if request.user.role != "admin":
        return redirect("login")

    actividad = get_object_or_404(Actividad, id=id)
    actividad.delete()

    messages.success(request, "Actividad eliminada.")
    return redirect("admin_ver_actividades")



# ======================================
#  DASHBOARD DOCENTE
# ======================================
@login_required
def dashboard_docente(request):
    if request.user.role != "docente":
        return redirect("login")

    return render(request, "wallet/dashboard_docente.html")



# ======================================
#  DOCENTE: MIS ACTIVIDADES
# ======================================
@login_required
def docente_actividades(request):
    if request.user.role != "docente":
        return redirect("dashboard_docente")

    actividades = Actividad.objects.filter(docente=request.user)

    return render(request, "wallet/docente_actividades.html", {
        "actividades": actividades
    })



# ======================================
#  DOCENTE: REVISAR ENTREGAS
# ======================================
@login_required
def docente_revisar_entregas(request, actividad_id):
    if request.user.role != "docente":
        return redirect("dashboard_docente")

    actividad = get_object_or_404(Actividad, id=actividad_id, docente=request.user)
    asignaciones = ActividadAsignada.objects.filter(actividad=actividad)

    return render(request, "wallet/docente_revisar_entregas.html", {
        "actividad": actividad,
        "asignaciones": asignaciones
    })



# ======================================
#  DOCENTE: MARCAR FINALIZADA
# ======================================
@login_required
def docente_marcar_finalizada(request, asignacion_id):
    asignacion = get_object_or_404(
        ActividadAsignada,
        id=asignacion_id,
        actividad__docente=request.user
    )

    return render(request, "wallet/docente_marcar_finalizada.html", {
        "asignacion": asignacion
    })



@login_required
def docente_marcar_finalizada_confirmar(request, asignacion_id):
    asignacion = get_object_or_404(
        ActividadAsignada,
        id=asignacion_id,
        actividad__docente=request.user
    )

    asignacion.finalizada = True
    asignacion.save()

    messages.success(request, f"Entrega finalizada para {asignacion.estudiante.username}.")

    return redirect("docente_revisar_entregas", actividad_id=asignacion.actividad.id)



# ======================================
#  WALLET
# ======================================
@login_required
def mi_wallet(request):
    wallet = Wallet.objects.filter(user=request.user).first()
    return render(request, "wallet/mi_wallet.html", {"wallet": wallet})



@login_required
def get_balance(request):
    address = request.GET.get("address")

    if not address:
        return JsonResponse({"error": "No se proporcionó dirección"}, status=400)

    try:
        info = ALGOD_CLIENT.account_info(address)
        balance = info.get("amount", 0) / 1_000_000
        return JsonResponse({"balance": balance})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



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
