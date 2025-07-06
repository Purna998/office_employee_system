from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from .models import Employee, Department, Role
from datetime import datetime
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request,'index.html')

def all_emp(request):
    emps=Employee.objects.all()
    context={
        'emps':emps
    }
    print(context)
    return render(request,'all_emp.html',context)

@csrf_protect
def add_emp(request):
    if request.method == 'POST':
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        location=request.POST['location']
        salary=int(request.POST['salary'])
        bonus=int(request.POST['bonus'])
        department_id=int(request.POST['department'])
        role_id=int(request.POST['role'])
        
        # Get the actual instances
        department = Department.objects.get(id=department_id)
        role = Role.objects.get(id=role_id)
        
        
        
        new_emp=Employee(
            first_name=first_name,
            last_name=last_name,
            dept=department,  # Use 'dept' not 'department'
            salary=salary,
            bonus=bonus,
            role=role,
            hire_date=datetime.now().date()  # Use 'hire_date' not 'hiredate'
        )
        new_emp.save()
        return HttpResponse("Employee added successfully")
    
    elif request.method=='GET':
        # Pass departments and roles to template
        departments = Department.objects.all()
        roles = Role.objects.all()
        context = {
            'departments': departments,
            'roles': roles
        }
        return render(request,'add_emp.html', context)
        
    else:
        return HttpResponse("An exception occured!")

def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed=Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully")
        except: 
            return HttpResponse("Employee Enter a valid Emp ID")
    emps=Employee.objects.all()
    context={
            'emps':emps,
    }
        
    return render(request,'remove_emp.html',context)
        
    
    
    

def filter_emp(request):
    if request.method=='POST':
        name=request.POST.get('name')
        dept=request.POST.get('dept')
        role=request.POST.get('role')
        emps=Employee.objects.all()
        
        if name:
            emps=emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps=emps.filter(dept__name__icontains=dept)
        if role:
            emps=emps.filter(role__name__icontains=role)
            
        context={
            'emps':emps,
        }
        
        return render(request,'all_emp.html',context)
    elif request.method=='GET':
        return render(request,'filter_emp.html')
    else:
        return HttpResponse("An exception occured!")
    