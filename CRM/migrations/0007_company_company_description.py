# Generated by Django 3.1.6 on 2021-12-06 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0006_auto_20211206_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
