# Generated by Django 5.0.1 on 2024-01-25 14:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("client_app", "0007_alter_dynamicformfieldvalue_user_request"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="userrequest",
            name="completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userrequest",
            name="created_by",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_requests",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userrequest",
            name="current_approval_level",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="userrequest",
            name="description",
            field=models.TextField(default="1"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userrequest",
            name="title",
            field=models.CharField(default="1", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="dynamicformfield",
            name="field_type",
            field=models.CharField(
                choices=[
                    ("CharField", "CharField"),
                    ("IntegerField", "IntegerField"),
                    ("DateField", "DateField"),
                    ("EmailField", "EmailField"),
                    ("DecimalField", "DecimalField"),
                    ("BooleanField", "BooleanField"),
                    ("TextField", "TextField"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="dynamicformfield",
            name="form_type",
            field=models.ManyToManyField(
                related_name="dynamic_form_type", to="client_app.formtype"
            ),
        ),
        migrations.AlterField(
            model_name="dynamicformfieldvalue",
            name="user_request",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_request_form_v",
                to="client_app.userrequest",
            ),
        ),
        migrations.CreateModel(
            name="Approval",
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
                ("comment", models.TextField()),
                ("signature", models.TextField()),
                (
                    "request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="request_approvals",
                        to="client_app.userrequest",
                    ),
                ),
                (
                    "users",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_approvals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
