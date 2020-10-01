from django.contrib import admin
from manager_app.models import *
# Register your models here.

admin.site.register(Payment_Method)
# admin.site.register(DefaultExpenseModel)
# admin.site.register(Bill)
admin.site.register(BillCategory)
admin.site.register(Add_Firm)
#admin.site.register(Add_benificiary_name)
admin.site.register(PayrollCategory)
# admin.site.register(Person)
admin.site.register(GenericExpenseCategory)
admin.site.register(Payroll)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['Name','work_type','phone','tag_balance',]
    fields = ['Name','phone']
    search_fields = ['Name','phone']

@admin.register(GenericExpense)
class GenericExpenseAdmin(admin.ModelAdmin):
    list_display = ['title','date_added', "final_value",'category','is_paid' ]                 

@admin.register(Bill)
class AdminBill(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ['date_added','bill_category','benificiary_name','bill_no','firm_name','final_value','paid_value','is_paid','payment_method']      
    list_filter = ['benificiary_name','firm_name','is_paid','date_added','title'] 
    # search_fields = ['benificiary_name__Benificiary_Name__search']
   
    search_fields = ['title']
   # actions = [action_paid,]                                           

@admin.register(Add_benificiary_name)
class AdminAdd_benificiary_name(admin.ModelAdmin):
    list_display = ['Benificiary_Name','tag_balance']
  #list_filter = ['date_added',]
    search_fields = ['Benificiary_Name']