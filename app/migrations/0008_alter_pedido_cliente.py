# Generated by Django 4.1.7 on 2023-06-02 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_pedido_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='cliente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.cliente'),
        ),
    ]