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

# def gen(camera):
#     while True:
#         ret, frame = camera.read()
#         if not ret:
#             break
#         _, jpeg = cv2.imencode('.jpg', frame)
#         frame = jpeg.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
@gzip.gzip_page        
def video_stream(request):
    return StreamingHttpResponse(plate_detection(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')      