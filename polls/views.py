from django.db import transaction
from django.http.response import JsonResponse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404, reverse, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView, ListView
from django.views.generic import RedirectView
from django.template import loader, RequestContext
from django.core.exceptions import ValidationError

from polls.models import practice_question
from . import forms
from .models import practice
from .models import practice_area
from .models import practice_question, Tutorial_Lecture, practice_question_input
from .forms import UserForm, LoginForm, UserEditForm, InputFormSet, QuestionForm, QuestionEditForm
from .models import tutorial, User, UserProfile, practice_area
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import logging
from polls import code_persistance, common
from polls.compilers.code_executor import CodeExecutor
from polls.compilers import compile_cpp, compile_c, wrapper
import json
from subprocess import call
import filecmp



logger = logging.getLogger(__name__)


class LoginFormView(View):
    form_class = LoginForm
    template_name = 'polls/login_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('polls:index')

        return render(request, self.template_name, {'form': form})


class UserFormView(View):
    form_class = UserForm
    template_name = 'polls/registration_form.html'


    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form' : form})


    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            new_user = authenticate(username= username, password= password)

            if user is not None:

                if user.is_active:
                    login(request, new_user)
                    return redirect('polls:index')

        return render(request, self.template_name, {'form': form})



class UserFormIndexView(View):
    form_class = UserForm
    template_name = 'polls/index.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form' : form})


    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            new_user = authenticate(username= username, password= password)

            if user is not None:

                if user.is_active:
                    login(request, new_user)
                    return redirect('polls:index')

        return render(request, self.template_name, {'form': form})


class UserQuestionView(generic.DetailView):
    template_name = 'polls/user_questions.html'
    model = User


    def get_context_data(self, **kwargs):
        context = super(UserQuestionView, self).get_context_data(**kwargs)
        context['practice_question'] =  practice_question.objects.all()
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse('polls:sorularim', kwargs={'pk':self.object.user.pk})



'''
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('polls:hacker')

    else:
        form = UserEditForm(instance=request.user)
        return render(request, 'polls/edit_profile.html', {'form': form})
'''


class UserEditView(UpdateView):
    template_name = 'polls/edit_profile.html'
    form_class = UserEditForm
    model = UserProfile

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk = self.kwargs['pk'])
        return user.userprofile

    def get_success_url(self, *args, **kwargs):
        return reverse('polls:edit_profile', kwargs={'pk':self.object.user.pk})


'''
def EditProfileView(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('polls:edit_profile')

    else:
        form = UserEditForm(instance=request.user)
        args = {'form' : form}
        return render(request, 'polls/edit_profile.html', args)


'''

def logoutView(request):
    logout(request)
    return redirect('polls:index')


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    form_class = UserForm

    def get_queryset(self):
        return practice.objects.all()


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            new_user = authenticate(username= username, password= password)

            if user is not None:

                if user.is_active:
                    login(request, new_user)
                    return redirect('polls:index')

        return render(request, self.template_name, {'form': form})


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = self.form_class
        return context




class DetailView(generic.DetailView):

    template_name = 'polls/dashboard.html'
    model = practice


class QuestionDetailView(generic.DetailView):
    template_name = 'polls/practice.html'
    model = practice_area

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['practice'] =  practice.objects.all()
        return context

    #def get_queryset(self):
    #    return practice_area.objects.all()

class QuestionExplainView(generic.DetailView):
    template_name = 'polls/question_explain.html'
    model = practice_question, UserProfile

    def get_queryset(self):
        return practice_question.objects.all()


class PracticeQuestionsView(View):
    template_name = 'polls/questions.html'
    model = practice_question

    form_class = QuestionForm


    def get(self, request):
        form = self.form_class(initial={'author':request.user})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.author = UserProfile.objects.get(user=request.user)
            question.save()

        return render(request, self.template_name, {'form': form})


    def get_success_url(self):
        return reverse('polls:question')


class PracticeQuestionEditView(UpdateView):
    template_name = 'polls/edit_question.html'
    form_class = QuestionEditForm
    model = practice_question

    def get_object(self, *args, **kwargs):
        question = get_object_or_404(practice_question, pk = self.kwargs['pk'])
        return question

    def get_success_url(self, *args, **kwargs):
        return reverse('polls:question_edit', kwargs={'pk':self.object.pk})


