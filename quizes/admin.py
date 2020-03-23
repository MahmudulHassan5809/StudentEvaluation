from django.contrib import admin
from django.utils.html import escape, mark_safe
from .models import Topic, Question, Option
# Register your models here.


class QuestionInline(admin.StackedInline):
    model = Question


class TopicAdmin(admin.ModelAdmin):
    list_display = ["topic_name", "add_question"]
    search_fields = ["topic_name"]
    inlines = [QuestionInline]
    list_per_page = 20

    def add_question(self, obj):
        return mark_safe(f'<a href="http://127.0.0.1:8000/admin/quizes/question/add/?topic={obj.id}">Add Question</a>')


admin.site.register(Topic, TopicAdmin)


class OptionInline(admin.StackedInline):
    model = Option


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["topic", "question_name", "add_options"]
    search_fields = ["topic__topic_name", "question_name"]
    list_filter = ["topic__topic_name"]
    autocomplete_fields = ('topic',)

    inlines = [OptionInline]

    list_per_page = 20

    def add_options(self, obj):
        return mark_safe(f'<a href="http://127.0.0.1:8000/admin/quizes/option/add/?question={obj.id}">Add Qoptions</a>')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        id = request.GET.get('topic')
        if db_field.name == 'topic' and id:
            kwargs["queryset"] = Topic.objects.filter(id=int(id))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Question, QuestionAdmin)


class OptionAdmin(admin.ModelAdmin):
    list_display = ["topic", "question", "option_name", "wright_answer"]
    search_fields = ["question__name", "option_name"]
    list_filter = ["question__topic__topic_name"]
    list_editable = ["wright_answer"]
    autocomplete_fields = ('question',)

    list_per_page = 20

    def topic(self, obj):
        return obj.question.topic

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        id = request.GET.get('question')
        if db_field.name == 'question' and id:
            kwargs["queryset"] = Question.objects.filter(id=int(id))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Option, OptionAdmin)
