from django import forms

from LunchCloud.models import FoodType, InvitationCode


class RegistrationForm(forms.Form):
    invitation_code = forms.CharField(max_length=50, widget=forms.HiddenInput)
    email = forms.EmailField()
    foods = forms.ModelMultipleChoiceField(queryset=FoodType.objects.filter(enabled=True))

    def clean(self) -> dict:
        cleaned_data = super().clean()
        ic = InvitationCode.objects.filter(code=cleaned_data).filter(used=False)
        if ic.count() == 0:
            raise forms.ValidationError('Invalid Invitation code')

        return cleaned_data


class Availability(forms.Form):
    def clean(self) -> dict:
        cleaned_data = super().clean()
        frm_datetime = cleaned_data.get('frm')
        until_datetime = cleaned_data.get('until')

        if until_datetime < frm_datetime:
            raise forms.ValidationError('The From datetime must be before the until datetime')

        return cleaned_data
