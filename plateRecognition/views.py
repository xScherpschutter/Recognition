# from channels.generic.websocket import WebsocketConsumer
from django.http import StreamingHttpResponse
from django.views.generic import View
# from . import plateR
from . import detection
import numpy as np
import cv2
import json
from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import gzip
# import json


class PlateRecognition(View):
    template_name = 'PlateRecognition.html'

    def get(self, request):
        return render(request, self.template_name, context={})


@gzip.gzip_page
def video_stream(request):
    print(request)

    def stream_gen():
        while True:
            video = request.GET.get('video')
            if video:
                video_data = np.frombuffer(video, np.uint8)
                frame = cv2.imdecode(video_data, cv2.IMREAD_COLOR)
                plates = detection.detect_plates(frame)
                yield json.dumps({'plates': plates})+'\n'
    return StreamingHttpResponse(
        stream_gen(), content_type="application/json")
    # return StreamingHttpResponse(
    #     plateR.PlateDetection(request.GET.get('video')),
    #     content_type="multipart/x-mixed-replace;boundary=frame")
