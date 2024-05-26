from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render

class IndexView(TemplateView):
    template_name = "base.html"
    
class FaceRecognitionView(View):
    template_name = 'faceRecognition.html'
    
    def get(self, request):
        return render(request, self.template_name, context= {})