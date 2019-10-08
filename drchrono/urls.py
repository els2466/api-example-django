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
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^checkin/$', DashboardView.as_view(), name='checkin'),
    url(r'^patients/$', PatientsView.as_view(), name='patients'),
]
