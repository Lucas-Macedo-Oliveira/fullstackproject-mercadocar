# Generated by Django 4.1.7 on 2023-10-02 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_contato'),
    ]

    operations = [
        migrations.AddField(
            model_name='contato',
            name='arquivado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contato',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='contato',
            name='nome',
            field=models.CharField(max_length=100),
        ),
    ]
