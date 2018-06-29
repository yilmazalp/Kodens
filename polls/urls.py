from django.conf.urls import url
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'polls'

urlpatterns = [



    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^kaydol/$', views.UserFormView.as_view(), name='register'),
    url(r'^giris/$', views.LoginFormView.as_view(), name='login'),
    url(r'^cikis/$', logoutView, name='logout'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'soru/ekle/$', views.PracticeQuestionsView.as_view(), name='question'),
    url(r'girdi/ekle/(?P<pk>[0-9]+)$', input_form, name='input'),
    url(r'sorular/(?P<pk>[0-9]+)/$', views.QuestionDetailView.as_view(), name='question_detail'),
    url(r'cevapla/(?P<pk>[0-9]+)$', views.QuestionExplainView.as_view(), name='question_explain'),
    url(r'cevapla/gonder$', submitcode, name='submit_code'),
    url(r'cevapla/kontrol$', runCode, name='run_code'),
    url(r'dersler/$', views.TutorialsView.as_view(), name='tutorial'),
    url(r'dersler/(?P<pk>[0-9]+)/$', views.TutorialLectureView.as_view(), name='tutorial_lecture'),
    url(r'dersler/(?P<pk>[0-9]+)/aciklama$', views.SubjectDetailsView.as_view(), name='subject_detail'),
    url(r'dersler/cevapla$', submitTutorialCode, name='submit_subject_code'),
    url(r'dersler/kontrol$', runTutorialCode, name='run_subject_code'),
    url(r'profil/(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='hacker'),
    url(r'profil/(?P<pk>[0-9]+)/duzenle/$', views.UserEditView.as_view(), name='edit_profile'),
    url(r'profil/sorularim/(?P<pk>[0-9]+)/$', views.UserQuestionView.as_view(), name='sorularim'),
    url(r'profil/soru/duzenle/(?P<pk>[0-9]+)/$', views.PracticeQuestionEditView.as_view(), name='question_edit'),

    #url(r'cevapla/program/derle/$',views.CompileView.as_view(), name='compiler_c')
    #url(r'^(?P<practice_id>[0-9]+)/(?P<area_id>[0-9]+)/$', views.question_area, name='question_area'),
    #url(r'^$', views.dashboard, name='dashboard')
    #url(r'^$', views.post, name='post'),
    #url(r'^$', views.practice, name='practice'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

