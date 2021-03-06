# Generated by Django 3.1.6 on 2022-01-05 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0018_sale_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadLoss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(max_length=255)),
                ('date', models.DateField(auto_now_add=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='losses', to='CRM.lead')),
            ],
        ),
    ]
