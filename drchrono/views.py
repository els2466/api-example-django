from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import *
from social_django.models import UserSocialAuth
from django.http import JsonResponse
from .models import *
from drchrono.endpoints import DoctorEndpoint, AppointmentEndpoint, PatientEndpoint, APIException
import datetime
import pytz
import json
from datetime import datetime, timedelta
from patients.models import CreatePatientIdTable
from dashboard.models import CreateTemplateIdTable, GetTemplateIdTable


class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    template_name = 'kiosk_setup.html'


class DoctorWelcome(TemplateView):
    """
    The doctor can see what appointments they have today.
    """
    template_name = 'doctor_welcome.html'

    def get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
        already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token

    def make_api_request(self):
        """
        Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've
        proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use it to fetch details
        access_token = self.get_token()
        self.request.session['access_token'] = access_token

        doctor = DoctorEndpoint(access_token).get_doctor()
        self.request.session['doctor'] = doctor
        # Grab the first doctor from the list; normally this would be the whole practice group, but your hackathon
        # account probably only has one doctor in it.
        #doctor = DoctorEndpoint(access_token).get_doctor()
        #self.request.session['doctor'] = doctor.id

        # I don't think I want to get patient info here.
        patient_details = PatientEndpoint(access_token).get_patients(doctor['id'])
        patient_details = CreatePatientIdTable(patient_details)
        appts = AppointmentEndpoint(access_token).get_appoinments(doctor['id'], datetime.now())
        # Get patients and appointments for the doctor and store it in the local DB
        CreateTemplateIdTable(appts, patient_details)
        appts = GetTemplateIdTable()

        return doctor

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        doctor_details = self.make_api_request()
        kwargs['doctor'] = doctor_details
        return kwargs
