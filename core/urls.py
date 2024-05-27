from django.contrib import admin
from django.urls import path
from facialRecognition.views import (
    IndexView, FaceRecognitionView, FaceTrainingView)
from plateRecognition.views import PlateRecognition, video_stream
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('face/', FaceRecognitionView.as_view(), name='face'),
    path('plates/', PlateRecognition.as_view(), name='plates'),
    path('stream/', video_stream, name='stream'),
    path('face_training/', FaceTrainingView.as_view(), name='face_training')
]