'''
class PracticeQuestionInputsView(CreateView):
    template_name = 'polls/question_input.html'
    model = practice_question_input
    fields = ['input_belong_practice', 'input_id', 'input_text', 'output_text']



    def get_context_data(self, **kwargs):
        data = super(PracticeQuestionInputsView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['inputs'] = InputsFormSet(self.request.POST)
        else:
            data['inputs'] = InputsFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        inputs = context['inputs']
        with transaction.atomic():
            self.object = form.save()

            if inputs.is_valid():
                inputs.instance = self.object
                inputs.save()
        return super(PracticeQuestionInputsView, self).form_valid(form)

    #def get_queryset(self):
    #    return practice_question_input.objects.all()

    #def get_success_url(self):
    #    return reverse

'''


def input_form(request, pk):
    question = get_object_or_404(practice_question, pk= pk)

    formset = forms.InputFormSet(queryset=question.practice_question_input_set.all(),
                                initial=[{'input_belong_practice': question.pk}])


    if request.method == 'POST':

        try:
            formset = forms.InputFormSet(request.POST,
                                         queryset=question.practice_question_input_set.all(),
                                         initial=[{'input_belong_practice': question.pk}],
                                         )

        except ValidationError:
            formset = None

        if formset.is_valid():
            inputs = formset.save(commit=False)

            for input_value in inputs:
                input_value.question = question
                input_value.save()

            messages.success(request, "Girdi değerleri başarıyla eklendi")


    return render(request, 'polls/question_input.html', {
        'formset': formset,
        'question': question,
    })


def editor(request, language):
    lang = practice_question.objects.filter(question_language_field=language)

    if len(lang) == 0:
        return HttpResponse(status=404)
    else:
        lang = lang[0]
    code = ''
    if request.user.is_authenticated():
        code = code_persistance.load(request.user.username, lang.question_language_field.name)
    template_name = loader.get_template('polls/question_explain.html')
    context = RequestContext(request, {
        'language' : lang,
        'max_code_length' : common.max_code_size,
        'max_input_length' : common.max_input_size,
        'code' : code,
    })
    return HttpResponse(template_name.render(context))


