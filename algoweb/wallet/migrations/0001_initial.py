from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(choices=[('admin', 'Administrador'), ('docente', 'Docente'), ('estudiante', 'Estudiante')], default='estudiante', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_entrega', models.DateField(blank=True, null=True)),
                ('recompensa', models.IntegerField(default=0)),
                ('docente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actividades_creadas', to='wallet.user')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=200)),
                ('private_key', models.CharField(max_length=200)),
                ('saldo', models.FloatField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wallet.user')),
            ],
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sender', models.CharField(max_length=100)),
                ('receiver', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('txid', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ActividadAsignada',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('entregada', models.BooleanField(default=False)),
                ('finalizada', models.BooleanField(default=False)),
                ('evidencia_texto', models.TextField(blank=True, null=True)),
                ('evidencia_link', models.URLField(blank=True, null=True)),
                ('fecha_entrega_real', models.DateTimeField(blank=True, null=True)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.actividad')),
                ('estudiante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wallet.user')),
            ],
        ),
    ]
