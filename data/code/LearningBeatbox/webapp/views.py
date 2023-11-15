# In views.py of your Django app

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render

# This will store the latest sounds (simple in-memory storage)
latest_sounds = []


def receive_data(request):
    global latest_sounds
    if request.method == 'GET':
        data = request.GET.get('data', '')
        if data:
            latest_sounds.append(data)
            # Keep only the last 10 entries
            latest_sounds = latest_sounds[-10:]
        return JsonResponse({"status": "success", "received_data": data})


def display_sounds(request):
    # Render a template with the latest sounds
    return render(request, "sounds.html", {"sounds": latest_sounds})
