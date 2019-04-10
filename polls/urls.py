from django.conf.urls import url, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from polls.forms import UserPasswordResetForm

app_name = 'polls'

urlpatterns = [


    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^kaydol/$', views.UserFormView.as_view(), name='register'),
    url(r'^giris/$', views.LoginFormView.as_view(), name='login'),
    url(r'^cikis/$', logoutView, name='logout'),

    #url('', include('django.contrib.auth.urls')),

    url(r'^parola-yenile/$', auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('polls:password_reset_done'),
            template_name='polls/password_reset_form.html',
            email_template_name='polls/password_reset_email.html',
            subject_template_name='polls/password_reset_subject.txt'),
            name='password_reset'),

    url(r'^parola-yenile/kontrol/$', auth_views.PasswordResetDoneView.as_view(
            template_name='polls/password_reset_done.html'),
            name='password_reset_done'),

    url(r'^yenile/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='polls/password_reset_confirm.html',
            form_class=UserPasswordResetForm,
            success_url = reverse_lazy('polls:password_reset_complete')),
            name='password_reset_confirm'),

    url(r'^yenile/kontrol/$', auth_views.PasswordResetCompleteView.as_view(
            template_name='polls/password_reset_complete.html'),
            name='password_reset_complete'),


    url(r'soru/ekle/$', views.PracticeQuestionsView.as_view(), name='question'),
    url(r'girdi/ekle/(?P<question_slug>[\w-]+)$', input_form, name='input'),

    url(r'dersler$', views.TutorialsView.as_view(), name='tutorial'),
    url(r'dersler/cevapla$', submitTutorialCode, name='submit_subject_code'),
    url(r'dersler/kontrol$', runTutorialCode, name='run_subject_code'),
    url(r'cevapla/gonder$', submitcode, name='submit_code'),
    url(r'cevapla/kontrol$', runCode, name='run_code'),

    url(r'^ara/$', views.SearchDetailsView.as_view(), name='search'),

    url(r'^(?P<slug>[\w-]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/(?P<area_slug>[\w-]+)/$', views.QuestionDetailView.as_view(), name='question_detail'),
    url(r'^(?P<slug>[\w-]+)/(?P<area_slug>[\w-]+)/(?P<question_slug>[\w-]+)$', views.QuestionExplainView.as_view(), name='question_explain'),


    url(r'dersler/(?P<slug>[\w-]+)$', views.TutorialLectureView.as_view(), name='tutorial_lecture'),
    url(r'dersler/(?P<pk>[0-9]+)/aciklama$', views.SubjectDetailsView.as_view(), name='subject_detail'),

    url(r'profil/duzenle$', views.UserEditView.as_view(), name='edit_profile'),


    url(r'profil/(?P<username>[a-zA-Z0-9]+)$', views.UserView.as_view(), name='hacker'),
    url(r'profil/sorularim/(?P<pk>[0-9]+)/$', views.UserQuestionView.as_view(), name='sorularim'),
    url(r'profil/soru/duzenle/(?P<pk>[0-9]+)/$', views.PracticeQuestionEditView.as_view(), name='question_edit'),
    url(r'profil/soru/sil/(?P<pk>[0-9]+)/$', views.PracticeQuestionDeleteView.as_view(), name='question_delete'),
    url(r'profil/(?P<username>[a-zA-Z0-9]+)/cozulen-problemler/$', views.UserAnswerView.as_view(), name='cozum'),

    url(r'^baglanti/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends')



    #url(r'cevapla/program/derle/$',views.CompileView.as_view(), name='compiler_c')
    #url(r'^(?P<practice_id>[0-9]+)/(?P<area_id>[0-9]+)/$', views.question_area, name='question_area'),
    #url(r'^$', views.dashboard, name='dashboard')
    #url(r'^$', views.post, name='post'),
    #url(r'^$', views.practice, name='practice'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

