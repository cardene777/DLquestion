from django.contrib import admin
from .models import *


class QuestionTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'about')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question', 'correct', 'number')


class DataAdmin(admin.ModelAdmin):
    list_display = ('experiment_number', 'user', 'judge', 'time', 'question_number', 'correct', 'answer')


admin.site.register(QuestionTitle, QuestionTitleAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Data, DataAdmin)