def submitcode(request):
    template_name = loader.get_template('polls/question_explain.html')

    if request.is_ajax() and request.method == 'POST':
        try:
            executor = CodeExecutor(
                request.POST.get('language'),
                request.POST.get('code'),
                request.POST.get('input', ''),
                #input_value.input_text
            )

            if request.user.is_authenticated():
                code_persistance.save(request.user.username, executor.language, executor.code)
            #if executor.language == 'python':

            #language_name = request.POST.get('language')
            question_id = request.POST.get('question')
            point = 0

            #Python
            if executor.language=="python":
                question = practice_question.objects.get(id = question_id)
                count = 0
                item_count = question.practice_question_input_set.count()

                for item in question.practice_question_input_set.all():
                    input_file = item.input_text
                    output_file = item.output_text

                    executor.pythonExecute(executor.code, input_file, output_file)
                    call(["node", 'static/python_compiler.js'])

                    file_path = "static/data_files/output.txt"
                    answer_file_path = "static/data_files/answer.txt"

                    read_output_file = open(file_path, 'r')
                    read_answer_file = open(answer_file_path, 'r')

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()

                    while output_line != '' or answer_line != '':

                        output_line = output_line.rstrip()
                        answer_line = answer_line.rstrip()

                        if output_line != answer_line:
                            count+=1
                            break

                        output_line = read_output_file.readline()
                        answer_line = read_answer_file.readline()

                hacker = UserProfile.objects.get(user=request.user)

                print(count)
                if count == 0:
                    point += item_count*5.0

                    hacker.user.userprofile.point += point
                    hacker.save()

            #C
            elif executor.language=="c":
                question = practice_question.objects.get(id=question_id)
                count = 0
                item_count = question.practice_question_input_set.count()

                for item in question.practice_question_input_set.all():
                    input_file = item.input_text
                    output_file = item.output_text

                    executor.cExecute(executor.code, input_file, output_file)
                    call(["node", 'static/compiler.js'])


                    file_path = "static/data_files/output.txt"
                    answer_file_path = "static/data_files/answer.txt"

                    read_output_file = open(file_path, 'r')
                    read_answer_file = open(answer_file_path, 'r')

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()



                    while output_line != '' or answer_line != '':

                        output_line = output_line.rstrip()
                        answer_line = answer_line.rstrip()

                        if output_line != answer_line:
                            count += 1

                        output_line = read_output_file.readline()
                        answer_line = read_answer_file.readline()

                hacker = UserProfile.objects.get(user=request.user)

                if count == 0:
                    point += item_count*5.0

                    hacker.user.userprofile.point += point
                    hacker.save()


            #Java
            elif executor.language == "java":
                question = practice_question.objects.get(id=question_id)
                count = 0
                item_count = question.practice_question_input_set.count()


                for item in question.practice_question_input_set.all():
                    input_file = item.input_text
                    output_file = item.output_text

                    executor.JavaExecute(executor.code, input_file, output_file)
                    call(["node", 'static/java_compiler.js'])

                    file_path = "static/data_files/output.txt"
                    answer_file_path = "static/data_files/answer.txt"

                    read_output_file = open(file_path, 'r')
                    read_answer_file = open(answer_file_path, 'r')

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()



                    while output_line != '' or answer_line != '':

                        output_line = output_line.rstrip()
                        answer_line = answer_line.rstrip()

                        if output_line != answer_line:
                            count += 1

                        output_line = read_output_file.readline()
                        answer_line = read_answer_file.readline()

                hacker = UserProfile.objects.get(user=request.user)

                if count == 0:
                    point += item_count * 5.0

                    hacker.user.userprofile.point += point
                    hacker.save()

            #PHP
            elif executor.language == "php":
                question = practice_question.objects.get(id=question_id)
                count = 0
                item_count = question.practice_question_input_set.count()

                for item in question.practice_question_input_set.all():
                    input_file = item.input_text
                    output_file = item.output_text

                    executor.phpExecute(executor.code, input_file, output_file)
                    call(["node", "static/php_compiler.js"])


                    file_path = "static/data_files/output.txt"
                    answer_file_path = "static/data_files/answer.txt"

                    read_output_file = open(file_path, 'r')
                    read_answer_file = open(answer_file_path, 'r')

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()



                    while output_line != '' or answer_line != '':

                        output_line = output_line.rstrip()
                        answer_line = answer_line.rstrip()

                        if output_line != answer_line:
                            count += 1

                        output_line = read_output_file.readline()
                        answer_line = read_answer_file.readline()

                hacker = UserProfile.objects.get(user=request.user)

                if count == 0:
                    point += item_count*5.0

                    hacker.user.userprofile.point += 5.0
                    hacker.save()


            #CSharp
            elif executor.language == "csharp":
                question = practice_question.objects.get(id=question_id)

                for item in question.practice_question_input_set.all():
                    input_file = item.input_text

                    executor.c_sharpExecute(executor.code, input_file)
                    call(["node", "C:\\Users\\User\\PycharmProjects\\web_ilk\\staticfiles\\csharp_compiler.js"])


            if point > 0:
                response = '<h1 id = "correctAnswer">Tebrikler!</h1>' + '\n' \
                           'Bütün testleri başarıyla geçerek ' + str(point) + ' puan kazandınız.'
            else:
                response = '<h1 id = "wrongAnswer">Yanlış Cevap</h1>' + '\n' \
                           'Bütün testlerden başarıyla geçemediniz.' \
                           'Lütfen tekrar deneyin.' + '\n' + 'Diğer test girdilerini dikkate alarak ' \
                           'programı tekrar yazmaya çalışın.'


            #file_path = "C:/Users/User/Desktop/output.txt"
            #file = open(file_path, 'r+')
            content_type = 'text/plain'

            #data = json.dumps(file)
            #mimetype = 'application/json'

            return HttpResponse(response, content_type)

        except Exception as e:
            logger.exception(e)
            return HttpResponse(str(e), status=400)
    else: # POST ve XHR olmayan çağrıları engelle
        return HttpResponse(status=400)


