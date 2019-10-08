# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

appt_list = []

def CreateTemplateIdTable(appts, patient_details):

    # Clear the list
    del appt_list[:]
    appt_id_list = []
    for a in appts:
        if a['patient'] not in appt_id_list:
            appt_id_list.append(a['patient'])
            id = a['patient']
            value_list = patient_details[id]
            a['first_name'] = value_list[0]
            a['last_name'] = value_list[1]

            # Convert dates to something better
            d1 = datetime.datetime.strptime(a['appt_time'],"%Y-%m-%dT%H:%M:%S")
            new_format = "%Y-%m-%d"
            d1.strftime(new_format)

            a['appt_time'] = d1
            # ID tags used in the template
            a['time_id'] = str(id)
            a['select_id'] = 'select_' + str(id)
            a['format_time_id'] = 'format_time_' + str(id)
            appt_list.append(a)

def AdjustAppointment(appointment_id, status):
    if (status == 'Cancelled'):
        for a in appt_list:
            if (a['patient'] == appointment_id):
                appt_list.remove(a)
                break

    else:
        for a in appt_list:
            if (a['patient'] == appointment_id):
                a['status'] = status
                break

def GetTemplateIdTable():
    return appt_list

