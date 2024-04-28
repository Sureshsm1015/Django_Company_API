from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import company,employee
from .serializers import companySerializer,employeeSerializer
from rest_framework import status
from django.contrib import messages 
from django.views.decorators.csrf import csrf_exempt
from .forms import CompanyForm
from django.http import HttpResponseRedirect
from django.db.models import Q



#this is for the html form data
def company_list(request):
    if request.method == 'GET':
        companies = company.objects.all()
        return render(request, 'company_list.html', {'companies':companies})

def company_list_by_location(request, location_name):
    companies = company.objects.filter(location=location_name)
    return render(request, 'company_list.html', {'companies': companies})     

def add_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        about = request.POST.get('about')
        type = request.POST.get('type')
        added_Date = request.POST.get('added_Date')  # Retrieve date from form

        #check if a company with the same name alredy exists
        existing_company = company.objects.filter(name=name)
        if existing_company.exists():
            messages.error(request,f"company with name'{name}' already exists.")
            return render(request, 'add_company.html')  # Render the add_company page again
        
        # if the company doesn't exist, proceed with saving the new company
        serializer = companySerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request,f"Company '{name}' added successfully.")
            return redirect('company_list')  # redirect to add_company view
        else:
            messages.error(request,"Error:fill the form")
            return render(request, 'add_company.html', {'serializer': serializer})
    else:
        return render(request, 'add_company.html')

def edit_company(request, company_id):
    company_instance = get_object_or_404(company, pk=company_id)
    companies = company.objects.all() 
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully.')
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company_instance,initial={'added_Date': company_instance.added_Date})
    
    return render(request, 'edit_company.html', {'form': form})
    

from django.utils import timezone


    # company = Company.objects.get(pk=company_id)
    
# def delete_company(request, id):
#     comp = company.objects.get(id=id)
#     comp.delete()
#     return redirect('company_list')

def delete_company(request, company_id):  
    print("Delete function called with company_id:", company_id)
    try:
        comp = company.objects.get(id=company_id)  
        print("Company object found:", comp)
        comp.delete()
        print("Company deleted successfully")
    except company.DoesNotExist:
        print("Company does not exist")
    return redirect('company_list')
###############################################################################################
#this is for the json formate data in django rest framework

# class CompanyViewSet(viewsets.ModelViewSet):
#     queryset = company.objects.all()
#     serializer_class = companySerializer

@csrf_exempt
@api_view(['GET'])
def companies_list(request):
    if request.method == 'GET':
        companies1 = company.objects.all()
        serializer = companySerializer(companies1,many=True)
        return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def companies_add(request):
        serializer = companySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            company_data = serializer.data
            company_name = company_data.get('name')
            company_place = company_data.get('location')
            message = f"The complany {company_name}-{company_place} was added successfully."
            return Response({'message':message,'data':company_data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def companies_details(request,pk):
    try:
        company_instance = company.objects.get(pk=pk)
    except company.DoesNotExist:
        return Response({'error':'company not found'},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = companySerializer(company_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        company_name = company_instance.name  # Fetch company name
        serializer = companySerializer(company_instance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':  f'Company {company_name} updated successfully', 'data': serializer.data})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        company_name = company_instance.name  # Fetch company name
        company_instance.delete()
        return Response({'message': f'Company {company_name} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
##########################################################################################################################################
# for the employees
# it is for the render page

@csrf_exempt
@api_view(['GET'])
def employee_list(request):
    if request.method == 'GET':
        employees = employee.objects.all()
        return render(request, 'employee_list.html', {'employees':employees})

def employee_list_by_location(request, Address_name):
    employees = employee.objects.filter(address=Address_name)
    return render(request, 'employee_list.html', {'employees': employees})

from django.forms.models import model_to_dict
from django.urls import reverse


def add_employee(request):
    companies = company.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Check if an employee with the same email already exists
        existing_employee = employee.objects.filter(email=email)
        if existing_employee.exists():
            messages.error(request, f"Employee with this email '{email}' already exists.")
            return render(request, 'add_employee.html', {'companies': companies})

        # If the employee doesn't exist, proceed with saving the new employee
        serializer = employeeSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, f"Employee added successfully.")
            return HttpResponseRedirect(reverse('employee_list') + '?success=true')
        else:
            print("Errors during form validation:", serializer.errors)
            messages.error(request, "Error: employee could not be added.")
            return render(request, 'add_employee.html', {'companies': companies, 'serializer': serializer})
    else:
        return render(request, 'add_employee.html', {'companies': companies})

from .forms import EmployeeForm 

def edit_employee(request, id):
    employee_instance = get_object_or_404(employee, id=id)
    companies = company.objects.all()

    if request.method == 'POST':
        # Update the employee details
        employee_instance.name = request.POST.get('name')
        employee_instance.email = request.POST.get('email')
        employee_instance.address = request.POST.get('address')
        employee_instance.phone_no = request.POST.get('phone_no')
        employee_instance.position = request.POST.get('position')
        employee_instance.salary = request.POST.get('salary')

        company_id = request.POST.get('company')  # Assuming the name of the input field is 'company'
        company_instance = get_object_or_404(company, id=company_id)
        employee_instance.company = company_instance
        # Update other fields similarly
        
        employee_instance.save()
        messages.success(request, 'Employee updated successfully.')
        return redirect('employee_list')  # Redirect to the employee list page
    
    return render(request, 'edit_employee.html', {'employee': employee_instance, 'companies': companies})

def delete_employee(request, id):
    emp=employee.objects.get(id=id)
    emp.delete()
    messages.success(request, 'Employee deleted successfully.')
    return redirect('employee_list') 
################################################################
#this is for json data
@csrf_exempt
@api_view(['GET'])
def employee_list1(request):
    if request.method == 'GET':
        employee1 = employee.objects.all()
        serializer = employeeSerializer(employee1,many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def employee_add(request):
        serializer = employeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            employee_data = serializer.data
            employee_name = employee_data.get('name')
            employee_position = employee_data.get('position')
            message = f"The employee {employee_name}-{employee_position} was added successfully."
            return Response({'message':message,'data':company_data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def employee_details(request,id):
    try:
        employee_instance = employee.objects.get(pk=id)
    except employee.DoesNotExist:
        return Response({'error':'employee not found'},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = employeeSerializer(employee_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        employee_name = employee_instance.name  # Fetch company name
        serializer = employeeSerializer(employee_instance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':  f'employee {employee_name} updated successfully', 'data': serializer.data})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employee_name = employee_instance.name  # Fetch company name
        employee_instance.delete()
        return Response({'message': f'employee {employee_name} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
##############################################################################
#to get employess who working specified companies

@api_view(['GET'])
def company_employees(request,company_id):
    try:
        company_instance = company.objects.get(pk=company_id)
    except company.DoesNotExist:
        return Response({'error':'company employee is not found'},status=status.HTTP_404_NOT_FOUND)
    
    #retrieve employees that are the company
    employees=employee.objects.filter(company=company_instance)
    serializer = employeeSerializer(employees,many=True)
    return Response(serializer.data)


