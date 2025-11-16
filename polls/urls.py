from django.urls import path
from.import views

urlpatterns = [
    path('question', views.index, name = 'index'),
    path('question/detail/<int:question_id>', views.detail, name = 'detail'),
    path('question/result/<int:question_id>', views.results, name = 'results'),
    path('question/vote/<int:question_id>', views.vote, name = 'vote'),
    path('index', views.IndexView.as_view()),
    path('detail/<int:pk>', views.DetailView.as_view()),
    path('result/<int:pk>', views.ResultView.as_view())
]

