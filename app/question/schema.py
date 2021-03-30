import graphene
from graphene_django import DjangoObjectType
from .models import QuestionTitle, Question



class QuestionTitleType(DjangoObjectType):
    class Meta:
        model = QuestionTitle
        fields = ("title", "about", "image")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "question", "correct")


class Query(graphene.ObjectType):
    question_titles = graphene.List(QuestionTitleType)
    questions = graphene.List(QuestionType)

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return QuestionTitle.objects.all()

    def resolve_category_by_name(root, info, name):
        return Question.objects.all()


schema = graphene.Schema(query=Query)
