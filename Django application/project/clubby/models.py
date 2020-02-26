from django.db import models
import datetime

# This is the models file, here we create the django objects we need for our application to work
# these first two models are here as testing grounds and should be deleted later on.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    # this is a reference to the Question class as a many to one configuration
    # if you are using VSCode you can see that by hovering on ForeignKey
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text