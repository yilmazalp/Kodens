import datetime
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField
from django.conf import settings

MY_CHOICES = (('c', 'C'),
              ('c++', 'C++'),
              ('c#', 'C#'),
              ('python', 'Python'),
              ('java', 'Java'),
              )





class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    school = models.CharField(max_length=100, default='')
    point = models.FloatField(default=0)
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    face = models.FileField(default='')

    @property
    def face_url(self):
        if self.face and hasattr(self.face, 'url'):
            return self.face.url

    #location = models.CharField(max_length=30, blank=True)
    #birth_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('polls:hacker', kwargs={'pk': self.pk})


    def __str__(self):  # __unicode__ for Python 2
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user = kwargs['instance'])


post_save.connect(create_profile, sender=User)


'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
'''


class Question(models.Model):
    question_text = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=20)
    votes = models.IntegerField(default=0)

class Hacker(models.Model):
    username = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    school = models.CharField(max_length=250)

class tutorial(models.Model):
    tutorial_name = models.CharField(max_length=250)
    tutorial_id = models.CharField(max_length=250)
    tutorial_logo = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.tutorial_name

class tutorial_language(models.Model):
    course = models.ForeignKey(tutorial, on_delete=models.CASCADE)
    language_id = models.CharField(max_length=250)
    language_name = models.CharField(max_length=250)

    def __str__(self):
        return self.language_name



class Tutorial_Lecture(models.Model):
    lecture_discipline = models.ForeignKey(tutorial, on_delete=models.CASCADE)
    lecture_area_name = models.CharField(max_length=100, default='')
    lecture_area_text = RichTextField(max_length=750, default='')
    lecture_area_input = models.TextField(max_length=150, default='')
    lecture_area_output = models.TextField(max_length=150, default='')


    def get_absolute_url(self):
        return reverse('polls:tutorial_lecture', kwargs={'pk': self.pk})


    def __str__(self):
        return self.lecture_area_name


class Deneme(models.Model):
    deneme_isim = models.CharField(max_length=250)
    deneme_id = models.CharField(max_length=250)


class practice(models.Model):
    practice_name = models.CharField(max_length=250)
    practice_id = models.CharField(max_length=250)
    practice_logo = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.practice_name

class practice_area(models.Model):
    discipline = models.ForeignKey(practice, on_delete=models.CASCADE)
    area_id = models.CharField(max_length=250)
    area_name = models.CharField(max_length=250)

    def __str__(self):
        return self.area_name

class practice_question(models.Model):
    practice_discipline = models.ForeignKey(practice_area, on_delete=models.CASCADE, verbose_name='konu adı', null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, default=1)
    question_area_id = models.CharField(max_length=5, default='1', null=True)
    question_area_name = models.CharField(max_length=100, default='', verbose_name='soru adı')
    question_area_text = RichTextField(max_length=750, default='', verbose_name='soru')
    question_input_text = models.TextField(max_length=150, default='', verbose_name='girdi formatı')
    question_answer_text = models.TextField(max_length=150, default='', verbose_name='çıktı formatı')
    question_language_field = MultiSelectField(choices=MY_CHOICES, default='', verbose_name='kullanılacak diller')


    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'pk': self.pk})


    def __str__(self):
        return self.question_area_name


class practice_question_input(models.Model):
    input_belong_practice = models.ForeignKey(practice_question, on_delete=models.CASCADE, null=True)
    input_id = models.CharField(max_length=5, default='')
    input_text = models.TextField(max_length=150, default='')
    output_text = models.TextField(max_length=150, default='')


    def get_absolute_url(self):
        return reverse('polls:question')

    def __str__(self):
        return str(self.input_belong_practice)


class challenge(models.Model):
    challenge_name = models.CharField(max_length=250)
    challenge_id = models.CharField(max_length=250)

class Job(models.Model):
    company_name = models.CharField(max_length=250, default='', verbose_name='firma ismi')
    job_name = models.TextField(max_length=100, default='', verbose_name='iş ismi')
    job_description  = RichTextField(max_length=750, default='', verbose_name='iş tanımı')

    def __str__(self):
        return str(self.company_name)