from django.conf.urls import url
from manager_app import views
from django.contrib import admin


app_name = 'manager_app'

urlpatterns = [
    
    url(r'^bill_create/$',views.CreateBillView.as_view(),name = 'bill_create'),
    url(r'^bills/$',views.BillListView.as_view(),name='bills_view'),
    url(r'^home/$',views.HomeView.as_view(),name='home'),
    url(r'^expense_list/$',views.GeneralExpenseView.as_view(),name = 'expense_list'),
    url(r'^expense_create/$',views.CreateExpenseView.as_view(),name='expense_create'),
    url(r'add_benificiary/$',views.AddBenificiaryView.as_view(),name='add_benificiary'),
    url(r'add_payroll/$',views.AddPayrollView.as_view(),name='add_payroll'),
    url(r'benificiary_list/$',views.BenificiaryListView.as_view(),name='benificiary_list')
    

]
