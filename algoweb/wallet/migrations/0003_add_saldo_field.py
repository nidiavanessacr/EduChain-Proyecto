from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_alter_user_options_alter_user_managers_user_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='saldo',
            field=models.FloatField(default=0.0),
        ),
    ]
