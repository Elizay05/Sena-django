# Generated by Django 5.0.1 on 2024-01-26 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_alter_usuario_correo'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='foto',
            field=models.ImageField(default='fotos_productos/default.png', upload_to='fotos_productos/'),
        ),
        migrations.AlterField(
            model_name='productos',
            name='nombre',
            field=models.CharField(max_length=254, unique=True),
        ),
    ]
