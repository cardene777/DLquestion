from django.db import models


class QuestionTitle(models.Model):
    class Meta:
        verbose_name = '問題タイトル'
        verbose_name_plural = '問題タイトル'

    title = models.CharField(
        verbose_name="問題タイトル",
        max_length=100,
    )

    about = models.TextField(
        verbose_name="問題概要",
        blank=True
    )

    image = models.ImageField(
        verbose_name="問題画像",
        upload_to="images/",
        default="images/question.png",
        blank=True,
    )

    def __str__(self):
        return f"{self.title}"


class Question(models.Model):
    class Meta:
        verbose_name = '問題'
        verbose_name_plural = '問題'

    experiment_number = models.IntegerField(
        verbose_name="実験番号",
        default=1
    )
    number = models.IntegerField(
        verbose_name="問題番号",
        default=0
    )
    title = models.ForeignKey(
        QuestionTitle,
        verbose_name="タイトル",
        on_delete=models.CASCADE,
        default=QuestionTitle,
        related_name="title_question"
    )

    question = models.CharField(
        verbose_name="問題",
        max_length=200,
    )

    correct = models.CharField(
        verbose_name="正解",
        max_length=200,
    )

    def __str__(self):
        return f"{self.title} {self.question} {self.correct} {self.number}"


class Data(models.Model):
    class Meta:
        verbose_name = '回答データ'
        verbose_name_plural = '回答データ'

    experiment_number = models.IntegerField(
        verbose_name="実験番号",
        default=1,
    )
    user = models.CharField(
        verbose_name="ユーザー名",
        max_length=50,
        default="none"
    )

    judge = models.CharField(
        verbose_name="正誤",
        max_length=20,
        default="none"
    )

    time = models.IntegerField(
        verbose_name="回答時間",
        default=0
    )

    question_number = models.IntegerField(
        verbose_name="問題番号",
        default=0
    )

    correct = models.CharField(
        verbose_name="正解",
        max_length=100,
        default="none"
    )

    answer = models.CharField(
        verbose_name="回答",
        max_length=100,
        blank=True
    )

    def __str__(self):
        return f"{self.experiment_number} {self.user} {self.judge} {self.time} {self.question_number} {self.correct} {self.answer}"
