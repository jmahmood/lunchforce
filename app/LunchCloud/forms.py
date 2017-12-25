import logging

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from LunchCloud.models import FoodOption, IntroductionCode
import gettext

_ = gettext.gettext


class RegistrationForm(forms.Form):
    invitation_code = forms.CharField(max_length=50, widget=forms.HiddenInput)
    email = forms.EmailField()
    foods = forms.ModelMultipleChoiceField(queryset=FoodOption.objects.filter(enabled=True))

    def clean(self) -> dict:
        cleaned_data = super().clean()
        ic = IntroductionCode.objects.filter(code=cleaned_data.get('invitation_code')).filter(used=False)
        if ic.count() == 0:
            raise forms.ValidationError('Invalid Invitation code')

        return cleaned_data


class AvailabilityForm(forms.Form):
    frm = forms.DateTimeField()
    until = forms.DateTimeField()

    def clean(self) -> dict:
        cleaned_data = super().clean()
        frm_datetime = cleaned_data.get('frm')
        until_datetime = cleaned_data.get('until')

        if until_datetime < frm_datetime:
            raise forms.ValidationError('The From datetime must be before the until datetime')

        return cleaned_data


class EmailAuthenticationForm(forms.Form):
    inputEmail = forms.EmailField(label=_("Email"))
    inputPassword = forms.CharField(label=_("Password"),
                                    strip=False,
                                    widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        # Default backend: import django.contrib.auth.backends.ModelBackend
        super().clean()

        email = self.cleaned_data.get('inputEmail')
        password = self.cleaned_data.get('inputPassword')

        logging.warning(email)
        logging.warning(password)

        if email and password:
            self.user_cache = authenticate(username=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    AuthenticationForm.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': 'Email'},
                )
            else:
                self.confirm_login_allowed()

        return self.cleaned_data

    def confirm_login_allowed(self):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not self.user_cache.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
