from django.contrib import admin
from .models import Question, Hacker, Job, tutorial, challenge, practice, \
    tutorial_language, practice_area,practice_question, Deneme, Tutorial_Lecture, practice_question_input
from polls.models import UserProfile
# Register your models here.

admin.site.register(Question)
admin.site.register(Hacker)
admin.site.register(tutorial)
admin.site.register(Job)
admin.site.register(challenge)
admin.site.register(practice)
admin.site.register(tutorial_language)
admin.site.register(practice_area)
admin.site.register(practice_question)
admin.site.register(Tutorial_Lecture)
admin.site.register(UserProfile)
admin.site.register(Deneme)
admin.site.register(practice_question_input)













