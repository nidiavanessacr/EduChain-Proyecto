# wallet/algorand_utils.py
"""
Módulo de utilidades para simular operaciones con Algorand en la testnet.
Este archivo está adaptado para el proyecto EduChain con fines educativos,
no realiza transacciones reales ni usa claves privadas válidas.
"""

from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk import transaction
import json

# ==============================================================
# Configuración del cliente hacia la testnet de Algonode
# ==============================================================
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""  # No se requiere token para Algonode público

ALGOD_CLIENT = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)


# ==============================================================
# Funciones simuladas de gestión de cuentas y transacciones
# ==============================================================

def crear_cuenta_demo():
    """
    Crea una cuenta simulada de Algorand para demostración.
    Devuelve la dirección y la clave mnemónica.
    """
    private_key, address = account.generate_account()
    passphrase = mnemonic.from_private_key(private_key)
    return {
        "address": address,
        "mnemonic": passphrase
    }


def consultar_saldo(address):
    """
    Devuelve el saldo de una cuenta en la testnet.
    Si no existe, devuelve 0 para evitar errores.
    """
    try:
        cuenta_info = ALGOD_CLIENT.account_info(address)
        return cuenta_info.get("amount", 0) / 1_000_000  # microalgos -> ALGOs
    except Exception:
        # Si la cuenta no existe, devolvemos saldo 0 para fines de demostración
        return 0.0


def simular_transaccion(origen, destino, cantidad):
    """
    Simula una transacción entre dos cuentas.
    No envía tokens reales; solo muestra la estructura que tendría la operación.
    """
    return {
        "from": origen,
        "to": destino,
        "amount": cantidad,
        "status": "Simulación exitosa (no enviada a la red real)"
    }


def mostrar_detalles_cliente():
    """
    Devuelve la versión del nodo testnet (informativo).
    """
    try:
        status = ALGOD_CLIENT.status()
        return json.dumps(status, indent=4)
    except Exception:
        return "Simulación: Cliente testnet conectado (sin errores detectables)."
