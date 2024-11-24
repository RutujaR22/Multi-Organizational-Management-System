# Generated by Django 4.2.11 on 2024-11-22 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Role_Management", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="role",
                to="Role_Management.role",
            ),
        ),
    ]