def runCode(request):
    if request.is_ajax() and request.method == 'POST':
        try:
            executor = CodeExecutor(
                request.POST.get('language'),
                request.POST.get('code'),
                request.POST.get('input', ''),
                # input_value.input_text
            )

            if request.user.is_authenticated():
                code_persistance.save(request.user.username, executor.language, executor.code)
            # if executor.language == 'python':

            # language_name = request.POST.get('language')
            question_id = request.POST.get('question')

            # Python
            if executor.language == "python":
                question = practice_question.objects.get(id=question_id)

                input_item = question.practice_question_input_set.get(input_id=1)
                input_file = input_item.input_text
                output_file = input_item.output_text

                executor.pythonExecute(executor.code, input_file, output_file)
                #call(["node", "C:\\Users\\User\\PycharmProjects\\web_ilk\\staticfiles\\python_compiler.js"])
                call(["node", "static/python_compiler.js"])

                file_path = "static/data_files/output.txt"
                answer_file_path = "static/data_files/answer.txt"

                read_output_file = open(file_path, 'r')
                read_answer_file = open(answer_file_path, 'r')

                output_line = read_output_file.readline()
                answer_line = read_answer_file.readline()

                count = 0

                while output_line != '' or answer_line != '':

                    output_line = output_line.rstrip()
                    answer_line = answer_line.rstrip()

                    if output_line != answer_line:
                        count += 1

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()

                hacker = UserProfile.objects.get(user=request.user)

                if count == 0:
                    hacker.user.userprofile.point += 5.0
                    hacker.save()

            # C
            elif executor.language == "c":
                question = practice_question.objects.get(id=question_id)

                input_item = question.practice_question_input_set.get(input_id=1)
                input_file = input_item.input_text
                output_file = input_item.output_text

                executor.cExecute(executor.code, input_file, output_file)
                #call(["node", "C:\\Users\\User\\PycharmProjects\\web_ilk\\staticfiles\\python_compiler.js"])
                call(["node", "static/compiler.js"])

                file_path = "static/data_files/output.txt"
                answer_file_path = "static/data_files/answer.txt"

                read_output_file = open(file_path, 'r')
                read_answer_file = open(answer_file_path, 'r')

                output_line = read_output_file.readline()
                answer_line = read_answer_file.readline()

                count = 0

                while output_line != '' or answer_line != '':

                    output_line = output_line.rstrip()
                    answer_line = answer_line.rstrip()

                    if output_line != answer_line:
                        count += 1

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()


                hacker = UserProfile.objects.get(user=request.user)

                if count == 0:
                    hacker.user.userprofile.point += 5.0
                    hacker.save()

            # Java
            elif executor.language == "java":
                question = practice_question.objects.get(id=question_id)

                input_item = question.practice_question_input_set.get(input_id=1)
                input_file = input_item.input_text
                output_file = input_item.output_text

                executor.JavaExecute(executor.code, input_file, output_file)
                call(["node", "static/java_compiler.js"])

                file_path = "static/data_files/output.txt"
                answer_file_path = "static/data_files/answer.txt"

                read_output_file = open(file_path, 'r')
                read_answer_file = open(answer_file_path, 'r')

                output_line = read_output_file.readline()
                answer_line = read_answer_file.readline()

                count = 0

                while output_line != '' or answer_line != '':

                    output_line = output_line.rstrip()
                    answer_line = answer_line.rstrip()

                    if output_line != answer_line:
                        count += 1

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()

                hacker = UserProfile.objects.get(user=request.user)

                if count == 0:
                    hacker.user.userprofile.point += 5.0
                    hacker.save()


            # PHP
            elif executor.language == "php":
                question = practice_question.objects.get(id=question_id)

                input_item = question.practice_question_input_set.get(input_id=1)
                input_file = input_item.input_text
                output_file = input_item.output_text

                executor.phpExecute(executor.code, input_file, output_file)
                call(["node", "static/java_compiler.js"])

                file_path = "static/data_files/output.txt"
                answer_file_path = "static/data_files/answer.txt"

                read_output_file = open(file_path, 'r')
                read_answer_file = open(answer_file_path, 'r')

                output_line = read_output_file.readline()
                answer_line = read_answer_file.readline()

                count = 0

                while output_line != '' or answer_line != '':

                    output_line = output_line.rstrip()
                    answer_line = answer_line.rstrip()

                    if output_line != answer_line:
                        count += 1

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()

                hacker = UserProfile.objects.get(user=request.user)

                if count == 0:
                    hacker.user.userprofile.point += 5.0
                    hacker.save()



            # CSharp
            elif executor.language == "csharp":
                question = practice_question.objects.get(id=question_id)

                for item in question.practice_question_input_set.all():
                    input_file = item.input_text

                    executor.c_sharpExecute(executor.code, input_file)
                    call(["node", "C:\\Users\\User\\PycharmProjects\\web_ilk\\staticfiles\\csharp_compiler.js"])

            file_path = "static/data_files/output.txt"
            file = open(file_path, 'r+')
            content_type = 'text/plain'

            # data = json.dumps(file)
            # mimetype = 'application/json'

            return HttpResponse(file, content_type)

        except Exception as e:
            logger.exception(e)
            return HttpResponse(str(e), status=400)
    else:  # POST ve XHR olmayan çağrıları engelle
        return HttpResponse(status=400)


