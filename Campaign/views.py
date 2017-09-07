from django.shortcuts import render
from .models import campaign_section

# Create your views here.
def home_view(request):
	campaign_sections = campaign_section.objects.all()
	return render(request, 'campaign-home.html', {'campaign_sections': campaign_sections})
def personal_statement_view(request):
	return render(request, 'personal_statement.html')
def planned_policies_view(request):
	return render(request, 'planned_polocies.html')