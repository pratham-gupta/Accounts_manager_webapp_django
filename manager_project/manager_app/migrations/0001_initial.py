# Generated by Django 3.0.3 on 2020-09-04 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Add_benificiary_name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Benificiary_Name', models.CharField(max_length=100, unique=True)),
                ('Benificiary_address', models.CharField(blank=True, max_length=200, null=True)),
                ('Benificary_GST_Number', models.CharField(blank=True, max_length=25, null=True, unique=True)),
                ('Benificiary_AC_number', models.DecimalField(decimal_places=0, default=0, max_digits=20, null=True)),
                ('Benificiary_Bank', models.CharField(max_length=100)),
                ('Benificiary_ph_no', models.DecimalField(decimal_places=0, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
            ],
            options={
                'verbose_name_plural': '5. Benificiary Names',
            },
        ),
        migrations.CreateModel(
            name='Add_Firm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firm_name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': '3. Add Firm',
            },
        ),
        migrations.CreateModel(
            name='BillCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_type', models.CharField(choices=[('SL', 'SALE'), ('PR', 'PURCHASE')], max_length=2)),
            ],
            options={
                'verbose_name_plural': '-> Bill Category',
            },
        ),
        migrations.CreateModel(
            name='GenericExpenseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('HE', 'House Expense'), ('FE', 'Factory Expense'), ('SE', 'Shop Expense'), ('ME', 'Miscellaneous Expense')], max_length=2)),
            ],
            options={
                'verbose_name_plural': '-> General Expenses',
            },
        ),
        migrations.CreateModel(
            name='Payment_Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('CS', 'CASH'), ('CQ', 'CHEQUE'), ('ON', 'RTGS/NEFT/IMPS')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='PayrollCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('FL', 'Factory Labour'), ('SL', 'Shop Labour'), ('LL', 'Loading Labour')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, unique=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('balance', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('work_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_app.PayrollCategory')),
            ],
            options={
                'verbose_name_plural': '-> Person',
            },
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('date_added', models.DateField()),
                ('final_value', models.DecimalField(decimal_places=1, default=0, max_digits=20, null=True)),
                ('paid_value', models.DecimalField(decimal_places=1, default=0, max_digits=20)),
                ('is_paid', models.BooleanField(default=False)),
                ('payment_type', models.CharField(blank=True, choices=[('CR', 'CREDIT'), ('DR', 'DEBIT')], max_length=2, null=True)),
                ('payment_update_date', models.DateField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_payroll', to='manager_app.PayrollCategory')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_app.Payment_Method')),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_payroll', to='manager_app.Person')),
            ],
            options={
                'verbose_name_plural': '-> Payroll',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='GenericExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('date_added', models.DateField()),
                ('final_value', models.DecimalField(decimal_places=1, default=0, max_digits=20, null=True)),
                ('paid_value', models.DecimalField(decimal_places=1, default=0, max_digits=20)),
                ('is_paid', models.BooleanField(default=False)),
                ('payment_type', models.CharField(blank=True, choices=[('CR', 'CREDIT'), ('DR', 'DEBIT')], max_length=2, null=True)),
                ('payment_update_date', models.DateField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_expenses', to='manager_app.GenericExpenseCategory')),
                ('firm_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='firm_expense_rel', to='manager_app.Add_Firm')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_app.Payment_Method')),
            ],
            options={
                'verbose_name_plural': '-> Generic Expense',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('date_added', models.DateField()),
                ('final_value', models.DecimalField(decimal_places=1, default=0, max_digits=20, null=True)),
                ('paid_value', models.DecimalField(decimal_places=1, default=0, max_digits=20)),
                ('is_paid', models.BooleanField(default=False)),
                ('payment_type', models.CharField(blank=True, choices=[('CR', 'CREDIT'), ('DR', 'DEBIT')], max_length=2, null=True)),
                ('payment_update_date', models.DateField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('benificiary_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='benificiary_bill', to='manager_app.Add_benificiary_name')),
                ('bill_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_category_rel', to='manager_app.BillCategory')),
                ('firm_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_app.Add_Firm')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_app.Payment_Method')),
            ],
            options={
                'verbose_name_plural': '->Bills',
                'ordering': ['-date_added'],
            },
        ),
    ]
