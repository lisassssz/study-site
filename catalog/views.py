from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Section
# Create your views here.
from .models import Subject, Test, Question, Answer, Student, TakenTest, Section, Lection, Video

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_subjects=Subject.objects.all().count()
    num_students=Student.objects.all().count()
    
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_subjects':num_subjects,'num_students':num_students},
    )

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

class AllSubjects(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = Subject
    template_name ='catalog/subject_list_all.html'
    # paginate_by = 6 вернуть, а имеено убрала для поиска

    # def get_queryset(self):
    #     return Subject.objects.all()
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Teachers').exists():
            # фильтрация предметов для учителей
            return Subject.objects.filter(teacher=user)
        elif user.groups.filter(name='All Students').exists():
            # фильтрация предметов для студентов
            return Subject.objects.all()
        else:
            # фильтрация предметов для остальных пользователей
            return Subject.objects.none()



from django.contrib.auth.mixins import PermissionRequiredMixin
from django import forms

# ABOUT SECTIONS

class SectionCreateForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'
        labels = {
            "name": "Название",
            "subject": "Предмет"
        }

class SectionCreate(PermissionRequiredMixin, CreateView):
    model = Section
    permission_required = 'catalog.can__section'
    form_class = SectionCreateForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        subjects = Subject.objects.filter(teacher=user)
        form.fields['subject'].queryset = subjects
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Используйте параметр pk, а не subject_id
        context['current_subject_id'] = self.kwargs.get('pk')
        # Добавляем текущий предмет в контекст
        context['current_subject'] = get_object_or_404(Subject, id=context['current_subject_id'])
        return context

    def form_valid(self, form):
        subject_id = self.kwargs.get('pk')
        if subject_id:
            form.instance.subject = get_object_or_404(Subject, id=subject_id)
        return super().form_valid(form)  

# class SectionCreate(PermissionRequiredMixin,LoginRequiredMixin, CreateView):
#     model = Section
#     permission_required = 'catalog.can__section'
#     fields = '__all__'
from django.urls import reverse_lazy

class SectionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Section
    permission_required = 'catalog.can__section'
    form_class = SectionCreateForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        subjects = Subject.objects.filter(teacher=user)
        form.fields['subject'].queryset = subjects
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Используйте параметр pk
        context['current_subject_id'] = self.kwargs.get('pk')
        # Добавляем текущий предмет в контекст
        context['current_subject'] = get_object_or_404(Subject, id=context['current_subject_id'])
        return context

    def get_success_url(self):
        # Возвращаем URL для списка разделов
        subject_id = self.object.subject.id
        return reverse('section_list', args=[subject_id])
    
class SectionDelete(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    model = Section
    permission_required = 'catalog.can__section'
    success_url = reverse_lazy('section_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавим переменные в контекст
        context['current_subject'] = self.object.subject
        context['section'] = self.object
        return context
    def get_success_url(self):
        # Вернуть URL для списка лекций
        subject_id = self.object.subject.id
        return reverse('section_list', args=[subject_id])


# ABOUT TESTS


# class TestCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
#     model = Test
#     permission_required = 'catalog.can_test'
#     fields = '__all__'
from django.shortcuts import render, redirect
# from .forms import TestForm, QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def create_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text', '')  # Изменено на 'question_text'
        answer_text = request.POST.get('answer_text', '')  # Изменено на 'answer_text'

        if question_text and answer_text:
            # Создание нового вопроса
            question = Question.objects.create(question_text=question_text)
            
            # Создание нового ответа, связанного с вопросом
            answer = Answer.objects.create(answer_text=answer_text, question=question)

            # Возвращение идентификаторов созданных вопроса и ответа в формате JSON
            return JsonResponse({'success': True, 'question_id': question.id, 'answer_id': answer.id})
        else:
            return JsonResponse({'success': False, 'error': 'Заполните все поля'})
    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})

from django.forms import formset_factory, modelformset_factory
from .forms import CreateTestForm, QuestionForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Test
# from .forms import TestForm, QuestionForm, AnswerForm

@login_required
def create_test(request,subject_id):
    subject = Subject.objects.get(id=subject_id)
    sections = Section.objects.filter(subject=subject)
    
    if request.method == 'POST':
        create_test_form = CreateTestForm(request.POST)
        question_form = QuestionForm(request.POST)

        if create_test_form.is_valid() and question_form.is_valid():
            title = create_test_form.cleaned_data['title']
            section = create_test_form.cleaned_data['section']  # Получение выбранного раздела
            # Создаем тест
            test = Test.objects.create(title=title, section=section)

            # Создаем вопросы и ответы
            questions = request.POST.getlist('questions')
            answers = request.POST.getlist('answers')

            for i in range(len(questions)):
                question_text = questions[i]
                answer_text = answers[i]
                question = Question.objects.create(question_text=question_text)
                answer = Answer.objects.create(answer_text=answer_text, is_correct=True, question=question)
                test.questions.add(question)

            return redirect('section-detail', pk=section.id)  # Перенаправьте на список тестов или другую страницу

    else:
        create_test_form = CreateTestForm(subject=subject)
        question_form = QuestionForm()

    return render(request, 'create_test.html', {'create_test_form': create_test_form, 'question_form': question_form, 'sections': sections})

#
from .forms import EditTestForm
from django.shortcuts import render, get_object_or_404, redirect
@login_required
def edit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    sections = Section.objects.all()

    if request.method == 'POST':
        edit_test_form = EditTestForm(request.POST, instance=test)
        question_form = QuestionForm(request.POST)

        if edit_test_form.is_valid():
            edit_test_form.save()

            questions = request.POST.getlist('questions')
            answers = request.POST.getlist('answers')

            for i in range(len(questions)):
                question_text = questions[i]
                answer_text = answers[i]

                if i < test.questions.count():
                    question = test.questions.all()[i]
                    question.question_text = question_text
                    question.save()
                else:
                    question = Question.objects.create(question_text=question_text)
                    test.questions.add(question)

                answer = question.answers.first()
                if answer:
                    answer.answer_text = answer_text
                    answer.save()
                else:
                    answer = Answer.objects.create(answer_text=answer_text, is_correct=True, question=question)

            return redirect('section-detail', pk=test.section.id)

    else:
        edit_test_form = EditTestForm(instance=test)
        question_form = QuestionForm()

    return render(request, 'catalog/edit_test.html', {'edit_test_form': edit_test_form, 'question_form': question_form, 'sections': sections, 'test': test})
#
@login_required
def pass_test(request, test_id):
    test = Test.objects.get(pk=test_id)
    questions = test.questions.all()
    
    if request.method == 'POST':
        # Обработка отправленных ответов
        score = 0
        total_questions = questions.count()
        
        for question in questions:
            user_answer = request.POST.get(str(question.id))
            if user_answer:
                # Получите правильный ответ для вопроса
                correct_answer = question.answers.filter(is_correct=True).first()

                if correct_answer and user_answer.lower() == correct_answer.answer_text.lower():
                    score += 1

        # Рассчитайте оценку (ваш логика)
        max_score = total_questions
        # user_score = (score / max_score) * 10
        user_score = (score / total_questions) * 10
        # Сохраните результаты в модель, если нужно
         # Сохраните результаты в модель TakenTest
        taken_test = TakenTest(test=test, student=request.user.student, score=user_score)
        taken_test.save()
        # например, test.user_scores.create(user=request.user, score=user_score)
        # Перенаправьтесь на страницу с результатами
        return redirect('test-results', test_id=test.id, score=int(user_score))
        
    return render(request, 'catalog/pass_test.html', {'test': test, 'questions': questions})

def test_results(request, test_id, score):
    test = Test.objects.get(pk=test_id)
    return render(request, 'catalog/test_results.html', {'test': test, 'score': score})

# пробник
def teacher_subject_test_results(request,test_id,pk):
    # test_id = request.GET.get('test_id')
    cur_test=Test.objects.get(pk=test_id)
    cur_group = MyGroup.objects.get(pk=pk)
    teacher = request.user  # Получаем текущего учителя (предполагается, что учитель авторизован)
    taken_tests = TakenTest.objects.filter(test__section__subject__teacher=teacher,student__group=cur_group, test=cur_test)
    return render(request, 'catalog/teacher_subject_test_results.html', {'taken_tests': taken_tests, 'cur_test': cur_test})



class TestDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Test
    permission_required = 'catalog.can_test'
    def get_success_url(self):
        # Вернуть URL для списка лекций
        section_id = self.object.section.id
        return reverse('section-detail', args=[section_id])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_subject'] = self.object.section.subject
        context['section'] = self.object.section
        return context

#About sections
@login_required
def section_list(request, pk):
    subject = Subject.objects.get(id=pk)
    sections = Section.objects.filter(subject=subject)
    return render(request, 'catalog/section_list.html', {'current_subject': subject, 'sections': sections})

@login_required
def detail_section(request,pk):
    section = Section.objects.get(id=pk)
    tests = Test.objects.filter(section=section)
    lections = Lection.objects.filter(section=section)
    videos = Video.objects.filter(section=section)
    subject = section.subject
    return render(request, 'catalog/detail_section.html',{'tests': tests, 'section': section, 'lections': lections, 'videos': videos, 'subject': subject,'current_subject': subject})

# ABOUT LECTIONS

class LectionCreateForm(forms.ModelForm):
    class Meta:
        model = Lection
        fields = '__all__'
        labels = {
            "title": "Название",
            "section": "Раздел",
            "file": "Файл"
        }
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }

class LectionCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Lection
    permission_required = 'catalog.can_lection'
    form_class = LectionCreateForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        sections = Section.objects.filter(subject__teacher=user)
        form.fields['section'].queryset = sections
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Используем параметр pk
        context['current_section_id'] = self.kwargs.get('pk')
        # Добавляем текущий раздел в контекст
        context['current_section'] = get_object_or_404(Section, id=context['current_section_id'])
        return context

    def form_valid(self, form):
        # Получаем текущий раздел из URL
        current_section_id = self.kwargs.get('pk')
        current_section = get_object_or_404(Section, id=current_section_id)
        # Устанавливаем текущий раздел в контекст
        form.instance.section = current_section
        return super().form_valid(form)

from django.shortcuts import redirect

class LectionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Lection
    permission_required = 'catalog.can_lection'
    form_class = LectionCreateForm
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        sections = Section.objects.filter(subject__teacher=user)
        form.fields['section'].queryset = sections
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_subject'] = self.object.section.subject
        context['section'] = self.object.section
        return context
    
from django.urls import reverse

class LectionDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Lection
    permission_required = 'catalog.can_lection'
    def get_success_url(self):
        # Вернуть URL для списка лекций
        section_id = self.object.section.id
        return reverse('section-detail', args=[section_id])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_subject'] = self.object.section.subject
        context['section'] = self.object.section
        return context

