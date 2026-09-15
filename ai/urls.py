from django.urls import path
from . import views

urlpatterns = [
    path(
        "interview/",
        views.start_interview,
        name="start_interview"
    ),

    path(
        "interview/<int:interview_id>/submit/",
        views.submit_interview,
        name="submit_interview"
    ),

    path(
        "chat/",
        views.chat,
        name="chat"
    ),
]