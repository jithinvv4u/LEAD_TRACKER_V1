from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from v1.leadtracker import models as lead_model
from v1.leadtracker.serializers import lead as lead_serializer
from v1.accounts import permissions as user_permission

from django.db.models import Count, F, Sum

from common import library as comm_lib


class IddecodeModelViewSet(viewsets.ModelViewSet):

    def get_object(self):
        return self.basename.objects.get(
            pk=comm_lib._decode(self.kwargs['pk']))


class LeadViewSet(IddecodeModelViewSet):
    """
    ViewSet to perform crud operations on lead.
    *authetication permission required.
    """

    queryset = lead_model.Lead.objects.all()
    serializer_class = lead_serializer.LeadSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class OrganizationView(viewsets.ModelViewSet):
    """
    View to perform operations on Organization.
    """

    queryset = lead_model.Organization.objects.all()
    serializer_class = lead_serializer.OrganizationSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class QuestionView(viewsets.ModelViewSet):
    """
    Viewset to list all question with options.
    """

    queryset = lead_model.Question.objects.all()
    serializer_class = lead_serializer.QuestionSerializer
    http_method_names = ['get']
    authentication_classes = []


class StageAnswerView(generics.ListCreateAPIView):
    """
    View for create and list Stage Answers.
    """

    queryset = lead_model.StageAnswer.objects.all()
    serializer_class = lead_serializer.StageAnswerSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class GeneralAnswerView(generics.ListCreateAPIView):
    """
    View for create and list General Answers.
    """

    queryset = lead_model.GeneralAnswer.objects.all()
    serializer_class = lead_serializer.GeneralAnswerSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class LeadListView(generics.ListCreateAPIView):
    """
    ViewSet to get list of leads data.
    """

    queryset = lead_model.Lead.objects.all()
    serializer_class = lead_serializer.LeadListSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for manage Contact details.
    """

    queryset = lead_model.Contact.objects.all()
    serializer_class = lead_serializer.ContactSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class LeadContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for lead contact details.
    """

    queryset = lead_model.LeadContact.objects.all()
    serializer_class = lead_serializer.LeadContactSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    http_method_names = ['get','post']
    authentication_classes = []


class DashboardView(generics.ListAPIView):
    """
    View to list data in dashboard.
    
    *autheticated user can view.
    """
    permission_classes = (user_permission.IsAuthenticated,)
    
    def list(self, request, format=None,user=None):
        """
        Return a list of all stages and lead details.
        """
        lead_total = lead_model.Lead.objects.all().count()
        lead_won = lead_model.Lead.objects.filter(status=2).count()
        lead_lost = lead_model.Lead.objects.filter(status=3).count()
        lead_stage = (lead_model.Lead.objects.values(
            stage=F("current_stage__name"))
            .annotate(count=Count("current_stage"))
            .order_by("-count")
        )
        all_stages = (lead_model.Stage.objects.values("name"))
                
        # lead_score = lead_model.StageAnswer.objects.values(
        #     'lead_id__name').annotate(
        #         total_point=Sum('option_id__points'),total_credit=Sum('question_id'),score=Sum(F('total_point') * ('total_credit'))).order_by('lead_id')
        # print(lead_score)
        
        return Response(
            {
                "lead_total": lead_total,
                "lead_won": lead_won,
                "lead_lost": lead_lost,
                "lead_stage": lead_stage,
                "stages": all_stages,
            },
            status=status.HTTP_200_OK,
        )