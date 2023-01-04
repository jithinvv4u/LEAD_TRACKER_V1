from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from v1.leadtracker import models as lead_model
from v1.accounts import permissions as user_permission
from v1.leadtracker.serializers import lead as lead_serializer
from v1.leadtracker.functions import get_dashboard

from common import library as comm_lib


class IddecodeModelViewSet(viewsets.ModelViewSet):

    def get_object(self):
        print(self.basename)
        return self.basename.objects.get(
            pk=comm_lib.decode(self.kwargs['pk']))


class LeadViewSet(IddecodeModelViewSet):
    """
    ViewSet to perform crud operations on lead.
    *authetication permission required.
    """

    queryset = lead_model.Lead.objects.all()
    serializer_class = lead_serializer.LeadSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []
    

class OrganizationView(IddecodeModelViewSet):
    """
    View to perform operations on Organization.
    """

    queryset = lead_model.Organization.objects.all()
    serializer_class = lead_serializer.OrganizationSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class QuestionView(IddecodeModelViewSet):
    """
    Viewset to list all question with options.
    """

    queryset = lead_model.Question.objects.all()
    serializer_class = lead_serializer.QuestionSerializer
    http_method_names = ['get']
    authentication_classes = []


class StageAnswerView(IddecodeModelViewSet):
    """
    View for create and list Stage Answers.
    """

    queryset = lead_model.StageAnswer.objects.all()
    serializer_class = lead_serializer.StageAnswerSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class GeneralAnswerView(IddecodeModelViewSet):
    """
    View for create and list General Answers.
    """

    queryset = lead_model.GeneralAnswer.objects.all()
    serializer_class = lead_serializer.GeneralAnswerSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class ContactViewSet(IddecodeModelViewSet):
    """
    ViewSet for manage Contact details.
    """

    queryset = lead_model.Contact.objects.all()
    serializer_class = lead_serializer.ContactSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class LeadContactViewSet(IddecodeModelViewSet):
    """
    ViewSet for lead contact details.
    """

    queryset = lead_model.LeadContact.objects.all()
    serializer_class = lead_serializer.LeadContactSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    # http_method_names = ['get','post']
    authentication_classes = []

    
class DashboardView(generics.ListAPIView):
    """
    View to list data in dashboard.
    
    *autheticated user can view.
    """
    permission_classes = (user_permission.IsAuthenticated,)
    
    def list(self, request, format=None,user=None):
        """
        call get_dashboard function to get data.
        """
        return Response(get_dashboard(),status=status.HTTP_200_OK,)
        
        
# class MakeLeadWon(viewsets.ModelViewSet):
#     serializer_class = lead_serializer.LeadSerializer
#     queryset = lead_model.Lead
#     http_method_names = ['patch']
    
#     def partial_update(self, request, *args, **kwargs):
#         kwargs['partial'] = True
#         return super().partial_update(request, *args, **kwargs)