def submitTutorialCode(request):

    if request.is_ajax() and request.method == 'POST':
        try:
            executor = CodeExecutor(
                request.POST.get('language'),
                request.POST.get('code'),
                request.POST.get('input', ''),
                # input_value.input_text
            )

            if request.user.is_authenticated():
                code_persistance.save(request.user.username, executor.language, executor.code)
                # if executor.language == 'python':

                # language_name = request.POST.get('language')
            lecture_question_id = request.POST.get('lecture_question')


            # Python
            if executor.language == "Python":
                question = Tutorial_Lecture.objects.get(id=lecture_question_id)

                input_file = question.lecture_area_input
                output_file = question.lecture_area_output

                executor.pythonExecute(executor.code, input_file, output_file)
                call(["node", "static/python_compiler.js"])

                file_path = "static/data_files/output.txt"
                answer_file_path = "static/data_files/answer.txt"

                read_output_file = open(file_path, 'r')
                read_answer_file = open(answer_file_path, 'r')

                output_line = read_output_file.readline()
                answer_line = read_answer_file.readline()

                count = 0
                while output_line != '' or answer_line != '':

                    output_line = output_line.rstrip()
                    answer_line = answer_line.rstrip()

                    if output_line != answer_line:
                        count += 1

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()

                hacker = UserProfile.objects.get(user=request.user)

                if count == 0:
                    hacker.user.userprofile.point += 5.0
                    hacker.save()

            elif executor.language == "C/C++":
                question = Tutorial_Lecture.objects.get(id=lecture_question_id)

                input_file = question.lecture_area_input
                output_file = question.lecture_area_output

                executor.cExecute(executor.code, input_file, output_file)
                call(["node", "static/compiler.js"])

                file_path = "static/data_files/output.txt"
                answer_file_path = "static/data_files/answer.txt"

                read_output_file = open(file_path, 'r')
                read_answer_file = open(answer_file_path, 'r')

                output_line = read_output_file.readline()
                answer_line = read_answer_file.readline()

                count = 0
                while output_line != '' or answer_line != '':

                    output_line = output_line.rstrip()
                    answer_line = answer_line.rstrip()

                    if output_line != answer_line:
                        count += 1

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()

                hacker = UserProfile.objects.get(user=request.user)

                if count == 0:
                    hacker.user.userprofile.point += 5.0
                    hacker.save()





            file_path = "static/data_files/output.txt"
            file = open(file_path, 'r+')
            content_type = 'text/plain'

            # data = json.dumps(file)
            # mimetype = 'application/json'

            return HttpResponse(file, content_type)

        except Exception as e:
            logger.exception(e)
            return HttpResponse(str(e), status=400)

    else:  # POST ve XHR olmayan çağrıları engelle
        return HttpResponse(status=400)


