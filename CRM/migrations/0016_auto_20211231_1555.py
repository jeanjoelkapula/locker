# Generated by Django 3.1.6 on 2021-12-31 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0015_auto_20211231_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadprogress',
            name='task_lines',
            field=models.ManyToManyField(blank=True, to='CRM.TaskProgessLine'),
        ),
    ]
