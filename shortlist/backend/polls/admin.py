from django.contrib import admin

from shortlist.backend.polls.models import Question
from shortlist.backend.polls.models import Choice

admin.site.register(Choice)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, dict(fields=["question_text"])),
        ("Date Information", dict(fields=["pub_date"], classes="collapse")),
    ]
    inlines = [ChoiceInline]
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
