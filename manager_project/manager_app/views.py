from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from manager_app.forms import *
from django.views.generic import TemplateView,CreateView, DetailView,ListView
from manager_app.models import *

CURRENCY = "Rs"
# Create your views here.


class HomeView(LRM,TemplateView):
    login_url = '/login/'
    template_name = 'home.html'
    
    def get_context_data(self,**kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        bills = Bill.my_query.get_queryset()[:20]
        payrolls = Payroll.my_query.get_queryset()[:20]
        expenses = GenericExpense.my_query.get_queryset()[:20]
        context.update({'bills': bills,
                        'payroll':payrolls,
                        'expenses':expenses})
        return context


class CreateBillView(LRM,CreateView):
    login_url = "/login/"
    template_name = 'bill_create.html'
    redirect_url_name = 'manager_app/page_list.html'
    form_class = BillForm
    model = Bill
    
class CreateExpenseView(LRM,CreateView):
    login_url = '/login/'
    template_name = 'expense_create.html'
    redirect_url_name = 'manager_app/expense_list.html'
    form_class = GenericExpenseForm
    model = GenericExpense

    
class BillDetailView(LRM, DetailView):
    login_url = '/login/'
    model = Bill
  

class GeneralExpenseView(LRM, ListView):
    login_url = '/login/'
    model = GenericExpense
    template_name = 'expense_list.html'
    paginate_by = 40

    def get_queryset(self):
        queryset = GenericExpense.objects.all()
        queryset = GenericExpense.filters_data(self.request,queryset)
        return queryset
    def get_context_data(self,**kwargs):
        context = super(GeneralExpenseView,self).get_context_data(**kwargs)
        page_title = 'Expense List'
        categories = GenericExpenseCategory.objects.all()
        cate_name, start_date, end_date  = [self.request.GET.get('cate_name',None),
                                            self.request.GET.get('start_date',None),
                                            self.request.GET.get('end_date',None)]
        
        total_value, total_paid_value, diff = GenericExpense.analysis(self.object_list)
        context.update(locals())
        return context
        

    

class BillListView(LRM,ListView):
    login_url = '/login/'

    model = Bill
    template_name = 'page_list.html'
    paginate_by = 30

    # def get_context_data(self,**kwargs):
    #     context = super(BillListView,self).get_context_data(**kwargs)
    #     page_titl= "Bill List"
    #     categories = BillCategory.objects.all()
    #     total_value, paid_value, diff = Bill.analysis(self.object_list)
    #     currency = CURRENCY
    #     context.update(locals())
    #     return context

    def get_queryset(self):
        queryset = Bill.objects.all()
        # custom filter analysis
        queryset = Bill.filters_data(self.request, queryset)
        

        # simple date filter
        # queryset =  queryset.filter(date_added__lte=timezone.now()).order_by('-date_added')
        return queryset

    def get_context_data(self,**kwargs):
        context = super(BillListView,self).get_context_data(**kwargs)
        page_title = "Bills List"
        categories = BillCategory.objects.all()
        search_name, start_date, end_date = [self.request.GET.get('search_name',None),
                                            self.request.GET.get('start_date',None),
                                            self.request.GET.get('end_date',None),
                                            ]


       
        total_value,total_paid_value,diff = Bill.analysis(self.object_list)
        benif_bal = Bill.benificiary_balance(self.object_list)
        currency = CURRENCY
        context.update(locals())
        return context

class AddBenificiaryView(LRM,CreateView):
    login_url = '/login/'
    template_name = 'add_benif.html'
    redirect_url_name = 'manager_app/add_benif.html'
    form_class = BenificiaryForm
    model = Add_benificiary_name

class AddPayrollView(LRM,CreateView):
    login_url = '/login/'
    template_name = 'add_payroll.html'
    redirect_url_name = 'manager_app/home.html'
    form_class = PayrollForm
    model = Payroll

class BenificiaryListView(LRM,ListView):
    login_url = '/login/'
    template_name = 'benificiary_list.html'
    model = Add_benificiary_name

    def get_context_data(self,**kwargs):
        context = super(BenificiaryListView,self).get_context_data(**kwargs)

        search_name = self.request.GET.get('search_name',None)
        context.update(locals())
        return context
    def get_queryset(self):
        queryset = Add_benificiary_name.objects.all()
        # custom filter analysis
        queryset = Add_benificiary_name.filters_data(self.request, queryset)
        

        # simple date filter
        # queryset =  queryset.filter(date_added__lte=timezone.now()).order_by('-date_added')
        return queryset