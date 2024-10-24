# Generated by Django 5.1.2 on 2024-10-16 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SalesRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employee_name', models.CharField(max_length=100)),
                ('created', models.DateTimeField()),
                ('dated', models.DateField()),
                ('lead_taken', models.IntegerField()),
                ('tours_booked', models.IntegerField()),
                ('applications', models.IntegerField()),
                ('tours_per_lead', models.FloatField()),
                ('apps_per_tour', models.FloatField()),
                ('apps_per_lead', models.FloatField()),
                ('mon_text', models.IntegerField()),
                ('tue_text', models.IntegerField()),
                ('wed_text', models.IntegerField()),
                ('thur_text', models.IntegerField()),
                ('fri_text', models.IntegerField()),
                ('sat_text', models.IntegerField()),
                ('sun_text', models.IntegerField()),
                ('mon_call', models.IntegerField()),
                ('tue_call', models.IntegerField()),
                ('wed_call', models.IntegerField()),
                ('thur_call', models.IntegerField()),
                ('fri_call', models.IntegerField()),
                ('sat_call', models.IntegerField()),
                ('sun_call', models.IntegerField()),
            ],
        ),
    ]
