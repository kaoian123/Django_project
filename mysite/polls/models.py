"""polls 應用程式的資料模型。"""
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """代表投票問題的模型。"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.question_text)

    def was_published_recently(self):
        """檢查問題是否在最近發布。"""
        return self.pub_date >= timezone.now() - timezone.timedelta(days=1)


class Choice(models.Model):
    """代表投票選項的模型。"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.choice_text)
