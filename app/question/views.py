from django.shortcuts import render
from django.views import generic
from .models import *
from django.urls import reverse_lazy
from .forms import QuestionTitleForm
from django.http import HttpResponse
import random
import time
import csv
import matplotlib
import matplotlib.pyplot as plt
import io

matplotlib.use('Agg')
plt.rcParams['font.family'] = 'IPAPGothic'


# Question Title View
class QuestionTitleList(generic.ListView):
    template_name = "question/question_title_list.html"
    model = QuestionTitle

    context_object_name = "question_titles"
    paginate_by = 10

    # # 検索機能
    # def get_queryset(self):
    #     question_titles = QuestionTitle.objects.all()
    #     if 'q' in self.request.GET and self.request.GET['q'] is not None:
    #         q = self.request.GET['q']
    #         question_title = question_titles.filter(question__icontains=q)
    #     # username = self.request.user.username
    #     return question_title


class QuestionTitleDetail(generic.DetailView):
    template_name = "question/question_title_detail.html"
    model = QuestionTitle
    context_object_name = "question_title"


class QuestionTitleCreate(generic.CreateView):
    template_name = "question/question_title_create.html"
    model = QuestionTitle
    # 新規作成フィールド
    form_class = QuestionTitleForm
    success_url = reverse_lazy("question:question_title_list")


class QuestionTitleUpdate(generic.UpdateView):
    template_name = "question/question_title_update.html"
    model = QuestionTitle
    fields = ('title', 'about', 'image')
    context_object_name = "question_title"

    success_url = reverse_lazy("question:question_title_list")


class QuestionTitleDelete(generic.DeleteView):
    template_name = "question/question_title_delete.html"
    model = QuestionTitle
    context_object_name = "question_title"
    success_url = reverse_lazy("question:question_title_list")


# Question View
class QuestionList(generic.ListView):
    template_name = "question/question_list.html"
    model = Question

    context_object_name = "questions"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        length = len(Question.objects.all())
        random_length = random.randrange(length)
        context["one_question"] = Question.objects.all()[random_length]
        print(context)
        return context


def answer_first(request):
    message = ''
    question_id = 0
    question = Question.objects.get(id=question_id + 1)
    start_time = time.time()
    params = {
        'question': question,
        'message': message,
        "start_time": start_time,
    }
    return render(request, 'question/question_answer.html', params)


def answer_question(request):
    message = ''
    done = ""
    if request.method == 'POST':
        start_time = time.time()
        question_id = int(request.POST["id"])
        question = Question.objects.get(id=question_id + 1)

        params = {
            'question': question,
            'message': message,
            "start_time": start_time,
        }
        return render(request, 'question/question_answer.html', params)


def asnwer_correct(request):
    message = ''
    done = ""
    if request.method == 'POST':
        end_time = time.time()
        question_word = request.POST['question']
        answer_word = request.POST['answer'].replace(" ", "").replace("　", "")
        start_time = float(request.POST['start_time'].replace(",", '').replace('"', '').replace("'", ""))
        question_id = int(request.POST['id'])
        answer_time = end_time - start_time

        correct_answer = Question.objects.filter(question=question_word).values_list('correct', flat=True)[0]
        if answer_word != "" and answer_word in correct_answer:
            message = f'正解です。'
            ans = 1
        else:
            message = f'不正解です。正しい答えは「{correct_answer}」です。'
            ans = 2

        question = Question.objects.get(id=question_id)
        count_question = len(Question.objects.filter(experiment_number=question.experiment_number))
        if question_id + 1 > count_question:
            done = "end!!!"

        user = request.user
        # register data
        data = Data(experiment_number=question.experiment_number, user=user.username, judge=str(ans),
                    time=int(answer_time), question_number=question_id,
                    correct=correct_answer, answer=answer_word)
        data.save()

        params = {
            'question': question,
            'message': message,
            "answer_time": answer_time,
            "done": done
        }
        return render(request, 'question/question_answer.html', params)


class AnswerDone(generic.TemplateView):
    template_name = "question/answer_done.html"
    model = Question


def data_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    for data in Data.objects.all():
        writer.writerow(
            [data.pk, data.experiment_number, data.user, data.question_number, data.judge, data.time, data.correct,
             data.answer])
    return response


class PlotView(generic.TemplateView):
    model = Data
    template_name = 'question/plot.html'


def plt2png():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=200)
    s = buf.getvalue()
    buf.close()
    return s


def plot_average_answer_time():
    experiment_number1 = [int(data.time) for data in Data.objects.filter(experiment_number=1)]
    average_time_1 = int(sum(experiment_number1) / len(experiment_number1))
    experiment_number2 = [int(data.time) for data in Data.objects.filter(experiment_number=2)]
    average_time_2 = int(sum(experiment_number2) / len(experiment_number2))
    experiment_number3 = [int(data.time) for data in Data.objects.filter(experiment_number=3)]
    average_time_3 = int(sum(experiment_number3) / len(experiment_number3))
    x_data = [average_time_1, average_time_2, average_time_3]
    plt.plot(x_data, label="average answer time", marker="o", color='red')
    plt.text(0, average_time_1-1, average_time_1)
    plt.text(1, average_time_2-1, average_time_2)
    plt.text(2, average_time_3-1, average_time_3)
    plt.ylabel("average answer time")
    plt.xlabel("experiment_number")
    plt.yticks(range(1, 11))
    plt.xticks([0, 1, 2], ["experiment 1", "experiment 2", "experiment 3"])
    plt.legend()
    plt.show()


def plot_average_judge():
    judge1 = [int(data.judge) for data in Data.objects.filter(experiment_number=1)]
    judge2 = [int(data.judge) for data in Data.objects.filter(experiment_number=2)]
    judge3 = [int(data.judge) for data in Data.objects.filter(experiment_number=3)]
    judge1 = int(sum(judge1) / len(judge1) * 100)
    judge2 = int(sum(judge2) / len(judge2) * 100)
    judge3 = int(sum(judge3) / len(judge3) * 100)
    x_data = [judge1, judge2, judge3]
    plt.plot(x_data, label="average judge", marker="o", color='green')
    plt.text(0, judge1-5, judge1)
    plt.text(1, judge2-5, judge2)
    plt.text(2, judge3-5, judge3)
    plt.ylabel("average judge")
    plt.xlabel("experiment_number")
    plt.yticks(range(0, 101, 10))
    plt.xticks([0, 1, 2], ["experiment 1", "experiment 2", "experiment 3"])
    plt.legend()
    plt.show()


# SVG化
def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s


# 実行するビュー関数
def plot_answer_time(request):
    plot_average_answer_time()
    svg = plt2svg()  # SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response


def plot_judge(request):
    plot_average_judge()
    svg = plt2svg()  # SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response


class QuestionDetail(generic.DetailView):
    template_name = "question/question_detail.html"
    model = QuestionTitle
    context_object_name = "questions"


class QuestionCreate(generic.CreateView):
    template_name = "question/question_create.html"
    model = Question
    success_url = reverse_lazy("question:question_list")


class QuestionUpdate(generic.UpdateView):
    template_name = "question/question_update.html"
    model = Question
    success_url = reverse_lazy("question:question_list")


class QuestionDelete(generic.DeleteView):
    template_name = "question/question_delete.html"
    model = Question
    success_url = reverse_lazy("question:question_list")
