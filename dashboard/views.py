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
from patients.models import CreatePatientIdTable

class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    appts = []

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

        patient_details = PatientEndpoint(access_token).get_patients(doctor['id'])
        patient_details = CreatePatientIdTable(patient_details)

        appts = AppointmentEndpoint(access_token).get_appoinments(doctor['id'], datetime.now())
        models.CreateTemplateIdTable(appts, patient_details)
        appts = models.GetTemplateIdTable()

        return patient_details, appts
    '''
    def get_context_data(self, **kwargs):
        print("!!!!Get context data")
        kwargs = super(DashboardView, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        patient_details, appointment_details = self.make_api_request()

        kwargs['patients'] = patient_details
        kwargs['appointment'] = appointment_details

        return kwargs
    '''
    def get(self, request):
        access_token = self.request.session.get('access_token')
        a = AppointmentEndpoint(access_token)
        if request.method == 'GET':
            appts = models.GetTemplateIdTable()
            data = appts
            print(data)
            if data == None:
                return JsonResponse({"data": None})
            context = {
                'appointment': data,
            }
            return render(request, 'dashboard.html', context)
        else:
            return JsonResponse({"data": data})

    def post(self, request):
        access_token = self.request.session.get('access_token')
        a = AppointmentEndpoint(access_token)

        if request.method == 'POST':
            request_data = json.loads(request.body)
            appointment_id = request_data.get("id")
            status = request_data.get("status")
            print(appointment_id, status)

            models.AdjustAppointment(appointment_id, status)

            # Update dictionsry with these items
            data = {
                'status': status
            }
            try:
                # Just to fill space
                a = 0
            except APIException:
                return JsonResponse({"status": "false"}, status=500)

        return JsonResponse({"status": "true"})
 