# Generated by Django 4.1.7 on 2023-06-02 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_cliente_id_pedido_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='cliente',
            field=models.CharField(max_length=255),
        ),
    ]
