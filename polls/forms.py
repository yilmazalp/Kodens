from django.contrib.auth.models import User
from polls.models import UserProfile
from polls.models import practice_area, practice_question, practice_question_input
from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms.formsets import DELETION_FIELD_NAME


'''
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['url', 'location', 'company']
'''

#QuestionFormSet = inlineformset_factory(practice_area, practice_question, extra=1)
#InputsFormSet = inlineformset_factory(practice_question, practice_question_input, extra=1)

class QuestionInputForm(forms.ModelForm):
    class Meta:
        model  = practice_question_input
        fields = ['input_belong_practice','input_id', 'input_text', 'output_text']
        widgets = {'input_belong_practice' : forms.HiddenInput()}

InputFormSet = forms.modelformset_factory(practice_question_input, form=QuestionInputForm)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = practice_question
        fields = ['practice_discipline', 'question_area_name', 'question_area_text',
                  'question_input_text', 'question_answer_text', 'question_language_field']


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


    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("Parolalar eşleşmedi")
        return password2


class UserEditForm(forms.ModelForm):
    #city = forms.CharField(max_length=100, default='')
    name = forms.CharField(max_length=100, label='Ad-Soyad', required=False,
                           widget=forms.TextInput(attrs={'style':'width:250px'}))

    school = forms.CharField(max_length=100, label='Okul', required=False,
                           widget=forms.TextInput(attrs={'style': 'width:250px'}))

    website = forms.URLField(max_length=100, label = 'Web Sitesi', required=False,
                             widget=forms.TextInput(attrs={'style': 'width:250px'}))

    phone = forms.IntegerField(label='Telefon', required=False,
                               widget=forms.TextInput(attrs={'style': 'width:250px'}))

    face = forms.FileField(label='Profil Resmi')

    class Meta:
        model = UserProfile
        fields = ['name','school','phone', 'website', 'face']
        #exclude = ['is_superuser']



