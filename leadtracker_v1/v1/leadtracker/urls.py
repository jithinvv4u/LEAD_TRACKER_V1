"""URLs of the app leadtracker."""

from django.urls import path, include
from rest_framework import routers
from v1.leadtracker.views import lead as lead_view
from v1.leadtracker import models as lead_model

router = routers.DefaultRouter()

router.register("lead", lead_view.LeadViewSet, basename=lead_model.Lead)
router.register("organization", lead_view.OrganizationView,
                basename=lead_model.Organization)

router.register("contact", lead_view.ContactViewSet,
                basename=lead_model.Contact)
router.register("leadcontact", lead_view.LeadContactViewSet,
                basename=lead_model.LeadContact)
router.register("question", lead_view.QuestionView,
                basename=lead_model.Question)
router.register("stageanswer", lead_view.StageAnswerView,
                basename=lead_model.StageAnswer)
router.register("generalanswer", lead_view.GeneralAnswerView,
                basename=lead_model.GeneralAnswer)


urlpatterns = [
    path("", include(router.urls)),
    
    path("dashboard/", lead_view.DashboardView.as_view()),
    
    # path("makewon/", lead_view.MakeLeadWon.as_view()),

]
