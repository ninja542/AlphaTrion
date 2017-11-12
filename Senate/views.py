from django.shortcuts import render
from .models import Senator, Minutes
from .forms import MinutesForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

def senate_home(request):
	"""
	The home view for the senate page

	**Context**
	''senator_list''
		List of all senators
	
	**Template:**
	:template:'senate-home.html'

	"""
	senator_list = Senator.objects.all()
	return render(request, 'senate-home.html', {'senator_list': senator_list})

def senate_constitution(request):
	return render(request, 'senate-constitution.html')

def minutes(request):
	minutes_list = Minutes.objects.all()
	return render(request, 'minutes.html', {'minutes': minutes_list})


@login_required
@user_passes_test(lambda u: u.groups.filter(name="Senators").exists(), login_url='/accounts/login')
def add_minutes(request):
	"""
	View to add minutes to the minute database

	**Context**
	''form''
		add minutes model form
	
	**Template:**
	:template:'add-minutes.html'

	"""
	user = request.user

	if request.method == "POST":
		minutes = MinutesForm(request.POST)
		if minutes.is_valid(): 
			minutes.save() 
			return HttpResponseRedirect(reverse('senate-minutes-home', current_app='Senate'))
	
	else:
		minutes = MinutesForm()

	return render(request, 'add-minutes.html', {'form': minutes})


@login_required
@user_passes_test(lambda u: u.groups.filter(name="Senators").exists(), login_url='/accounts/login')
def delete_minutes(request, minuteid):
	"""
	View to delete minutes from the minute database
	
	**Template:**
	:template:'minutes.html'
	
	"""
	minute = get_object_or_404(Minutes, pk=minuteid)
	minute.delete()
	return HttpResponseRedirect(reverse('senate-minutes-home', current_app='Senate'))