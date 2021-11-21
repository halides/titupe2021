from django.urls import path

from .views import homePageView, transferView, messageView

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('message/', messageView, name='message'),
]
