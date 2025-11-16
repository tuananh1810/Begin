from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.template import loader
from django.http import HttpResponse, Http404
# Create your views here.

def index(request):
    lates_question_list = Question.objects.order_by('-pub_date')[:5] 
    # lấy tất cả bản ghi trong question 
    # [:5] lấy 5 bản ghi 
    # order by : sắp xếp theo (pub date) mới nhất lên đầu
    template = loader.get_template('polls/index.html')
    context = {
        "latest_question_list" : lates_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExsist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html' , {'Question': question} )


def results(request, question_id):
    response = "1223424 %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("123232432342 %s." % question_id)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'
