from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from modeltranslation.forms import TranslationModelForm

from .models import (
    Quiz,
    Progress,
    Question,
    MCQuestion,
    Choice,
    MultiResponseQuestion,
    MultiResponseChoice,
    TrueFalseQuestion,
    TrueFalseStatement,
    EssayQuestion,
    Sitting,
)


class ChoiceInline(admin.TabularInline):
    model = Choice


class MultiResponseChoiceInline(admin.TabularInline):
    model = MultiResponseChoice


class TrueFalseStatementInline(admin.TabularInline):
    model = TrueFalseStatement
class QuizAdminForm(TranslationModelForm):
    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(verbose_name=_("Questions"), is_stacked=False),
    )

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields[
                "questions"
            ].initial = self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data["questions"])
        self.save_m2m()
        return quiz


class QuizAdmin(TranslationAdmin):
    form = QuizAdminForm
    fields = ('title', 'description',)
    list_display = ("title",)
    # list_filter = ('category',)
    search_fields = (
        "description",
        "category",
    )


class MCQuestionAdmin(TranslationAdmin):
    list_display = ("content",)
    # list_filter = ('category',)
    fieldsets = [(u'figure' 'quiz' 'choice_order', {'fields': ("content","explanation")})]

    search_fields = ("content", "explanation")
    filter_horizontal = ("quiz",)

    inlines = [ChoiceInline]


class MultiResponseQuestionAdmin(TranslationAdmin):
    list_display = ("content",)
    fieldsets = [(u'figure' 'quiz' 'choice_order', {'fields': ("content","explanation")})]
    search_fields = ("content", "explanation")
    filter_horizontal = ("quiz",)
    inlines = [MultiResponseChoiceInline]


class TrueFalseQuestionAdmin(TranslationAdmin):
    list_display = ("content",)
    fieldsets = [(u'figure' 'quiz', {'fields': ("content","explanation")})]
    search_fields = ("content", "explanation")
    filter_horizontal = ("quiz",)
    inlines = [TrueFalseStatementInline]


class ProgressAdmin(admin.ModelAdmin):
    search_fields = (
        "user",
        "score",
    )


class EssayQuestionAdmin(admin.ModelAdmin):
    list_display = ("content",)
    # list_filter = ('category',)
    fields = (
        "content",
        "quiz",
        "explanation",
    )
    search_fields = ("content", "explanation")
    filter_horizontal = ("quiz",)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(MultiResponseQuestion, MultiResponseQuestionAdmin)
admin.site.register(TrueFalseQuestion, TrueFalseQuestionAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(EssayQuestion, EssayQuestionAdmin)
admin.site.register(Sitting)
