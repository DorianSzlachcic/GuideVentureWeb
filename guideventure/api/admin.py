from django.contrib import admin

from .models import Adventure, Question, QuizStep, Step

admin.site.register(Adventure)
admin.site.register(Step)


class QuizInline(admin.StackedInline):
    model = Question
    can_delete = False
    verbose_name_plural = "quiestions"


class QuizStepAdmin(admin.ModelAdmin):
    inlines = (QuizInline,)


admin.site.register(QuizStep, QuizStepAdmin)
