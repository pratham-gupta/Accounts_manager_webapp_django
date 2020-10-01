# Generated by Django 3.0.3 on 2020-09-04 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payroll',
            name='category',
        ),
        migrations.AddField(
            model_name='payroll',
            name='firm_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payroll_firm', to='manager_app.Add_Firm'),
            preserve_default=False,
        ),
    ]