from django.db import models

# Create your models here.


class Users(models.Model):
    u_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=40)
    email = models.EmailField()
    password = models.CharField(max_length=30)

class Subject(models.Model):
    subject_id=models.IntegerField(primary_key=True)
    subject_name=models.CharField(max_length=30)

class Topic(models.Model):
    topic_id=models.IntegerField(primary_key=True)
    topic_name=models.CharField(max_length=30)
    subject_name=models.CharField(max_length=30)
    last_date=models.DateField()

class Assignmentt(models.Model):
    assignment_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=40)
    assignment_name = models.CharField(max_length=100)
    file = models.FileField()
    status=models.CharField(max_length=20)


class Plagiarism_Value(models.Model):
    p_id = models.IntegerField(primary_key=True)
    file = models.CharField(max_length=100)
    cosine_value = models.CharField(max_length=50)


class Match(models.Model):
    m_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=40)
    file = models.CharField(max_length=100)
    matching_content = models.TextField()
