# scanner/admin.py
from django.contrib import admin
from .models import Target, Vulnerability

admin.site.register(Target)
admin.site.register(Vulnerability)
