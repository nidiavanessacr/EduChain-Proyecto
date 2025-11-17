from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wallet.models import Wallet
from algosdk import account


class Command(BaseCommand):
    help = 'Genera wallets para usuarios que no tengan una'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        usuarios = User.objects.all()

        creadas = 0

        for usuario in usuarios:
            # Si el usuario ya tiene wallet, saltar
            if Wallet.objects.filter(user=usuario).exists():
                continue

            # Crear wallet nueva
            private_key, address = account.generate_account()
            Wallet.objects.create(
                user=usuario,
                address=address,
                private_key=private_key
            )
            creadas += 1
            self.stdout.write(self.style.SUCCESS(f"Wallet creada para {usuario.username}"))

        if creadas == 0:
            self.stdout.write(self.style.WARNING("Todos los usuarios ya tienen wallet."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Listo. Wallets creadas: {creadas}"))
