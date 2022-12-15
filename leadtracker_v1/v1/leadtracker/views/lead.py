from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from v1.leadtracker import models as lead_model
from v1.accounts import permissions as user_permission

from v1.leadtracker.serializers import lead as lead_serializer

from django.shortcuts import get_object_or_404
from django.db.models import Count


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet to perform crud operations on lead.
    """

    queryset = lead_model.Lead.objects.all()
    serializer_class = lead_serializer.LeadSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []

    def retrieve(self, request, pk=None,user=None):
        """retrieve lead using lead_id"""
        queryset = lead_model.Lead.objects.all()
        lead = get_object_or_404(queryset, pk=pk)
        serializer = lead_serializer.LeadListSerializer(lead)
        return Response(serializer.data)

    # @action(detail=False, methods=["get"], url_path="dashboard/lead")
    # def dashboard_lead(self, request, *args, **kwargs):
    #     lead_total = lead_model.Lead.objects.all().count()
    #     lead_won = lead_model.Lead.objects.filter(status=2).count()
    #     lead_lost = lead_model.Lead.objects.filter(status=3).count()
    #     lead_stage = (lead_model.Lead.objects.values("current_stage__name")
    #         .annotate(count=Count("current_stage"))
    #         .order_by("-count")
    #     )
    #     all_stages = (lead_model.Stage.objects.values("name"))
    #     return Response(
    #         {
    #             "lead_total": lead_total,
    #             "lead_won": lead_won,
    #             "lead_lost": lead_lost,
    #             "lead_stage": lead_stage,
    #             "all_stages": all_stages,
    #         },
    #         status=status.HTTP_200_OK,
    #     )


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
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class DashboardView(APIView):
    """
    View to list data in dashboard.
    
    *autheticated user can view.
    """
    permission_classes = (user_permission.IsAuthenticated,)
    
    def get(self, request, format=None,user=None):
        """
        Return a list of all stages and lead details.
        """
        lead_total = lead_model.Lead.objects.all().count()
        lead_won = lead_model.Lead.objects.filter(status=2).count()
        lead_lost = lead_model.Lead.objects.filter(status=3).count()
        lead_stage = (lead_model.Lead.objects.values("current_stage__name")
            .annotate(count=Count("current_stage"))
            .order_by("-count")
        )
        all_stages = (lead_model.Stage.objects.values("name"))
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


class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet to perform crud operations on lead.
    """

    queryset = lead_model.Contact.objects.all()
    serializer_class = lead_serializer.ContactSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    authentication_classes = []


class LeadContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet to perform crud operations on lead.
    """

    queryset = lead_model.LeadContact.objects.all()
    serializer_class = lead_serializer.LeadContactSerializer
    permission_classes = (user_permission.IsAuthenticated,)
    http_method_names = ['get','post']
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
