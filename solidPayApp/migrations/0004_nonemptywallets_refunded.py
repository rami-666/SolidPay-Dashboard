# Generated by Django 4.2.1 on 2023-06-04 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solidPayApp', '0003_usdpaymentrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonemptywallets',
            name='refunded',
            field=models.BooleanField(default=False),
        ),
    ]