import multiprocessing.process
from django.shortcuts import render

import models

import subprocess
import time

def start_stream():
    process = subprocess.run(["systemctl", "--user", "start", "cam.service"])

def stop_stream():
    process = subprocess.run(["systemctl", "--user", "stop", "cam.service"])

def take_pic(image_name):
    process = subprocess.run(["python","/home/pi/rasberry-pi-camera-live/camera/take_pic.py", image_name])

def stream_view(request):
    try:
        if request.method == "POST" and request.POST["PIC"]:
            stop_stream()
            time.sleep(1)
            saved_images = models.saved_images.objects.get(name="defualt")
            saved_images.count += 1
            image_name = f"saved_image_{saved_images.count}"
            saved_images.save()
            image = models.image.objects.create(name=f"{image_name}")
            image.save()
            take_pic(image_name)
            start_stream()
    except KeyError:
        pass
    
    context = {
        
    }
    return render(request, "stream.html", context=context)

def saved_series_view(request):

    saved_images = models.image.objects.all()

    context = {
        "saved_images": saved_images
    }
    return render(request, "saved.html", context=context)