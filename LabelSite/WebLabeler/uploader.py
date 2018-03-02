# encoding: utf-8
import json

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView
from .models import Media
from .response import JSONResponse, response_mimetype
from .serialize import serialize


class MediaCreateView(CreateView):
    model = Media
    template_name = 'WebLabeler/upload.html'
    #fields = "__all__"
    #fields = ['localFile', 'programName']
    fields = ['localFile']

    def form_valid(self, form):
        #print 'upload form valid'

        # default programName = filename
        form.instance.programName = form.instance.localFile.name

        self.object = form.save()
        files = [serialize(self.object, file_attr='localFile')]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        print response
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        #print 'upload form invalid'
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class MediaDeleteView(DeleteView):
    model = Media

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class MediaListView(ListView):
    model = Media

    def render_to_response(self, context, **response_kwargs):
        #files = [ serialize(p, file_attr='localFile') for p in self.get_queryset() ]
        files = []
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
