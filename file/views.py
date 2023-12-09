import os
from wsgiref.util import FileWrapper
from django.views.decorators.csrf import csrf_exempt
from taggit.models import Tag
from django.http import JsonResponse
from django.core.serializers import serialize
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView

from file.forms import FileForm
from file.models import File
from django.views.decorators.http import require_POST

from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import ColorTag
from folder.models import Folder
from django.http import JsonResponse, Http404

@csrf_exempt
def create_tag(request):
    try:
        tag_name = request.POST.get('tag_name')
        tag_color = request.POST.get('tag_color')

        print(f"Received tag name: {tag_name}, color: {tag_color}")

        if tag_name is not None and tag_name.strip():
            tag, created = ColorTag.objects.get_or_create(name=tag_name, color=tag_color)
            return JsonResponse({'tag': tag.name, 'color': tag.color})
        else:
            return JsonResponse({'error': 'Tag name cannot be null or empty'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)

    
    
def get_tags(request):
    tags = ColorTag.objects.values('name','id','color')
    return JsonResponse({'tags': list(tags)})

class TagUpdateView(UpdateView):
    model = ColorTag
    fields = ['name', 'color']
    template_name = 'file/edit_tag.html'  # Create an HTML template for editing tags
    success_url = reverse_lazy('file:get_tags')
    
class TagDeleteView(DeleteView):
    model = ColorTag
    template_name = 'file/confirm_delete_tag.html'  # Create an HTML template for confirming tag deletion
    success_url = reverse_lazy('file:get_tags')
    
class FileDeleteView(DeleteView):
    model = File
    template_name = 'file/confirm_delete.html'
    success_url = reverse_lazy('file:get_tags')



class FileCreateView(CreateView):
    form_class = FileForm
    template_name = 'file/add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_url'] = reverse('file:add')
        context['add_folder'] = reverse('folder:add')
        context['add_file'] = reverse('file:add')
        return context

    def get_success_url(self):
        return reverse('folder:list')
    def form_valid(self, form):
        try:
            # Create a new File instance
            file_instance = form.save(commit=False)
            file_instance.folder = form.cleaned_data['folder']
            file_instance.file = form.cleaned_data['file']
            file_instance.save()

            # Process existing tags
            existing_tags = form.cleaned_data.get('existing_tags')
            new_tag = form.cleaned_data.get('new_tag')

            if existing_tags:
                file_instance.tags.add(*existing_tags)

            if new_tag:
                tag, created = ColorTag.objects.get_or_create(name=new_tag)
                file_instance.tags.add(tag)

            return super().form_valid(form)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    

class FileListView(ListView):
    model = File
    context_object_name = 'file_list'
    template_name = 'file/list.html'

    def render_to_response(self, context, **response_kwargs):
        file_list = context[self.context_object_name]

        # Serialize the data with tags, including the color
        file_list_data = [
            {
                "model": "file.file",
                "pk": file.pk,
                "fields": {
                    "name": file.name,
                    "tags": [
                        {"name": tag.name, "color": tag.color} for tag in file.tags.all()
                    ],  # Include tags with name and color
                    "folder": file.folder.name if file.folder else None,
                },
            }
            for file in file_list
        ]

        # Use JsonResponse to handle serialization
        return JsonResponse({'file_list': file_list_data}, safe=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Include tags in the queryset to avoid N+1 query issues
        queryset = queryset.select_related('folder').prefetch_related('tags')
        return queryset

    
class FileDownloadView(View):
    def get(self, request, pk):
        file = File.objects.filter(pk=pk).first()
        filename = file.file.path
        wrapper = FileWrapper(file.file)
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % file.name
        response['Content-Length'] = os.path.getsize(filename)
        return response
    
    
class FileUpdateView(View):
    def post(self, request, *args, **kwargs):
        file_instance = get_object_or_404(File, pk=kwargs['pk'])

        # Print file details before update
        print(f"File Details Before Update - Name: {file_instance.name}, Folder: {file_instance.folder}")

        try:
            # Process existing tags
            existing_tags = request.POST.getlist('existing_tags', [])
            new_tag = request.POST.get('new_tag', '')

            # If existing_tags is provided, add only the ones that already exist
            if existing_tags:
                existing_tags = ColorTag.objects.filter(id__in=existing_tags)
                file_instance.tags.set(existing_tags)

            # If new_tag is provided, add it (whether it exists or not)
            if new_tag:
                tag_instance, created = ColorTag.objects.get_or_create(name=new_tag)
                file_instance.tags.add(tag_instance)

            # Process folder only if it is explicitly provided in the request body
            folder_id = request.POST.get('folder_id', None)
            if folder_id is not None:
                folder = get_object_or_404(Folder, pk=folder_id)
                file_instance.folder = folder

            file_instance.save()

            # Print file details after update
            print(f"File Details After Update - Name: {file_instance.name}, Folder: {file_instance.folder}")

            return JsonResponse({'success': 'File updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
def get_pdf_url(request, pk):
    try:
        file_instance = get_object_or_404(File, pk=pk)
        pdf_url = file_instance.file.url
        print(f"PDF URL: {pdf_url}")
        return JsonResponse({'pdfUrl': pdf_url})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)