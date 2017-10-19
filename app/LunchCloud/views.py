# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
import django.views.generic

import LunchCloud.forms

# from app.LunchCloud.forms import RegistrationForm
from LunchCloud.models import Profile, InvitationCode


def create_account(form_data:dict) -> (InvitationCode, Profile):
    ic = InvitationCode.objects.get(code=form_data.get('invitation_code'))

    prf: Profile = Profile(
        email=form_data.get('email'),
        blacklist=form_data.get('foods'),
        invited_by=ic.invited_by
    )
    return ic, prf


def enrollment(request: HttpRequest) -> HttpResponse:
    """
    User creates account and enrolls for system.

    :param request:
    :return:
    """
    frm:LunchCloud.forms.RegistrationForm

    if request.method == 'POST':
        frm = LunchCloud.forms.RegistrationForm(request.POST)

    if request.method == 'GET':
        frm = LunchCloud.forms.RegistrationForm({"invited_by":request.GET.get('invited_by', None)})

    if frm.is_valid():
        ic, prf = create_account(frm.cleaned_data)
        ic.used = True
        ic.save()
        prf.save()

        return redirect('my-dashboard', enrollment=True, profile=prf.pk)
    print(repr(frm))
    return render(
        request, 'enrollment.html', {'frm': frm}
    )

    pass
