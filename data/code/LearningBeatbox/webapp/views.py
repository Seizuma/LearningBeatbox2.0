# In views.py of your Django app

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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

            # Trigger the group send
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "sounds",  # The group name where all consumers are listening
                {
                    "type": "sound_message",  # Custom method in the consumer
                    "message": data,
                }
            )

        return JsonResponse({"status": "success", "received_data": data})


def display_sounds(request):
    # Render a template with the latest sounds
    return render(request, "sounds.html", {"sounds": latest_sounds})
