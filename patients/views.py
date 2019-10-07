# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from social_django.models import UserSocialAuth
from django.http import JsonResponse
from .models import *
from drchrono.endpoints import DoctorEndpoint, AppointmentEndpoint, PatientEndpoint, APIException
import datetime
import pytz
import json
from datetime import datetime, timedelta

import models

class PatientsView(TemplateView):
    template_name = 'list_patients.html'

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

        doctor = self.request.session['doctor']
        patients = PatientEndpoint(access_token).get_patients(doctor['id'])

        return patients

    def get_context_data(self, **kwargs):
        kwargs = super(PatientsView, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        patient_details = self.make_api_request()
        kwargs['patient'] = patient_details

        return kwargs
