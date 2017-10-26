# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import RedirectView

import LunchCloud.forms
from LunchCloud.models import Profile, InvitationCode


@login_required
def index(request: HttpRequest) -> HttpResponse:
    # This is a simple basic view which is powered by Angular.JS
    # It just displays your upcoming
    pass


def create_account(form_data: dict) -> (InvitationCode, Profile):
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
    frm: LunchCloud.forms.RegistrationForm

    if request.method == 'POST':
        frm = LunchCloud.forms.RegistrationForm(request.POST)

    if request.method == 'GET':
        frm = LunchCloud.forms.RegistrationForm({"invited_by": request.GET.get('invited_by', None)})

    if frm.is_valid():
        ic, prf = create_account(frm.cleaned_data)
        ic.used = True
        ic.save()
        prf.save()

        return redirect('my-dashboard', enrollment=True, profile=prf.pk)

    return render(
        request, 'enrollment.html', {'frm': frm}
    )

    pass


class RedirectLoginView(RedirectView):
    permanent = True
    url = '/account/login/'
