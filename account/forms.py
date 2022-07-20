from wsgiref.validate import validator
from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re


def usr_name(value):
	pattern = re.compile("^[a-zA-Z]{3,}$")
	#"^[A-Za-z]\\w{5, 29}$"
	if  len(value)>30 or len(value)<=5:
		raise ValidationError("Min 5 and Max 12 Characters")
	if not pattern.match(value):
		raise ValidationError("Only Alphabets")
		
def rest_name(value):
	pattern = re.compile("^[a-zA-Z]{3,}$")
	#"^[A-Za-z]\\w{5, 29}$"
	if  len(value)>30 or len(value)<=2:
		raise ValidationError("Min 2 and Max 12 Characters")
	if not pattern.match(value):
		raise ValidationError("Only Alphabets and min 6 and max 30 Charcters")


def passw(value):
	if validate_password(value):
		raise ValidationError("Min 8 Charracters")

def mobile(value):
  if len(value) < 10 or not value.isdigit() or len(value)>12:
    raise ValidationError("Invalid Mobile")

# creating a form
# class CustomerSignUpForm(forms.ModelForm):
# 	username = forms.CharField(initial = "username",max_length = 12,validators=[usr_name])
# 	password = forms.CharField(widget=forms.PasswordInput,validators=[passw])
# 	email	 = forms.CharField(required=True)
	

