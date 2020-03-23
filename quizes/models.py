from django.db import models

# Create your models here.


class Topic(models.Model):
    topic_name = models.CharField(max_length=255)

    def __str__(self):
        return self.topic_name

    def get_number_questions(self):
        return self.topic_question.all().count()


class Question(models.Model):
    topic = models.ForeignKey(
        Topic, related_name='topic_question', on_delete=models.CASCADE)
    question_name = models.CharField(max_length=255)

    def __str__(self):
        return self.question_name


class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='question_option')
    option_name = models.CharField(max_length=255)
    wright_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.option_name
