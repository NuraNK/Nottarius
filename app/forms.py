from django import forms

from .models import *


class EmployeeCreate(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['fio', 'position', ]


class DepartmentCreate(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', ]


class PositionCreate(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'salary', 'department']


class DiscountCreate(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['name', 'percent']


class ClientCreate(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['fio', 'passport', 'address', 'phone', 'discount']


class ServiceCreate(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name', ]


class AppoinmentCreate(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['client', 'date']
