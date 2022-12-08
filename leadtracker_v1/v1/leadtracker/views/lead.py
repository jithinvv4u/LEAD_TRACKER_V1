from rest_framework import viewsets
from rest_framework import generics

from rest_framework.response import Response

from v1.leadtracker import models as lead_model
from v1.accounts import permissions as user_permission

from v1.leadtracker.serializers import lead as lead_serializer
from django.shortcuts import get_object_or_404


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet to perform crud operations on lead.
    """

    queryset = lead_model.Lead.objects.all()
    serializer_class = lead_serializer.LeadSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []

    def retrieve(self, request, pk=None):
        """retrieve lead using lead_id"""
        queryset = lead_model.Lead.objects.all()
        lead = get_object_or_404(queryset, pk=pk)
        serializer = lead_serializer.LeadListSerializer(lead)
        return Response(serializer.data)


class OrganizationView(viewsets.ModelViewSet):
    """
    View for listing questions and answers.
    """
    queryset = lead_model.Organization.objects.all()
    serializer_class = lead_serializer.OrganizationSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []
    
    def retrieve(self, request, pk=None):
        """retrieve lead using lead_id"""
        queryset = lead_model.Organization.objects.all()
        organization = get_object_or_404(queryset, pk=pk)
        serializer = lead_serializer.OrganizationSerializer(organization)
        return Response(serializer.data)
    
    
class StageAnswerView(generics.ListCreateAPIView):
    """
    View for listing questions and answers.
    """
    queryset = lead_model.StageAnswer.objects.all()
    serializer_class = lead_serializer.StageAnswerSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []
    
    
class QuestionView(generics.ListAPIView):
    """
    View for listing questions and answers.
    """
    queryset = lead_model.Question.objects.all()
    serializer_class = lead_serializer.QuestionSerializer
    authentication_classes = []
    
    
class GeneralAnswerView(generics.ListCreateAPIView):
    """
    View for listing questions and answers.
    """
    queryset = lead_model.GeneralAnswer.objects.all()
    serializer_class = lead_serializer.GeneralAnswerSerializer
    # permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []
    
        
class LeadListView(generics.ListCreateAPIView):
    """
    ViewSet to get list of leads data.
    """
    queryset = lead_model.Lead.objects.all()
    serializer_class = lead_serializer.LeadListSerializer
    # permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []
    
    
# class OrganizationRetrieveView(generics.RetrieveAPIView):
#     """
#     View for listing questions and answers.
#     """
#     queryset = lead_model.Organization.objects.all()
#     serializer_class = lead_serializer.OrganizationSerializer
#     permission_classes = []
#     authentication_classes = []

    
# class AnswerListView(generics.ListAPIView):
#     """
#     View for listing questions and answers.
#     """
#     queryset = lead_model.Answer.objects.all()
#     serializer_class = lead_serializer.AnswerSerializer
#     permission_classes = []
#     authentication_classes = []
    

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = lead_serializer.QuestionSerializer(queryset, many=True)
    #     return Response(serializer.data)


# class OrganizationViewSet(viewsets.ModelViewSet):
#     queryset = lead_model.Organization.objects.all()
#     serializer_class = serializer.OrganizationSerializer
#     http_method_names = ['post', 'get']


# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = lead_model.Question.objects.all()
#     serializer_class = serializer.QuestionSerializer
#     http_method_names = ['post', 'get']


# class AnswerViewSet(viewsets.ModelViewSet):
#     queryset = lead_model.Answer.objects.all()
#     serializer_class = serializer.AnswerSerializer
#     http_method_names = ['post']


# class StageViewSet(viewsets.ModelViewSet):
#     queryset = lead_model.Stage.objects.all()
#     serializer_class = serializer.StageSerializer
#     http_method_names = ['post']


# class ContactViewSet(viewsets.ModelViewSet):
#     queryset = lead_model.Contact.objects.all()
#     serializer_class = serializer.ContactSerializer
#     http_method_names = ['post']


# class AnswerView(generics.ListAPIView):
#     queryset = lead_model.Answer.objects.all()
#     serializer_class = lead_serializer.AnswerSerializer
#     permission_classes = []
#     authentication_classes = []

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = lead_serializer.AnswerSerializer(queryset, many=True)
#         return Response(serializer.data)
