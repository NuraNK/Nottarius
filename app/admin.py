# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.
from app.models import *

admin.site.register(
    [Department, Position, Discount, Employee, Services, Client, Appointment, Operation]
)
