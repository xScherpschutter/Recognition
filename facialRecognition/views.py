from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
import json
import base64
import os
import tempfile
from facialRecognition.components.face_recognition import recognize_face

class IndexView(TemplateView):
    template_name = "base.html"
    
class FaceRecognitionView(View):
    template_name = 'faceRecognition.html'
    
    def get(self, request):
        return render(request, self.template_name, context= {})
    
    def post(self, request, *args, **kwargs):
        try:
            
            body = request.body.decode('utf-8')
            body_data = json.loads(body)
               
            
            image_data_base64 = body_data['image']
            dni = str(body_data['dni'])
            
            image_data_binary = base64.b64decode(image_data_base64.split(',')[1])
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            temp_file.write(image_data_binary)
            temp_file.close()
            image_path = temp_file.name

            success, message = recognize_face(image_path, dni)
            os.unlink(temp_file.name)
            
            if success:
                return JsonResponse({'success': True, 'dni': message})
            
            return JsonResponse({'success': False, 'dni': message})
        
        except Exception as e:
            print('Error: {}'.format(e))
            return JsonResponse({'success': False, 'dni': str(e)})
        
class FaceTrainingView(View):
    
    def get(self, request):
        from facialRecognition.components.training import training
        result, msg = training()
        
        return JsonResponse({
            'sucess' : result,
            'message' : msg
        })