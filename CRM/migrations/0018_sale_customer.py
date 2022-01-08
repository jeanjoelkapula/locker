# Generated by Django 3.1.6 on 2022-01-05 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0017_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='CRM.customer'),
            preserve_default=False,
        ),
    ]
