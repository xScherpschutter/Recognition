from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.generic import View
import cv2
from django.views.decorators import gzip
from plateRecognition.components.plate_detection import plate_detection
# Create your views here.

class PlateView(View):
    template_name = 'plateRecognition.html'
    
    def get(self, request):
        return render(request, self.template_name, context ={})
        
@gzip.gzip_page        
def video_stream(request):
    return StreamingHttpResponse(plate_detection(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')      