from django.contrib import admin
from .models import Senator, Minutes


@admin.register(Senator)
class SenatorAdmin(admin.ModelAdmin):
	model = Senator

	
@admin.register(Minutes)
class SenatorAdmin(admin.ModelAdmin):
	model = Minutes