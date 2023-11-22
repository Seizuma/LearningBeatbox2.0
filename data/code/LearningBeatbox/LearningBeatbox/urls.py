"""
URL configuration for LearningBeatbox project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# In urls.py of your Django app

from django.urls import path
from webapp.views import receive_data
from webapp.views import display_sounds
from webapp.views import home

urlpatterns = [
    # Other URL patterns...
    path('', home, name='home'),
    path('receive_data', receive_data, name='receive_data'),
    path('sounds/', display_sounds, name='display_sounds')
]
