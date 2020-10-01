from django.db import models
from django.db.models import Sum,F
import datetime
from django.utils import timezone
from manager_app.managers import GeneralManager
from django.urls import reverse_lazy,reverse
from datetime import date


# Create your models here.
CURRENCY = 'Rs'
class Payment_Method(models.Model):
    PAYMENT_CHOICES = [('CS','CASH'),
                        ('CQ','CHEQUE'),
                        ('ON','RTGS/NEFT/IMPS')]
    method = models.CharField(max_length=2,choices=PAYMENT_CHOICES)

    def __str__(self):
        return self.get_method_display()





class DefaultExpenseModel(models.Model):

    PAYMENT_TYPES = [('CR','CREDIT'),
                    ('DR','DEBIT')]

    
    author = models.ForeignKey('auth.User',on_delete = models.SET_NULL,null=True)
    title = models.CharField(max_length=100,blank=True,null=True)
    date_added = models.DateField()
    final_value = models.DecimalField(default=0,null=True,decimal_places=1,max_digits=20)
    paid_value = models.DecimalField(default=0,decimal_places=1,max_digits=20)
    is_paid = models.BooleanField(default=False)
    payment_method = models.ForeignKey(Payment_Method, on_delete = models.CASCADE)
    payment_type = models.CharField(blank=True,null=True,max_length=2,choices=PAYMENT_TYPES)
    objects = models.Manager()
    my_query = GeneralManager()
    payment_update_date = models.DateField(blank=True,null=True)

    class Meta:
        abstract = True
    def tag_is_paid(self):
        return 'Is Paid' if self.is_paid else 'Not Paid'
     
   

    def pay_status_update(self):
        self.is_paid = True
        self.paid_value = self.final_value
        self.payment_update_date = timezone.now()
        self.save()

    def save(self,*args,**kwargs):
        if self.paid_value == self.final_value:
            self.payment_update_date = timezone.now()
            self.is_paid = True
        else:
            self.is_paid = False
        
        super(DefaultExpenseModel,self).save(*args,**kwargs)
    def __str__(self):
        return self.title

    @staticmethod
    def analysis(queryset):
        total_value = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset else 0
        paid_value = queryset.aggregate(Sum('paid_value'))['paid_value__sum']\
            if queryset else 0
        diff = total_value - paid_value
        # category_analysis = queryset.values('bill_category_rel').annotate(total_value=Sum('final_value'),
        #                                                                remaining=Sum(F('final_value')-F('paid_value'))
        #                                                                ).order_by('remaining')
        return [total_value, paid_value, diff]





class Add_benificiary_name(models.Model):
    Benificiary_Name = models.CharField(max_length=100,unique=True)
    Benificiary_address = models.CharField(max_length=200,blank=True,null=True)
    Benificary_GST_Number  = models.CharField(max_length=25,blank=True,null=True,unique=True)
    Benificiary_AC_number = models.DecimalField(default=0000000000,decimal_places=0,max_digits=20,null=True)
    Benificiary_Bank = models.CharField(max_length=100)
    Benificiary_ph_no = models.DecimalField(decimal_places=0,max_digits=10)
    balance = models.DecimalField(max_digits=20,decimal_places=0,null=True)
    def __str__(self):
        return self.Benificiary_Name
    class Meta:
        verbose_name_plural = "5. Benificiary Names"
    def get_absolute_url(self):
        return reverse_lazy('manager_app:bill_create')
    

    def update_benificiary(self):
        queryset = self.benificiary_bill.all()
        sale_queryset = queryset.filter(bill_category = 1)
        sale_debit = sale_queryset.aggregate(Sum('final_value'))['final_value__sum'] \
            if sale_queryset else 0 # Sale Bill goes to Debit
        # payment recvd against a bill goes to CR
        sale_credit = sale_queryset.aggregate(Sum('paid_value'))['paid_value__sum'] \
            if sale_queryset else 0
        # purchase bill amount goes to CR
        # purchase payment amount goes to DR
        purchase_queryset = queryset.filter(bill_category = 2)
        purchase_credit = purchase_queryset.aggregate(Sum('final_value'))['final_value__sum'] \
            if purchase_queryset else 0
        purchase_debit = purchase_queryset.aggregate(Sum('paid_value'))['paid_value__sum'] if purchase_queryset else 0
        self.balance = (sale_debit - sale_credit) + ( purchase_debit - purchase_credit)
        self.save()
    def tag_balance(self):
        if self.balance >=0:
            status = "DR"
        else:
            status = 'CR'
        return f"{self.balance} {status}"
    tag_balance.short_description = 'Total Balance'
    @staticmethod
    def filters_data(request,queryset):
        search_name = request.GET.get('search_name',None)
        queryset = queryset.filter(Benificiary_Name__icontains=search_name) if search_name else queryset
        return queryset






