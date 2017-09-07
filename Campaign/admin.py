from django.contrib import admin
from .models import campaign_section
# Register your models here.
@admin.register(campaign_section)
class ViewCampaignAsAdmin(admin.ModelAdmin): 
	model = campaign_section