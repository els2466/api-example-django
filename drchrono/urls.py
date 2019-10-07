from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView
from django.contrib import admin
admin.autodiscover()

import views
from patients.views import PatientsView
from dashboard.views import DashboardView


urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorWelcome.as_view(), name='welcome'),
    #url(r'^complete/drchrono/$', DashboardView.as_view(), name='dashboard'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^analytics/$', views.AnalyticsView.as_view(), name='analytics'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    #url(r'^checkin/$', views.CheckinView.as_view(), name='checkin'),
    url(r'^checkin/$', DashboardView.as_view(), name='checkin'),
    url(r'^patients/$', PatientsView.as_view(), name='patients'),
]

'''
Patient Schedule wants to access your data:

Create and modify patient lab orders and results.
View billing information.
View detailed patient information.
Edit select account information, such as creating new exam rooms.
Create and modify messages in your message center.
Modify patient payment information
Create and modify tasks in your tasks center
Create new patients and set their name, chart_id, age, and gender.
Create and modify clinical information, such as vitals, clinical notes, medications and diagnoses.
View your basic information.
View tasks in your tasks center
View patient payment information
View summary information about your patients. This includes patients' name, chart_id, age, and gender.
View patient lab orders and results.
View resources that requires Settings permission, such as custom fields.
Modify billing information.
Schedule appointments and modify the data associated with them.
View messages in your message center.
View clinical information, such as vitals, clinical notes, medications and diagnoses.
Create resources that requires Settings permission, such as custom fields.
Create patients and modify detailed patient information.
View your appointments.
Patient Schedule
This app is in test mode.
'''
