"""URLs of the app leadtracker."""

from django.urls import path, include
from rest_framework import routers
from v1.leadtracker.views import lead as lead_view

router = routers.DefaultRouter()

router.register("lead", lead_view.LeadViewSet, basename="lead")
router.register("organization", lead_view.OrganizationView,
                basename="organization")

urlpatterns = [
    path("", include(router.urls)),
    
    path("leadlist/", lead_view.LeadListView.as_view()),
    #url to view questions
    path("question/", lead_view.QuestionView.as_view()),
    #url to create and view answers
    path("stageanswer/", lead_view.StageAnswerView.as_view()),
    path("generalanswer/", lead_view.GeneralAnswerView.as_view()),

]