class Add_Firm(models.Model):
    firm_name = models.CharField(max_length=200)

    def __str__(self):
        return self.firm_name
    class Meta:
        verbose_name_plural = "3. Add Firm"

    

    


class BillCategory(models.Model):
    CATEGORIES = [('SL','SALE'),
                ('PR','PURCHASE')]
    bill_type = models.CharField(max_length=2,choices=CATEGORIES)

    class Meta:
        verbose_name_plural = "-> Bill Category"
    
    def __str__(self):
        return self.get_bill_type_display()

    # def update_bill_category(self):
    






class Bill(DefaultExpenseModel):
    app_label = 'manager_app'
    bill_category = models.ForeignKey(BillCategory,on_delete=models.CASCADE,related_name='bill_category_rel')
    firm_name = models.ForeignKey(Add_Firm,on_delete=models.CASCADE)
   
    benificiary_name = models.ForeignKey(Add_benificiary_name,on_delete=models.CASCADE,related_name='benificiary_bill')
    
    class Meta:
        verbose_name_plural = "->Bills"
        ordering = ['-date_added']

    def __str__(self):
        return str(self.title) + str(self.id)

    def save(self,*args, **kwargs):
        if self.bill_category.bill_type == 'SL':
            self.payment_type = 'CR'
        else:
            self.payment_type = "DR"
        super(Bill,self).save(*args, **kwargs)
        self.benificiary_name.update_benificiary()
    def bill_no(self):
        return str(self.title)
    bill_no.short_description = 'Bill No.'
    def tag_final_value(self):
        
        if self.payment_type=="CR":
            bill_amount_status = "DR"
        else:
            bill_amount_status = 'CR'
        return f'{self.final_value} {bill_amount_status}'
    tag_final_value.short_description = 'Bill Value'
    def tag_paid_value(self):
        return f'{self.paid_value} - {self.payment_type}'

    def tag_category(self):
        return f'{self.bill_category}'

    def get_absolute_url(self):
        return reverse_lazy("manager_app:bills_view")
    def get_admin_url(self):
        return reverse('admin:%s_%s_change'%(self._meta.app_label,self._meta.model_name),args=[self.pk])
        
        # return 'admin/%s/%s/%s/change/'%(self._meta.app_label,self._meta.model_name,self.pk)
    
    @staticmethod
    def benificiary_balance(queryset):
        name_balance = queryset[0].benificiary_name.balance if queryset else 0
        if name_balance >=0:
            status = "DR"
        else:
            status = 'CR'
       
        return f"{name_balance} {status}" if queryset else  " -- "

  
    

    @staticmethod
    def filters_data(request,queryset):
        search_name = request.GET.get('search_name',None)
        start_date = request.GET.get('start_date',None)
        end_date = request.GET.get('end_date',None)
        if not end_date:
            end_date = date.today() 
        
        queryset = queryset.filter(benificiary_name__Benificiary_Name__icontains=search_name) if search_name else queryset
        queryset = queryset.filter(date_added__range = [end_date,start_date]) if (start_date and end_date) else queryset

        return queryset
class PayrollCategory(models.Model):
    PAYROLL_CATEGORIES = [('FL','Factory Labour'),
                            ('SL','Shop Labour'),
                            ('LL',"Loading Labour")] 
    category = models.CharField(max_length=2,choices=PAYROLL_CATEGORIES)

    def __str__(self):
        return self.get_category_display()



