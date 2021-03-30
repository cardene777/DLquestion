from django.test import TestCase
import sys
sys.path.append('../../')
from app.models import Question, QuestionTitle


class QuestionTitleModelTests(TestCase):
    def test_question_title_empty(self):
        saved_question_titles = QuestionTitle.objects.all()
        self.assertEqual(saved_question_titles.count(), 0)

    def test_question_title_not_empty(self):
        question_titles = QuestionTitle(title="test1", about="test1")
        question_titles.save()
        print("###########################################")
        print(question_titles.id)
        print("###########################################")
        saved_question_titles = QuestionTitle.objects.all()
        self.assertEqual(saved_question_titles.count(), 1)


# class QuestionModelTests(TestCase):
#     def test_question_empty(self):
#         saved_questions = Question.objects.all()
#         self.assertEqual(saved_questions.count(), 0)
#
#     def test_question_not_empty(self):
#         questions = Question()
#         print(questions)
#         questions.save()
#         saved_questions = Question.objects.all()
#         self.assertEqual(saved_questions.count(), 1)
