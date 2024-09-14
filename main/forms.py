from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Bus, Record


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ["username", "password1"]

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""
        self.fields["username"].help_text = ""  # Remove help text for password1


class CustomUserAuthenticationForm(AuthenticationForm):
    class Meta(AuthenticationForm):
        model = CustomUser
        fields = ["username", "password"]


class BusRegisterForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BusRegisterForm, self).__init__(*args, **kwargs)
        self.fields["conductor"].queryset = CustomUser.objects.filter(
            usertype="conductor"
        )


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["income", "expense", "date"]

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "text",
                "class": "datepicker",
                "placeholder": "Pick a date",
            },
            format="%d/%m/%Y",
        ),
        input_formats=["%d/%m/%Y"],
    )
