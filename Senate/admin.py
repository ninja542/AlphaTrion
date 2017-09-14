from django.contrib import admin
from .models import Senator
# Register your models here.
@admin.register(Senator)
class SenatorAdmin(admin.ModelAdmin):
	model = Senator