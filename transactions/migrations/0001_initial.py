# Generated by Django 4.2.11 on 2025-04-01 01:03

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
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
                (
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("deposit", "Depósito"),
                            ("transfer", "Transferência"),
                            ("withdrawal", "Saque"),
                        ],
                        max_length=10,
                        verbose_name="tipo",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pendente"),
                            ("completed", "Concluída"),
                            ("failed", "Falha"),
                        ],
                        default="pending",
                        max_length=10,
                        verbose_name="status",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                        verbose_name="valor",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="descrição"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="data de criação"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="data de atualização"
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="received_transactions",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="destinatário",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sent_transactions",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="remetente",
                    ),
                ),
            ],
            options={
                "verbose_name": "transação",
                "verbose_name_plural": "transações",
                "ordering": ["-created_at"],
            },
        ),
    ]
