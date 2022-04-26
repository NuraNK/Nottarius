# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, default='')
    salary = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=255)
    percent = models.FloatField()

    def __str__(self):
        return self.name


class Employee(models.Model):
    fio = models.CharField(max_length=255, default='')
    position = models.ForeignKey(Position, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.fio


class Services(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Client(models.Model):
    fio = models.CharField(max_length=255, default='')
    passport = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=255, default='')
    discount = models.ForeignKey(Discount, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.fio


class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ['client', 'date']

    def __str__(self):
        return self.client.fio


class Operation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_mime_type = models.CharField(max_length=100)
    file_size = models.IntegerField()
    file_hash = models.CharField(max_length=66)
    previous_hash = models.CharField(max_length=255, default="")

