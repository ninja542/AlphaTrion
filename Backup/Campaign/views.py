from django.shortcuts import render

def personal_statement_view(request):
	return render(request, 'personal_statement.html')
def planned_policies_view(request):
	return render(request, 'planned_polocies.html')