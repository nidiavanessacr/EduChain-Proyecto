from django.core.management.base import BaseCommand
from wallet.models import User
from algosdk import account

class Command(BaseCommand):
    help = "Regenera wallets reales para usuarios existentes"

    def handle(self, *args, **kwargs):

        usuarios = ["vane", "docente", "nidia", "alex"]

        for nombre in usuarios:
            user = User.objects.get(username=nombre)
            wallet = user.wallet

            private_key, address = account.generate_account()

            wallet.address = address
            wallet.private_key = private_key
            wallet.saldo = 0
            wallet.save()

            self.stdout.write(f"{nombre} → {address}")

        self.stdout.write(self.style.SUCCESS("Wallets actualizadas correctamente"))
