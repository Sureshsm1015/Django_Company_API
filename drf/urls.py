from django.urls import path
from .import views



urlpatterns = [
    path('companies/', views.company_list, name='company_list'),
    path('companies/add/', views.add_company, name='add_company'),
    path('companies/<str:location_name>/', views.company_list_by_location, name='company_list_by_location'),  # URL for filtering companies by location
    path('companies/edit/<int:company_id>/', views.edit_company, name='edit_company'),
    path('company/delete/<int:company_id>/', views.delete_company, name='delete_company'),


    path('companiesjson/',views.companies_list,name='companies_list'),
    path('companiesaddjson/',views.companies_add,name='add_companies_add'),
    path('companiesjson/<int:pk>/', views.companies_details, name='companies_details'),


    path('employee/', views.employee_list, name='employee_list'),
    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/<str:Address_name>/', views.employee_list_by_location, name='employee_list_by_location'),
    path('employee/edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('employee/delete/<int:id>/', views.delete_employee, name='delete_employee'),

    path('employeejson/', views.employee_list1, name='employee_list1'),
    path('employee/addjson/', views.employee_add, name='employee_add'),
    path('employeejson/<int:pk>/', views.employee_details, name='employee_details'),

    path('companies/<int:company_id>/employee/',views.company_employees),

]
