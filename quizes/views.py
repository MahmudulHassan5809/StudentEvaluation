from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from accounts.mixins import AictiveUserRequiredMixin, AictiveTeacherRequiredMixin, AictiveStudentRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Topic, Question, Option
from django.views import View
# Create your views here.


class QuizeBoard(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        all_topic = Topic.objects.all()

        context = {
            'all_topic': all_topic,
            'title': 'Quiz Board'
        }

        return render(request, 'quizes/quiz_board.html', context)


class StartExam(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        topic_name = kwargs.get('topic_name')
        topic_id = kwargs.get('topic_id')

        topic_obj = get_object_or_404(Topic, id=topic_id)

        all_topic_question = topic_obj.topic_question.all()

        # request.session[settings.ANSWER_SESSION_ID] = {}
        # request.session.modified = True

        page = request.GET.get('page', 1)
        paginator = Paginator(all_topic_question, 2)
        try:
            all_topic_question = paginator.page(page)
        except PageNotAnInteger:
            all_topic_question = paginator.page(1)
        except EmptyPage:
            all_topic_question = paginator.page(paginator.num_pages)

        context = {
            'title': topic_obj.topic_name,
            'all_topic_question': all_topic_question,
            'topic_name': topic_name,
            'topic_id': topic_id,
            'page': page
        }

        return render(request, 'quizes/start_exam.html', context)

    def post(self, request, *args, **kwargs):
        topic_name = kwargs.get('topic_name')
        topic_id = kwargs.get('topic_id')
        page = request.POST.get('page')

        page = int(page) + 1

        topic_obj = get_object_or_404(Topic, id=topic_id)

        data = iter(request.POST.items())
        first_item = next(data)
        second_item = next(data)

        correct_results = {}
        incorrect_results = {}

        self.session = request.session
        answer = self.session.get(
            settings.ANSWER_SESSION_ID)

        if not answer:
            answer = self.session[settings.ANSWER_SESSION_ID] = {}

        self.answer = answer

        for question_id, option_id in data:
            question = Question.objects.filter(
                id=question_id, topic=topic_obj).first()
            your_option = Option.objects.filter(id=option_id).first()
            correct_option = question.question_option.filter(
                wright_answer=True).first()

            if correct_option.id == int(option_id):
                self.answer[question_id] = {
                    'Question': question.question_name,
                    'YourOption': your_option.option_name,
                    'CorrectOption': correct_option.option_name,
                    'status': 'Correct',
                    'points': 1
                }

            else:
                self.answer[question_id] = {
                    'Question': question.question_name,
                    'YourOption': your_option.option_name,
                    'CorrectOption': correct_option.option_name,
                    'status': 'InCorrect',
                    'points': 0
                }
            self.session[settings.ANSWER_SESSION_ID] = self.answer
            self.session.modified = True

        return HttpResponseRedirect(f"http://127.0.0.1:8000/quizes/start-exam/{topic_name}/{topic_id}/?page={page}")


class ViewAnswer(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        topic_id = kwargs.get('topic_id')
        topic_name = kwargs.get('topic_name')

        topic_obj = get_object_or_404(Topic, id=topic_id)

        context = {
            'title': f'{topic_obj} Result',
            'topic_obj': topic_obj
        }

        return render(request, 'quizes/quiz_result.html', context)


class ReTry(AictiveUserRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        request.session[settings.ANSWER_SESSION_ID] = {}
        request.session.modified = True

        return redirect('quizes:quize_board')
