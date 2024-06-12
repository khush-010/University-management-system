# Generated by Django 5.0.4 on 2024-06-07 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('R', 'Rejected'), ('P', 'Pending')], default='P', max_length=10),
        ),
        migrations.AlterField(
            model_name='application',
            name='study_mode',
            field=models.CharField(choices=[('Online', 'Online'), ('On Campus', 'On-Campus')], max_length=10),
        ),
    ]
