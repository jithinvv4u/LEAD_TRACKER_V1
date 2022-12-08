"""URLs of the app tasks."""

from django.urls import path

from .views.notification import NotificationList
from .views.notification import ReadNotification
from .views.notification import NotificationDetails


urlpatterns = [
    # Notification APIS
    path("notifications/", NotificationList.as_view()),
    path("notifications/read/", ReadNotification.as_view()),
    path("notifications/<idencode:pk>/", NotificationDetails.as_view()),
]
