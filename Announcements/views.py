from django.shortcuts import render
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Announcement
from .forms import AnnouncementForm


def announcements(request):
	"""
	Displays a list of announcements
	
	**Context**
	''Announcements''
		All announcement objects

	**Template:**
	:template:'announcements-home.html'
	"""
	announcements = Announcement.objects.all()
	return render(request, 'announcements-home.html', {'announcements': announcements})


@login_required
@user_passes_test(lambda u: u.groups.filter(name="Senators").exists(), login_url='/accounts/login')
def add_announcement(request):
	"""
	Template to add a announcement
	
	**Context**
	''form''
		Add announcement form

	**Template:**
	:template:'add_announcement.html'
	"""
	if request.method == "POST":
		form = AnnouncementForm(request.POST)

		if form.is_valid():
			form.save()
		return HttpResponseRedirect(reverse('announcements-home', current_app='Announcements'))

	else:
		form = AnnouncementForm()

	return render(request, 'add_announcement.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name="Senators").exists(), login_url='/accounts/login')
def delete_announcement(request, announcementid):
	"""Function call to delete an announcement

	:param announcementid: the id to delete an announcement
	:type announcementid: integer
	"""	
	announcement = get_object_or_404(Announcement, pk=announcementid)
	announcement.delete()
	return HttpResponseRedirect(reverse('announcements-home', current_app='Announcements'))