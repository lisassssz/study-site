from django.contrib import admin

from .models import Subject,Section, Test, Question, Answer, Student, TakenTest, Lection, Video, MyGroup

admin.site.register(Subject)
admin.site.register(Section)
admin.site.register(Lection)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Student)
admin.site.register(TakenTest)
admin.site.register(Video)
admin.site.register(MyGroup)