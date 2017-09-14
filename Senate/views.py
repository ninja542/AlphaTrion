from django.shortcuts import render

def senate_home(request):
	return render(request, 'senate-home.html')

def senate_constitution(request):
	return render(request, 'senate-constitution.html')