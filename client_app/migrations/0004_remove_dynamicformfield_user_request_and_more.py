# Generated by Django 5.0.1 on 2024-01-17 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("client_app", "0003_dynamicformfield_user_request"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dynamicformfield",
            name="user_request",
        ),
        migrations.CreateModel(
            name="DynamicFormFieldValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=255)),
                ("field_value", models.CharField(max_length=50)),
                (
                    "user_request",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="client_app.userrequest",
                    ),
                ),
            ],
        ),
    ]
