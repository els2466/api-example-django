# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create a dictionary associating patient ID with name
def CreatePatientIdTable(patient_details):

    patient_table = {}

    for p in patient_details:
        patient_table.update( {p['id']: [p['first_name'], p['last_name']]} )

    return patient_table