# ABOUT Videos
class VideoCreateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'
        labels = {
            "title": "Название",
            "section": "Раздел",
            "reference": "Ссылка"
        }
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }

class VideoCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Video
    permission_required = 'catalog.can_video'
    form_class = VideoCreateForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Получаем текущего пользователя
        user = self.request.user
        # Фильтруем разделы по привязке к текущему пользователю
        sections = Section.objects.filter(subject__teacher=user)
        form.fields['section'].queryset = sections
        return form

class VideoUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Video
    permission_required = 'catalog.can_video'
    form_class = VideoCreateForm
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Получаем текущего пользователя
        user = self.request.user
        # Фильтруем разделы по привязке к текущему пользователю
        sections = Section.objects.filter(subject__teacher=user)
        form.fields['section'].queryset = sections
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_subject'] = self.object.section.subject
        context['section'] = self.object.section
        return context
    
from django.urls import reverse

class VideoDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Video
    permission_required = 'catalog.can_video'
    def get_success_url(self):
        # Вернуть URL для списка лекций
        section_id = self.object.section.id
        return reverse('section-detail', args=[section_id])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_subject'] = self.object.section.subject
        context['section'] = self.object.section
        return context

# список групп учителя
from .models import MyGroup

class AllTeacherGroups(LoginRequiredMixin,generic.ListView):
    model = MyGroup
    template_name ='catalog/all_teacher_groups.html'
    paginate_by = 10
    

    def get_queryset(self):
        user = self.request.user
        test_id = self.kwargs.get('test_id')  # Получение значения test_id из URL

        # Ваш текущий тест
        current_test = Test.objects.get(id=test_id)
        return MyGroup.objects.filter(teacher=user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_id'] = self.kwargs.get('test_id')
        return context
# полсе перехода по группе
# def detail_group(request,pk):
#     subject = Subject.objects.get(id=pk)
    
#     section = Section.objects.filter(subject=subject)
#     tests = Test.objects.filter(section=section)
#     return render(request, 'catalog/detail_group.html',{'tests': tests, 'sections': section, 'subject': subject})

# def section_list(request, pk):
#     subject = Subject.objects.get(id=pk)
#     sections = Section.objects.filter(subject=subject)
#     return render(request, 'catalog/section_list.html', {'subject': subject, 'sections': sections})
class SectionListView(generic.ListView):
    model = Section
    template_name = 'catalog/detail_group.html'
    context_object_name = 'sections'

    def get_queryset(self):
        return Section.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tests_by_section = {}
        
        for section in context['sections']:
            tests = Test.objects.filter(section=section)
            tests_by_section[section] = tests

        context['tests_by_section'] = tests_by_section
        return context