class Person(models.Model):
    Name = models.CharField(unique=True,max_length=100)
    work_type = models.ForeignKey(PayrollCategory,on_delete = models.CASCADE)
    # amont_paid = models.DecimalField(default=0,decimal_places=0,max_digits=20)
    phone = models.CharField(max_length=10,blank=True,null=True)
    balance = models.DecimalField(default=0,max_digits=20,decimal_places=0)

    class Meta:
        verbose_name_plural = "-> Person"
    
    def __str__(self):
        return self.Name
    def tag_balance(self):
        return f'{self.balance} Rs'

    def update_person(self):
        queryset = self.person_payroll.all()
        total_value = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset else 0
        paid_value = queryset.aggregate(Sum('paid_value'))['paid_value__sum'] if queryset else 0
        print(paid_value)
        self.balance = total_value - paid_value
        self.save()



class Payroll(DefaultExpenseModel):
    person = models.ForeignKey(Person,null=True,on_delete=models.SET_NULL,related_name = "person_payroll")
    # category = models.ForeignKey(PayrollCategory,null=True,on_delete=models.SET_NULL,related_name="category_payroll")
    firm_name = models.ForeignKey(Add_Firm,on_delete=models.CASCADE,related_name = 'payroll_firm',null=True)

    class Meta:
        verbose_name_plural = "-> Payroll"
        ordering = ['-date_added']

    def save(self,*args, **kwargs):
        super(Payroll,self).save(*args,**kwargs)
        self.person.update_person()
  
        
    def tag_category(self):
        return f"{self.person} - {self.category}"
    

class GenericExpenseCategory(models.Model):
    CHOICES = [('HE','House Expense'),
                ('FE','Factory Expense'),
                ('SE','Shop Expense'),
                ('ME','Miscellaneous Expense')]
    category = models.CharField(max_length=2,choices=CHOICES)
    total_amount = models.DecimalField(max_digits=20,decimal_places=0,default=0)
    class Meta:
        verbose_name_plural = "-> General Expenses"

    def __str__(self):
        return self.get_category_display()

    def total_amount(self):
        return f"{total_amount} Rs"
    total_amount.short_description = "Total Amount"

    def update_category(self):
        queryset = self.category_expenses.all()
        self.total_amount = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset else 0
        self.save()




class GenericExpense(DefaultExpenseModel):
    category = models.ForeignKey(GenericExpenseCategory,on_delete=models.CASCADE,related_name='category_expenses')
    firm_name = models.ForeignKey(Add_Firm,on_delete=models.CASCADE,related_name = 'firm_expense_rel')

    class Meta:
        verbose_name_plural = "-> Generic Expense"
        ordering = ['-date_added']
      
       
    def save(self,*args, **kwargs):
        self.is_paid = True
        self.payment_update_date = self .date_added
        self.payment_type = "CR"
        self.paid_value = self.final_value

        if not self.title:
            self.title = f'{self.category} - {self.id}'
        super(GenericExpense,self).save(*args,**kwargs)
        self.category.update_category()
    def tag_category(self):
        return f"{self.category}"

    @staticmethod
    def filters_data(request,queryset):
        cate_name = request.GET.getlist('cate_name',None)
        # cate_name = GenericExpenseCategory.CHOICES[cate_name] if GenericExpenseCategory.CHOICES[cate_name] else cate_name
        start_date = request.GET.get('start_date',None)
        end_date = request.GET.get('end_date',None)
        if not end_date:
            end_date = date.today() 
        cate_name = cate_name[0] if any(cate_name) else None
        if cate_name == " ":
            cate_name = None
        queryset = queryset.filter(category__category__icontains=cate_name) if cate_name else queryset
        queryset = queryset.filter(date_added__range = [end_date,start_date]) if (start_date and end_date) else queryset
        return queryset

    def get_absolute_url(self):
        return reverse_lazy("manager_app:expense_list")
    
        
