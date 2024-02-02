from django.db import models


from django.db.models import Q

from django.contrib.auth.models import User
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to=Q(groups__name='Teachers'))
    image = models.ImageField(upload_to='subject_images/', null=True, blank=True)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('subject-detail', args=[str(self.id)])

class Section(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('section-detail', args=[str(self.id)])
    
    class Meta:
        permissions = (("can__section", "Work with section"),)

class Test(models.Model):
    title = models.CharField(max_length=200)
    questions = models.ManyToManyField('Question')
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True)
    class Meta:
        permissions = (("can_test", "Work with test"),)

    def __str__(self):
        return self.title or "Без названия"

class Question(models.Model):
    question_text = models.CharField(max_length=500,null=True)
    answers = models.ManyToManyField('Answer')
    
    class Meta:
        permissions = (("can_question", "Work with question"),)

    def __str__(self):
        return self.question_text or "Без текста"

class Answer(models.Model):
    answer_text = models.CharField(max_length=500, null=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        permissions = (("can_answer", "Work with answer"),)

    def __str__(self):
        return self.answer_text or "Без текста"


class ExtraQuestion(models.Model):
    question_text = models.CharField(max_length=500)
    # Возможно, вам нужно добавить поле, связывающее вопрос с тестом, если оно необходимо

class ExtraAnswer(models.Model):
    question = models.ForeignKey(ExtraQuestion, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    
#проба
from django.core.validators import FileExtensionValidator

def get_upload_path(instance, filename):
    # Функция для указания пути сохранения загруженного файла
    return f"lections/{instance.section}/{filename}"

class Lection(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=get_upload_path,validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt'])],blank=True )
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True)
    class Meta:
        permissions = (("can_lection", "Work with lection"),)

    def __str__(self):
        return self.title
    
    def get_file_url(self):
        return self.file.url if self.file else ''
    
    def get_absolute_url(self):
        return reverse('section-detail', args=[str(self.section.id)])
    


class Video(models.Model):
    title = models.CharField(max_length=100)
    reference = models.URLField()
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True)
    class Meta:
        permissions = (("can_video", "Work with video"),)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('section-detail', args=[str(self.section.id)])
#конец пробы

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=30, null=True)
    class Meta:
        permissions = (("can_pass", "Can pass test"),)
    def __str__(self):
        return self.user.username

class TakenTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    class Meta:
        permissions = (("can_watch", "See tests results"),)
    def __str__(self):
        return f"Оценка для {self.student.user.last_name} {self.student.user.first_name}: {self.score}"
    
class MyGroup(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ManyToManyField(User)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('group-detail', args=[str(self.id)])