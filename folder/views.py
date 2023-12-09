from django.urls import reverse
from django.views.generic import ListView, CreateView
from django.views import View
from folder.forms import FolderForm
from folder.models import Folder
from file.forms import FileForm
from file.models import File
# folder/views.py
from django.shortcuts import get_object_or_404
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from file.models import File
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from folder.models import Folder
from folder.forms import FolderForm
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from folder.models import Folder
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})
class FolderDeleteView(DeleteView):
    model = Folder
    template_name = 'folder/confirm_folder_delete.html'
    success_url = reverse_lazy('folder:list')
class FolderUpdateView(UpdateView):
    model = Folder
    form_class = FolderForm
    template_name = 'folder/edit.html'
    success_url = reverse_lazy('folder:list')
class FileDeleteView(DeleteView):
    model = File
    success_url = reverse_lazy('folder:list')
class FolderCreateView(CreateView):
    form_class = FolderForm
    template_name = 'folder/add.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_url'] = reverse('folder:add')
        context['add_folder'] = reverse('folder:add')
        context['add_file'] = reverse('file:add')
        return context
    def get_success_url(self):
        return reverse('folder:list')
class FolderListView(ListView):
    def get_queryset(self):
        pk = self.request.GET.get('id')
        queryset = Folder.objects.all()
        if pk:
            queryset = queryset.filter(parent__pk=pk)
        else:
            queryset = queryset.filter(parent=None)
        order_by = self.request.GET.get('sort')
        if order_by == 'time':
            queryset = queryset.order_by('-created_at')
        elif order_by == 'name':
            queryset = queryset.order_by('name')
        return queryset
    def get_file_query(self, pk):
        file_query = File.objects.all()
        if pk:
            file_query = file_query.filter(folder__pk=pk)
        else:
            file_query = file_query.filter(folder=None)
        order_by = self.request.GET.get('sort')
        if order_by == 'time':
            file_query = file_query.order_by('-created_at')
        elif order_by == 'name':
            file_query = file_query.order_by('name')
        return file_query
    @staticmethod
    def get_parent_folder_link(pk):
        parent_folder = []
        if pk:
            folder = Folder.objects.get(pk=pk)
            parent_folder.append({
                'text': folder.name,
                'link': reverse('folder:list') + f'?id={folder.pk}',
            })
            while folder.parent:
                parent_folder.append({
                    'text': folder.parent.name,
                    'link': reverse('folder:list') + f'?id={folder.parent.pk}',
                })
                folder = folder.parent
            parent_folder.reverse()
        return parent_folder
    def render_to_response(self, context, **response_kwargs):
        pk = self.request.GET.get('id')
        folder_list = [
            {'id': folder.id, 'name': folder.name} for folder in self.get_queryset()
        ]
        file_list = [
            {'id': file.id, 'name': file.name} for file in self.get_file_query(pk)
        ]
        parent_folder = [
            {'text': folder['text'], 'link': folder['link']} for folder in self.get_parent_folder_link(pk)
        ]
        response_data = {
            'folder_list': folder_list,
            'file_list': file_list,
            'parent_folder': parent_folder,
        }
        return JsonResponse(response_data)
class FolderDetailsView(View):
    def get(self, request, folder_id):
        try:
            folder = Folder.objects.get(pk=folder_id)
            subfolders = Folder.objects.filter(parent=folder)
            files = File.objects.filter(folder=folder)
            folder_list = [{'id': subfolder.id, 'name': subfolder.name} for subfolder in subfolders]
            file_list = [{'id': file.id, 'name': file.name} for file in files]
            response_data = {
                'folder_list': folder_list,
                'file_list': file_list,
                'parent_folder': [],  # You can implement this if needed
            }
            return JsonResponse(response_data)
        except Folder.DoesNotExist:
            return JsonResponse({'error': 'Folder not found'}, status=404)
class FolderDetailsSubfoldersView(View):
    def get(self, request, folder_id):
        try:
            folder = Folder.objects.get(pk=folder_id)
            subfolders = Folder.objects.filter(parent=folder)
            folder_list = [{'id': subfolder.id, 'name': subfolder.name} for subfolder in subfolders]
            response_data = {
                'folder_list': folder_list,
            }
            return JsonResponse(response_data)
        except Folder.DoesNotExist:
            return JsonResponse({'error': 'Folder not found'}, status=404)
class FolderDetailsEditView(View):
    def post(self, request, folder_id, subfolder_id):
        try:
            subfolder = get_object_or_404(Folder, pk=subfolder_id, parent__pk=folder_id)
            form = FolderForm(request.POST, instance=subfolder)
            if form.is_valid():
                subfolder.name = form.cleaned_data['name']  # Update only the 'name' field
                subfolder.save(update_fields=['name'])  # Save the updated subfolder
                return JsonResponse({'message': 'Subfolder name updated successfully'})
            else:
                return JsonResponse({'error': 'Invalid form data'}, status=400)
        except Folder.DoesNotExist:
            return JsonResponse({'error': 'Subfolder not found'}, status=404)
class FolderDetailsDeleteView(View):
    def post(self, request, folder_id, subfolder_id):
        try:
            # Assuming subfolder_id is a valid ID for the subfolder
            subfolder = Folder.objects.get(pk=subfolder_id, parent__id=folder_id)
            subfolder.delete()
            return JsonResponse({'message': 'Subfolder deleted successfully'})
        except Folder.DoesNotExist:
            return JsonResponse({'error': 'Subfolder not found'}, status=404)