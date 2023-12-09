from django.urls import path
from file import views
from .views import get_tags, create_tag

app_name = 'file'


urlpatterns = [
    path('add/', views.FileCreateView.as_view(), name='add'),
    path('list/', views.FileListView.as_view(), name='list'),
    path('<int:pk>/download/', views.FileDownloadView.as_view(), name='download'),
    path('delete/<int:pk>/', views.FileDeleteView.as_view(), name='file_delete'),
    path('get_tags/', get_tags, name='get_tags'),
    path('create_tag/', create_tag, name='create_tag'),
    path('edit_tag/<int:pk>/', views.TagUpdateView.as_view(), name='edit_tag'),
    path('delete_tag/<int:pk>/', views.TagDeleteView.as_view(), name='delete_tag'),
    path('update/<int:pk>/', views.FileUpdateView.as_view(), name='file_update'),
    path('api/files/<int:pk>/{pdf-url}/', views.get_pdf_url, name='get_pdf_url'),

]
