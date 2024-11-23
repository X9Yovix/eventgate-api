# Generated by Django 5.1.1 on 2024-11-21 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestedtojoin',
            name='status',
            field=models.CharField(choices=[('ACCEPTED', 'Accepted'), ('PENDING', 'Pending'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=10),
        ),
    ]