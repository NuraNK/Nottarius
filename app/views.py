from datetime import datetime
def get_now_date():
    tz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(tz=tz)
    return now

import pdfkit as pdfkit
import pytz
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from hashlib import sha256
from django.http import HttpResponse
from django import template
from django.contrib import messages


from app.models import *
from app.forms import *
from core import settings


@login_required(login_url="/login/")
def index(request):
    cb = Department.objects.all().count()
    cc = Client.objects.all().count()
    cs = Employee.objects.all().count()
    cd = Discount.objects.all().count()
    context = {'segment': 'index', 'cb': cb, 'cc': cc, "cs": cs, 'cd': cd}

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def employee(request):
    list = Employee.objects.all()
    context = {'list': list, 'segment': 'employees'}

    html_template = loader.get_template('employees.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def department(request):
    # list = Department.objects.filter(position__employee=)
    list = Department.objects.all().annotate(
        count=Count("position__employee", distinct=True))
    context = {'list': list, 'segment': 'department'}
    html_template = loader.get_template('department.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def position(request):
    list = Position.objects.all()
    context = {'list': list, 'segment': 'position'}
    html_template = loader.get_template('position.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def discount(request):
    list = Discount.objects.all()
    context = {'list': list, 'segment': 'discount'}
    html_template = loader.get_template('discount.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def client(request):
    list = Client.objects.all()
    context = {'list': list, 'segment': 'client'}
    html_template = loader.get_template('clients.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def service(request):
    list = Services.objects.all()
    context = {'list': list, 'segment': 'service'}
    html_template = loader.get_template('services.html')
    return HttpResponse(html_template.render(context, request))

def service_doc(request,pk):

    now_date = get_now_date().date()
    day = str(now_date.day)
    month = str(now_date.month)
    year = str(now_date.year)


    l = Services.objects.get(pk=pk)
    return render(request, 'doc.html', {'l': l, "day":day, 'month':month,"year":year})


@login_required(login_url="/login/")
def appoinments(request):
    upload = AppoinmentCreate()
    if request.method == 'POST':
        upload = AppoinmentCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('/%2Fappoinments')
        else:
            list = Appointment.objects.all()
            clients = Client.objects.all()

            context = {'list': list, 'client': clients, 'message': "На этот день уже запись есть", 'segment': 'appoint'}
            html_template = loader.get_template('appoinments.html')
            return HttpResponse(html_template.render(context, request))
        return render(request, 'appoinments.html', context)

    list = Appointment.objects.all()
    clients = Client.objects.all()
    context = {'list': list, 'client': clients, 'message': "", 'segment': 'appoint'}
    html_template = loader.get_template('appoinments.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def operations(request):
    list = Operation.objects.all().order_by("-pk")
    context = {'list': list, 'segment': 'operations'}
    html_template = loader.get_template('operations.html')
    return HttpResponse(html_template.render(context, request))


def proof(request):
    if request.method == "POST":
        file = request.FILES['file']
        pk = request.POST.get('pk')
        operation = Operation.objects.get(pk=pk)
        file_hash = sha256(file.read()).hexdigest()
        if operation.file_hash == file_hash:
            messages.success(request, "Файл не изменен")
        else:
            messages.error(request, "Файл изменен, возмжно не тот файл")

        return redirect('operations')


def add_operation(request):
    if request.method == 'POST':
        file = request.FILES['file']
        size = file.size
        name = file.name
        content_type = file.content_type
        employee = request.POST.get('employee')
        client = request.POST.get('client')
        operations = Operation.objects.all().last()
        file_hash = sha256(file.read()).hexdigest()
        if not operations:
            Operation.objects.create(
                file_size=size, file_name=name, file_mime_type=content_type,
                file_hash=file_hash, client_id=client, employees_id=employee,
            )
        else:
            Operation.objects.create(
                file_size=size, file_name=name, file_mime_type=content_type,
                file_hash=file_hash, client_id=client, employees_id=employee, previous_hash=operations.file_hash
            )
        return redirect('operations')
    else:

        clients = Client.objects.all()
        employees = Employee.objects.all()
        context = {
            # "upload_form": upload,
            "action": "Қосу",
            'clients': clients,
            'employees': employees,
        }
        return render(request, 'add-operation.html', context)


def add_employee(request):
    upload = EmployeeCreate()
    if request.method == 'POST':
        upload = EmployeeCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('/%2Femployee')
        else:
            return HttpResponse(
                """your form is wrong, reload on <a href = "{{ url : '/%2Femployee'}}">reload</a>""")
    else:
        list = Position.objects.all()
        context = {
            "upload_form": upload,
            "list": list,
            "action": "Қосу",
            'segment': 'employees'
        }
        return render(request, 'add-employee.html', context)


def add_department(request):
    upload = DepartmentCreate()
    if request.method == 'POST':
        upload = DepartmentCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('/%2Fdepartment')
        else:
            return HttpResponse(
                """your form is wrong, reload on <a href = "{{ url : '/%2Fdepartment'}}">reload</a>""")
    else:
        context = {
            "upload_form": upload,
            "action": "Қосу",
            'segment': 'department'
        }
        return render(request, 'add-department.html', context)


def add_position(request):
    upload = PositionCreate()
    if request.method == 'POST':
        upload = PositionCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('/%2Fposition')
        else:
            return HttpResponse(
                """your form is wrong, reload on <a href = "{{ url : '/%2Fposition'}}">reload</a>""")
    else:
        list = Department.objects.all()
        context = {
            "upload_form": upload,
            "list": list,
            "action": "Қосу",
            'segment': 'position'
        }
        return render(request, 'add-position.html', context)


def add_discount(request):
    upload = DiscountCreate()
    if request.method == 'POST':
        upload = DiscountCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('/%2Fdiscount')
        else:
            return HttpResponse(
                """your form is wrong, reload on <a href = "{{ url : '/%2Fdiscount'}}">reload</a>""")
    else:
        context = {
            "upload_form": upload,
            "action": "Қосу",
            'segment': 'discount'
        }
        return render(request, 'add-discount.html', context)


def add_client(request):
    upload = ClientCreate()
    if request.method == 'POST':
        upload = ClientCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('/%2Fclient')
        else:
            return HttpResponse(
                """your form is wrong, reload on <a href = "{{ url : '/%2Fclient'}}">reload</a>""")
    else:
        list = Discount.objects.all()
        context = {
            "upload_form": upload,
            "list": list,
            "action": "Қосу",
            'segment': 'client'
        }
        return render(request, 'add-client.html', context)


def add_service(request):
    upload = ServiceCreate()
    if request.method == 'POST':
        # with open('1.html', 'r') as r:
        #     r.read()
        create_user_contract_document()
        upload = ServiceCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('/%2Fservice')
        else:
            return HttpResponse(
                """your form is wrong, reload on <a href = "{{ url : '/%2Fservice'}}">reload</a>""")
    else:
        context = {
            "upload_form": upload,
            "action": "Қосу",
            'segment': 'service'
        }
        return render(request, 'add-service.html', context)


@login_required(login_url="/admin-panel/login/")
def update_employee(request, emp_id: int):
    try:
        emp_sel = Employee.objects.get(pk=emp_id)
    except emp_id.DoesNotExist:
        return redirect('/%2Femployee')
    news_form = EmployeeCreate(request.POST, request.FILES or None, instance=emp_sel)
    if news_form.is_valid():
        news_form.save()
        return redirect('/%2Femployee')

    list = Position.objects.all()
    context = {
        "ProductForm": news_form,
        "ProductModel": emp_sel,
        "list": list,
        "action": "Жаңарту",
        'segment': 'employees',
    }
    return render(request, 'add-employee.html', context)


@login_required(login_url="/admin-panel/login/")
def update_department(request, id: int):
    try:
        sel = Department.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('/%2Fdepartment')
    form = DepartmentCreate(request.POST, request.FILES or None, instance=sel)
    if form.is_valid():
        form.save()
        return redirect('/%2Fdepartment')

    context = {
        "ProductForm": form,
        "ProductModel": sel,
        "action": "Жаңарту",
        'segment': 'department'
    }
    return render(request, 'add-department.html', context)


@login_required(login_url="/admin-panel/login/")
def update_position(request, id: int):
    try:
        sel = Position.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('/%2Fposition')
    form = PositionCreate(request.POST, request.FILES or None, instance=sel)
    if form.is_valid():
        form.save()
        return redirect('/%2Fposition')

    list = Department.objects.all()
    context = {
        "ProductForm": form,
        "ProductModel": sel,
        "list": list,
        "action": "Жаңарту",
        'segment': 'position'
    }
    return render(request, 'add-position.html', context)


@login_required(login_url="/admin-panel/login/")
def update_discount(request, id: int):
    try:
        sel = Discount.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('/%2Fdiscount')
    form = DiscountCreate(request.POST, request.FILES or None, instance=sel)
    if form.is_valid():
        form.save()
        return redirect('/%2Fdiscount')

    context = {
        "ProductForm": form,
        "ProductModel": sel,
        "action": "Жаңарту",
        'segment': 'discount'
    }
    return render(request, 'add-discount.html', context)


@login_required(login_url="/admin-panel/login/")
def update_client(request, id: int):
    try:
        sel = Client.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('/%2Fclient')
    form = ClientCreate(request.POST, request.FILES or None, instance=sel)
    if form.is_valid():
        form.save()
        return redirect('/%2Fclient')

    list = Discount.objects.all()
    context = {
        "ProductForm": form,
        "ProductModel": sel,
        "list": list,
        "action": "Жаңарту",
        'segment': 'client'
    }
    return render(request, 'add-client.html', context)


@login_required(login_url="/admin-panel/login/")
def update_service(request, id: int):
    try:
        sel = Services.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('/%2Fservice')
    form = ServiceCreate(request.POST, request.FILES or None, instance=sel)
    if form.is_valid():
        form.save()
        return redirect('/%2Fservice')

    context = {
        "ProductForm": form,
        "ProductModel": sel,
        "action": "Жаңарту",
        'segment': 'service'
    }
    return render(request, 'add-service.html', context)


@login_required(login_url="/admin-panel/login/")
def delete_employee(request, emp_id: int):
    try:
        emp_sel = Employee.objects.get(pk=emp_id)

    except emp_id.DoesNotExist:
        return redirect('/%2Femployee')
    emp_sel.delete()
    return redirect('/%2Femployee')


@login_required(login_url="/admin-panel/login/")
def delete_department(request, id: int):
    try:
        sel = Department.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('/%2Fdepartment')
    sel.delete()
    return redirect('/%2Fdepartment')


@login_required(login_url="/admin-panel/login/")
def delete_position(request, id: int):
    try:
        sel = Position.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('/%2Fposition')
    sel.delete()
    return redirect('/%2Fposition')


@login_required(login_url="/admin-panel/login/")
def delete_discount(request, id: int):
    try:
        sel = Discount.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('/%2Fdiscount')
    sel.delete()
    return redirect('/%2Fdiscount')


@login_required(login_url="/admin-panel/login/")
def delete_client(request, id: int):
    try:
        sel = Client.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('/%2Fclient')
    sel.delete()
    return redirect('/%2Fclient')


@login_required(login_url="/admin-panel/login/")
def delete_service(request, id: int):
    try:
        sel = Services.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('/%2Fservice')
    sel.delete()
    return redirect('/%2Fservice')


@login_required(login_url="/admin-panel/login/")
def delete_app(request, id: int):
    try:
        sel = Appointment.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('/%2Fappoinments')
    sel.delete()
    return redirect('/%2Fappoinments')


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