def runTutorialCode(request):

    if request.is_ajax() and request.method == 'POST':
        try:
            executor = CodeExecutor(
                request.POST.get('language'),
                request.POST.get('code'),
                request.POST.get('input', ''),
                # input_value.input_text
            )

            if request.user.is_authenticated():
                code_persistance.save(request.user.username, executor.language, executor.code)
                # if executor.language == 'python':

                # language_name = request.POST.get('language')
            lecture_question_id = request.POST.get('lecture_question')


            # Python
            if executor.language == "Python":
                question = Tutorial_Lecture.objects.get(id=lecture_question_id)

                input_file = question.lecture_area_input
                output_file = question.lecture_area_output

                executor.pythonExecute(executor.code, input_file, output_file)
                call(["node", "static/python_compiler.js"])

                file_path = "static/data_files/output.txt"
                answer_file_path = "static/data_files/answer.txt"

                read_output_file = open(file_path, 'r')
                read_answer_file = open(answer_file_path, 'r')

                output_line = read_output_file.readline()
                answer_line = read_answer_file.readline()

                count = 0
                while output_line != '' or answer_line != '':

                    output_line = output_line.rstrip()
                    answer_line = answer_line.rstrip()

                    if output_line != answer_line:
                        count += 1

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()

                hacker = UserProfile.objects.get(user=request.user)

                if count == 0:
                    hacker.user.userprofile.point += 5.0
                    hacker.save()

            elif executor.language == "C/C++":
                question = Tutorial_Lecture.objects.get(id=lecture_question_id)

                input_file = question.lecture_area_input
                output_file = question.lecture_area_output

                executor.cExecute(executor.code, input_file, output_file)
                call(["node", "static/compiler.js"])

                file_path = "static/data_files/output.txt"
                answer_file_path = "static/data_files/answer.txt"

                read_output_file = open(file_path, 'r')
                read_answer_file = open(answer_file_path, 'r')

                output_line = read_output_file.readline()
                answer_line = read_answer_file.readline()

                count = 0
                while output_line != '' or answer_line != '':

                    output_line = output_line.rstrip()
                    answer_line = answer_line.rstrip()

                    if output_line != answer_line:
                        count += 1

                    output_line = read_output_file.readline()
                    answer_line = read_answer_file.readline()

                hacker = UserProfile.objects.get(user=request.user)

                if count == 0:
                    hacker.user.userprofile.point += 5.0
                    hacker.save()




            file_path = "static/data_files/output.txt"
            file = open(file_path, 'r+')
            content_type = 'text/plain'

            # data = json.dumps(file)
            # mimetype = 'application/json'

            return HttpResponse(file, content_type)

        except Exception as e:
            logger.exception(e)
            return HttpResponse(str(e), status=400)

    else:  # POST ve XHR olmayan çağrıları engelle
        return HttpResponse(status=400)



class TutorialsView(generic.ListView):
    template_name = 'polls/dersler.html'
    model = tutorial

    def get_queryset(self):
        return tutorial.objects.all()


class TutorialLectureView(generic.DetailView):
    template_name = 'polls/konular.html'
    model = tutorial

    def get_queryset(self):
        return tutorial.objects.all()

class SubjectDetailsView(generic.DetailView):
    template_name = 'polls/konu_detail.html'
    model = Tutorial_Lecture

    def get_queryset(self):
        return Tutorial_Lecture.objects.all()


class UserView(CreateView):
    template_name = 'polls/user_profile.html'
    model = User
    fields = '__all__'

    def get_queryset(self):
        return User.objects.all()
















































'''
from django.shortcuts import render, get_object_or_404
from .models import tutorial, practice, practice_area
from django.http import HttpResponse
# Create your views here.

def index(request):
    #return render(request, 'polls/index.html', {})

    all_practices = practice.objects.all()

    context = {'all_practices': all_practices}

    #html = ''
    #for tutorials in all_tutorials:
    #    url = '/' + str(tutorials.tutorial_id) + '/'
    #    html += '<a href="' + url + '">' + tutorials.tutorial_name + '</a><br>'

    return render(request, 'polls/index.html', context)

def detail(request, practice_id):

    practice_no = get_object_or_404(practice, practice_id = practice_id)
    return render(request, 'polls/dashboard.html',  {'practice_no': practice_no})

def question_area(request, area_id):

    practice_area_no = get_object_or_404(practice_area, area_id = area_id)
    return render(request, 'polls/questions.html', {'practice_area_no': practice_area_no})

def practice(request):
    return render(request, 'polls/practice.html', {})

def post(request):
    template = loader.get_template('polls/post_form_upload.html')
    return HttpResponse(template.render(request))
'''






