# Generated by Django 5.1.2 on 2024-10-18 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_analysis', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesrecord',
            name='created',
        ),
        migrations.RemoveField(
            model_name='salesrecord',
            name='dated',
        ),
        migrations.AddField(
            model_name='salesrecord',
            name='created_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='salesrecord',
            name='employee_name',
            field=models.CharField(max_length=255),
        ),
    ]
