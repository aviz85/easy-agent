# Generated by Django 5.0.7 on 2024-08-05 23:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commission', '0002_remove_agreement_commissions_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='commissionstructure',
            name='agent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='commissionstructure',
            name='agreement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commission.agreement'),
        ),
    ]
