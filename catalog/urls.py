from django.urls import path
from . import views
from .views import section_list
from .views import detail_section
from .views import create_test

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('subjects/', views.AllSubjects.as_view(), name='subjects'),
    #path('subject/<int:pk>', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('subject/<int:pk>/', section_list, name='section_list'),

    path('section/<int:pk>/', detail_section, name='section-detail'),#моя проба
]
urlpatterns += [
    # path('section/create/', views.SectionCreate.as_view(), name='section-create'),
    path('section/create/<int:pk>/', views.SectionCreate.as_view(), name='section-create'),
    # path('teacher-subject-test-results/', views.teacher_subject_test_results, name='teacher-subject-test-results'),

    path('groups/<int:test_id>/', views.AllTeacherGroups.as_view(), name='groups'), #для списка групп учителя
    # path('group/<int:pk>/', views.SectionListView.as_view(), name='group'), #для групп учителя
    path('group/<int:test_id>/<int:pk>/', views.teacher_subject_test_results, name='group'), #для групп учителя

    path('edit_test/<int:test_id>/', views.edit_test, name='edit_test'),
    path('pass_test/<int:test_id>/', views.pass_test, name='pass_test'),
    path('test-results/<int:test_id>/<int:score>/', views.test_results, name='test-results'),
    #path('test/create/', views.TestCreate.as_view(), name='test-create'),
    path('create_test/<int:subject_id>/', create_test, name='create_test'),
    path('create_question/', views.create_question, name='create_question'),
    path('lection/create/<int:pk>/', views.LectionCreate.as_view(), name='lection-create'),
    path('video/create/', views.VideoCreate.as_view(), name='video-create'),
]

urlpatterns += [
    path('section/<int:pk>/update/', views.SectionUpdate.as_view(), name='section-update'),
    path('section/<int:pk>/delete/', views.SectionDelete.as_view(), name='section-delete'),

    path('lection/<int:pk>/update/', views.LectionUpdate.as_view(), name='lection-update'),
    path('lection/<int:pk>/delete/', views.LectionDelete.as_view(), name='lection-delete'),

    path('video/<int:pk>/update/', views.VideoUpdate.as_view(), name='video-update'),
    path('video/<int:pk>/delete/', views.VideoDelete.as_view(), name='video-delete'),

    path('test/<int:pk>/delete/', views.TestDelete.as_view(), name='test-delete'),
]

