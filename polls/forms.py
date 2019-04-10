from django.contrib.auth.models import User
from polls.models import UserProfile
from polls.models import practice_area, practice_question, practice_question_input
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext as _
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms.formsets import DELETION_FIELD_NAME
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import ugettext as _, ungettext
import gzip
import os
import re
from django.utils._os import upath
from django.contrib.auth.models import UserManager
from django.utils.six import string_types
from difflib import SequenceMatcher
from django.utils.encoding import force_text
from polls.validators import UserAttributeSimilarityValidator



'''
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['url', 'location', 'company']
'''

#QuestionFormSet = inlineformset_factory(practice_area, practice_question, extra=1)
#InputsFormSet = inlineformset_factory(practice_question, practice_question_input, extra=1)


my_default_errors = {
    'required' : 'Lütfen bu alanı doldurunuz',
    'invalid'  : 'Lütfen geçerli bir değer giriniz'
}

class QuestionInputForm(forms.ModelForm):
    class Meta:
        model  = practice_question_input
        fields = ['input_belong_practice', 'input_text', 'output_text']
        widgets = {'input_belong_practice' : forms.HiddenInput()}

InputFormSet = forms.modelformset_factory(practice_question_input, form=QuestionInputForm, can_delete=True)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = practice_question
        fields = ['practice_discipline', 'question_area_name', 'question_area_text',
                  'question_input_text', 'question_answer_text', 'question_language_field', 'level', 'point']



class QuestionEditForm(forms.ModelForm):
    class Meta:
        model = practice_question
        fields = ['practice_discipline', 'question_area_name', 'question_area_text',
                  'question_input_text', 'question_answer_text', 'question_language_field']
        widgets = {'practice_discipline' : forms.HiddenInput()}
        exclude = ['practice_discipline']



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder' : 'Kullanıcı Adı',
                                                             'class'       : 'form-control'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder' : 'Parola',
                                                             'class'       : 'form-control'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        try:
            User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Kullanıcı adı veya parola hatalı.")
        return self.cleaned_data


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'placeholder' : 'Kullanıcı Adı',
                                                             'class'       : 'form-control'}))
    email = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'placeholder' : 'E-Posta Adresi',
                                                          'class': 'form-control'}))
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Parola',
                                                                 'class': 'form-control'}))
    password2 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Parola Doğrulama',
                                                                  'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={'placeholder' : 'Adı',
                                                               'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={'placeholder' : 'Soyadı',
                                                              'class': 'form-control'}))
    #school = forms.CharField(max_length=100, label='Okul')

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password',
                  'password2',
                  'first_name',
                  'last_name']

    DEFAULT_PASSWORD_LIST_PATH = os.path.join(
        os.path.dirname(os.path.realpath(upath(__file__))), 'common-passwords.txt.gz'
    )

    password_list_path = DEFAULT_PASSWORD_LIST_PATH

    #DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')

    try:
        common_passwords_lines = gzip.open(password_list_path).read().decode('utf-8').splitlines()
    except IOError:
        with open(password_list_path) as f:
            common_passwords_lines = f.readlines()

    passwords = {p.strip() for p in common_passwords_lines}



    def clean_username(self):
        username = self.cleaned_data.get('username')

        #if SequenceMatcher(a=username.lower(), b=password.lower()).quick_ratio() > 0.7:
        #    raise forms.ValidationError("Parola kişisel bilgileriniz ile benzerlik taşıyor.")

        #print(username)
        #print(password)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Bu kullanıcı adı daha önce alınmış. ")



    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if SequenceMatcher(a=username.lower(), b=password.lower()).quick_ratio() > 0.7:

            raise forms.ValidationError("Parola kişisel bilgileriniz ile benzerlik taşıyor.")
        else:
            return self.cleaned_data


    def clean_email(self):
        email_data = self.cleaned_data.get('email')

        if "@" and "." not in email_data:
            raise forms.ValidationError("Geçersiz e-mail adresi")
        elif email_data.index("@") > email_data.index("."):
            raise forms.ValidationError("Geçersiz e-mail adresi")

        return email_data



    def clean_password2(self, min_length=8):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')


        #min_length = self.min_length

        DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')
        user_attributes = DEFAULT_USER_ATTRIBUTES
        self.user_attributes = user_attributes

        if password and password2 and password != password2:
            raise forms.ValidationError("Parolalar eşleşmedi")
        elif len(password) < min_length:
            raise forms.ValidationError("Parola en az 8 karakter içermelidir.")
        elif password.lower().strip() in self.passwords:
            raise forms.ValidationError("Kolay tahmin edilen parola kullanmamalısınız.")

        return password



    def clean_first_name(self):
        cleaned_data = super(UserForm, self).clean()

        first_name = self.cleaned_data.get('first_name')
        password = self.cleaned_data.get('password')
        username = cleaned_data.get('username')


        if SequenceMatcher(a=password.lower(), b=first_name.lower()).quick_ratio() > 0.7:
            raise forms.ValidationError("Parola adınız ile benzerlik taşıyor.")
        elif SequenceMatcher(a=password.lower(), b=username.lower()).quick_ratio() > 0.7:
            raise forms.ValidationError("Parola kullanıcı adınız ile benzerlik taşıyor.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password')

        if SequenceMatcher(a=password.lower(), b=last_name.lower()).quick_ratio() > 0.7:
            raise forms.ValidationError("Parola soyadınız ile benzerlik taşıyor.")

        return last_name






class UserEditForm(forms.ModelForm):
    #city = forms.CharField(max_length=100, default='')
    name = forms.CharField(max_length=100, label='Ad-Soyad', required=False,
                           widget=forms.TextInput(attrs={'style':'width:250px'}))

    school = forms.CharField(max_length=100, label='Okul', required=False,
                           widget=forms.TextInput(attrs={'style': 'width:250px'}))

    website = forms.URLField(max_length=100, label = 'Web Sitesi', required=False,
                             widget=forms.TextInput(attrs={'style': 'width:250px'}))

    phone = forms.IntegerField(label='Telefon', required=False, error_messages=my_default_errors,
                               widget=forms.TextInput(attrs={'style': 'width:250px'}))

    face = forms.FileField(label='Profil Resmi')

    class Meta:
        model = UserProfile
        fields = ['name','school','phone', 'website', 'face']
        #exclude = ['is_superuser']


class UserPasswordResetForm(SetPasswordForm):

    error_messages = {'password_mismatch': _("Parolalar eşleşmedi"),
                      'password_incorrect': _("Parola doğru girilmedi. "
                                            "Lütfen tekrar deneyin")}


    new_password1 = forms.CharField(label=_("Parolayı Yenile"),
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Parolayı Yenile',
                                                                      'class': 'form-control'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Parolayı Doğrula"),
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Parolayı Doğrula',
                                                                      'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


