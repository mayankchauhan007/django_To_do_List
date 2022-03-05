from django.urls import path
from home.views import taskDelete, taskList , taskDetail , taskCreate , taskUpdate , DeleteView , CustomLoginView , registerPage
from django.contrib.auth.views import LogoutView
urlpatterns = [

    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('register/',registerPage.as_view(), name = 'register'),

    path('', taskList.as_view(),name='tasks'),
    path('task/<int:pk>/', taskDetail.as_view(),name='task'),
    path('task-create/', taskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/', taskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/', taskDelete.as_view(),name='task-delete'),
]
