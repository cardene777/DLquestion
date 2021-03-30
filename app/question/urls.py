from django.urls import path
from .views import *


app_name = "question"

urlpatterns = [
    # Question Title URL
    path("question_title_list", QuestionTitleList.as_view(), name="question_title_list"),
    path("question_title_detail/<int:pk>/", QuestionTitleDetail.as_view(), name="question_title_detail"),
    path("question_title_create/", QuestionTitleCreate.as_view(), name="question_title_create"),
    path("question_title_update/<int:pk>/", QuestionTitleUpdate.as_view(), name="question_title_update"),
    path("question_title_delete/<int:pk>/", QuestionTitleDelete.as_view(), name="question_title_delete"),

    # Question URL
    path("question_list/", QuestionList.as_view(), name="question_list"),
    path("question_detail/<int:pk>/", QuestionDetail.as_view(), name="question_detail"),
    path("question_create/", QuestionCreate.as_view(), name="question_create"),
    path("question_update/<int:pk>/", QuestionUpdate.as_view(), name="question_update"),
    path("question_delete/<int:pk>/", QuestionDelete.as_view(), name="question_delete"),

    # answer
    path("answer_question/", answer_question, name="answer_question"),
    path("answer_correct/", asnwer_correct, name="asnwer_correct"),
    path("answer_first/", answer_first, name="answer_first"),
    path("answer_done/", AnswerDone.as_view(), name="answer_done"),
    path("export/", data_export, name="export"),

    # plot
    path("plot_list/", PlotView.as_view(), name="plot_list"),
    path("plot_answer_time/", plot_answer_time, name="plot_answer_time"),
    path("plot_judge/", plot_judge, name="plot_judge"),
]
