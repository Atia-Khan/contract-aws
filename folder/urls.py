from django.urls import path
from folder import views
from .views import get_csrf_token

app_name = 'folder'

urlpatterns = [
    path('add/', views.FolderCreateView.as_view(), name='add'),
    path('list/', views.FolderListView.as_view(), name='list'),
    path('details/<int:folder_id>/', views.FolderDetailsView.as_view(), name='details'),
    path('<int:folder_id>/file/<int:pk>/delete/', views.FileDeleteView.as_view(), name='file-delete'),
    path('edit/<int:pk>/', views.FolderUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.FolderDeleteView.as_view(), name='delete'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('details/<int:folder_id>/subfolders/', views.FolderDetailsSubfoldersView.as_view(), name='details_subfolders'),
    path('details/<int:folder_id>/edit/<int:subfolder_id>/', views.FolderDetailsEditView.as_view(), name='details_edit'),
    path('details/<int:folder_id>/delete/<int:subfolder_id>/', views.FolderDetailsDeleteView.as_view(), name='details_delete'),
]