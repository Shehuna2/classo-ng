# Generated by Django 4.2.2 on 2023-07-19 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_recentpdfdownload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recentpdfdownload',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_downloads', to=settings.AUTH_USER_MODEL),
        ),
    ]