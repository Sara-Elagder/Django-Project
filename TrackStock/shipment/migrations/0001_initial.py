# Generated by Django 5.1.7 on 2025-03-15 13:30
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factory_name', models.CharField(default='Default Factory', max_length=255)),
                ('date_received', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Received', 'Received')], default='Pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ShipmentItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product')),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shipment.shipment')),
            ],
        ),
        migrations.AddField(
            model_name='shipment',
            name='products',
            field=models.ManyToManyField(through='shipment.ShipmentItem', to='inventory.product'),
        ),
    ]
