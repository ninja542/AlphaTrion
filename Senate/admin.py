from django.contrib import admin
from .models import Senator


@admin.register(Senator)
class SenatorAdmin(admin.ModelAdmin):
	model = Senator