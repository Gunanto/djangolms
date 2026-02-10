from django import forms
from django.forms.widgets import RadioSelect, Textarea, CheckboxSelectMultiple
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from django.forms.models import inlineformset_factory

from accounts.models import User
from .models import (
    Question,
    Quiz,
    MCQuestion,
    Choice,
    MultiResponseQuestion,
    MultiResponseChoice,
    TrueFalseQuestion,
    TrueFalseStatement,
)


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_choices_list()]
        self.fields["answers"] = forms.ChoiceField(
            choices=choice_list, widget=RadioSelect
        )


class EssayForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(EssayForm, self).__init__(*args, **kwargs)
        self.fields["answers"] = forms.CharField(
            widget=Textarea(attrs={"style": "width:100%"})
        )


class QuizAddForm(forms.ModelForm):
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
        super(QuizAddForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields[
                "questions"
            ].initial = self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAddForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data["questions"])
        self.save_m2m()
        return quiz


class MCQuestionForm(forms.ModelForm):
    class Meta:
        model = MCQuestion
        exclude = ()


class MultiResponseForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(MultiResponseForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_choices_list()]
        self.fields["answers"] = forms.MultipleChoiceField(
            choices=choice_list, widget=CheckboxSelectMultiple
        )


class TrueFalseForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(TrueFalseForm, self).__init__(*args, **kwargs)
        self.statement_fields = []
        self.field_statement_map = {}
        statements = question.get_choices()
        for stmt in statements:
            field_name = f"statement_{stmt.id}"
            self.fields[field_name] = forms.ChoiceField(
                choices=(("true", _("Benar")), ("false", _("Salah"))),
                widget=RadioSelect,
                required=True,
            )
            self.statement_fields.append((stmt, field_name))
            self.field_statement_map[field_name] = stmt.id

    def clean(self):
        cleaned = super().clean()
        answers = {}
        for field_name, stmt_id in self.field_statement_map.items():
            value = cleaned.get(field_name)
            if value is None:
                continue
            answers[stmt_id] = True if value == "true" else False
        cleaned["answers"] = answers
        return cleaned

class MCQuestionFormSet(forms.BaseInlineFormSet):
    def clean(self):
        """
        Custom validation for the formset to ensure:
        1. At least two choices are provided and not marked for deletion.
        2. At least one of the choices is marked as correct.
        """
        super().clean()

        # Collect non-deleted forms
        valid_forms = [form for form in self.forms if not form.cleaned_data.get('DELETE', True)]

        valid_choices = ['choice' in form.cleaned_data.keys() for form in valid_forms]
        if(not all(valid_choices)):
            raise forms.ValidationError("You must add a valid choice name.")

        # If all forms are deleted, raise a validation error
        if len(valid_forms) < 2:
            raise forms.ValidationError("You must provide at least two choices.")

        # Check if at least one of the valid forms is marked as correct
        correct_choices = [form.cleaned_data.get('correct', False) for form in valid_forms]

        if not any(correct_choices):
            raise forms.ValidationError("One choice must be marked as correct.")

        if correct_choices.count(True)>1:
            raise forms.ValidationError("Only one choice must be marked as correct.")


class MultiResponseQuestionForm(forms.ModelForm):
    class Meta:
        model = MultiResponseQuestion
        exclude = ()


class MultiResponseQuestionFormSet(forms.BaseInlineFormSet):
    def clean(self):
        """
        Custom validation for the formset to ensure:
        1. At least two choices are provided and not marked for deletion.
        2. At least one of the choices is marked as correct.
        """
        super().clean()

        valid_forms = [form for form in self.forms if not form.cleaned_data.get("DELETE", True)]

        valid_choices = ["choice" in form.cleaned_data.keys() for form in valid_forms]
        if not all(valid_choices):
            raise forms.ValidationError("You must add a valid choice name.")

        if len(valid_forms) < 2:
            raise forms.ValidationError("You must provide at least two choices.")

        correct_choices = [form.cleaned_data.get("correct", False) for form in valid_forms]

        if not any(correct_choices):
            raise forms.ValidationError("At least one choice must be marked as correct.")

class TrueFalseQuestionForm(forms.ModelForm):
    class Meta:
        model = TrueFalseQuestion
        exclude = ()


class TrueFalseStatementForm(forms.ModelForm):
    class Meta:
        model = TrueFalseStatement
        fields = ["statement", "correct"]


class TrueFalseQuestionFormSet(forms.BaseInlineFormSet):
    def clean(self):
        """
        Custom validation for the formset to ensure:
        1. At least two statements are provided and not marked for deletion.
        2. Each statement has a defined truth value.
        """
        super().clean()

        valid_forms = [form for form in self.forms if not form.cleaned_data.get("DELETE", True)]

        valid_statements = ["statement" in form.cleaned_data.keys() for form in valid_forms]
        if not all(valid_statements):
            raise forms.ValidationError("You must add a valid statement.")

        if len(valid_forms) < 2:
            raise forms.ValidationError("You must provide at least two statements.")


MCQuestionFormSet = inlineformset_factory(
    MCQuestion,
    Choice,
    form=MCQuestionForm,
    formset=MCQuestionFormSet,
    fields=["choice", "correct"],
    can_delete=True,
    extra=5,
)

MultiResponseQuestionFormSet = inlineformset_factory(
    MultiResponseQuestion,
    MultiResponseChoice,
    form=MultiResponseQuestionForm,
    formset=MultiResponseQuestionFormSet,
    fields=["choice", "correct"],
    can_delete=True,
    extra=5,
)

TrueFalseQuestionFormSet = inlineformset_factory(
    TrueFalseQuestion,
    TrueFalseStatement,
    form=TrueFalseStatementForm,
    formset=TrueFalseQuestionFormSet,
    fields=["statement", "correct"],
    can_delete=True,
    extra=5,
)
