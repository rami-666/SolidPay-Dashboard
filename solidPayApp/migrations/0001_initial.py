# Generated by Django 4.2.1 on 2023-05-25 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='nonEmptyWallets',
            fields=[
                ('privateKey', models.CharField(max_length=1000, primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=500)),
                ('balance', models.DecimalField(decimal_places=10, max_digits=30)),
            ],
        ),
        migrations.CreateModel(
            name='paymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=500)),
                ('amount', models.DecimalField(decimal_places=10, max_digits=30)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='paymentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privateKey', models.CharField(max_length=1000)),
                ('createdAddress', models.CharField(max_length=500)),
                ('pendingAmount', models.DecimalField(decimal_places=10, max_digits=30)),
                ('destinationAddress', models.CharField(max_length=500)),
                ('fullfilled', models.BooleanField(default=False)),
                ('requestDate', models.DateTimeField()),
            ],
        ),
    ]
