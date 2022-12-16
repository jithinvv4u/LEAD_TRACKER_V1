from rest_framework import serializers

from v1.leadtracker import models as lead_models

from common.drf_custom import fields as custom_fields


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag.
    """

    class Meta:
        """Meta Info."""

        model = lead_models.Tag
        fields = ("idencode", "name", )


class StagePresetSerializer(serializers.ModelSerializer):
    """
    Serializer for Stage Preset.
    """

    class Meta:
        """Meta Info."""

        model = lead_models.StagePreset
        fields = ("idencode", "name", )


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for Organization.
    """

    class Meta:
        """Meta Info"""

        model = lead_models.Organization
        fields = (
            "idencode", "name", "email",
            "website", "country",
        )


class LeadSerializer(serializers.ModelSerializer):
    """
    Serializer for Lead, create with organization(
        user can select or create one).
    """

    # organizations = OrganizationSerializer(many=True)
    organization = custom_fields.IdencodeField(
        related_model=lead_models.Organization)
    
    class Meta:
        """Meta Info"""

        model = lead_models.Lead
        fields = (
            "idencode", "name", "pipedrive", "team_size",
            "revenue", "lead_source", "organization"
        )

    # def create(self, validated_data):
    #     organization_data = validated_data.pop("organization")
    #     lead = lead_models.Lead.objects.create(**validated_data)
    #     for organization in organization_data:
    #         lead_models.Organization.objects.create(lead_id=lead, **organization)
    #     return lead


class LeadListSerializer(serializers.ModelSerializer):
    """
    Serializer for Lead, create with organization(
        user can select or create one).
    """

    class Meta:
        """Meta Info"""

        model = lead_models.Lead
        fields = (
            "idencode", "name", "organizations",
            "updated_on", "current_stage",
        )

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     return data


class OptionSerializer(serializers.ModelSerializer):
    """
    serializer for Answer.
    """

    class Meta:
        """Meta Info"""

        model = lead_models.Option
        fields = ("idencode", "option",
            # "question_id",
            # "points",
        )


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for Question.
    """

    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        """Meta Info"""

        model = lead_models.Question
        fields = ("idencode", "question", "options")


class StageAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for Question.
    """
    stage_id = custom_fields.IdencodeField(
        related_model=lead_models.Stage)
    lead_id = custom_fields.IdencodeField(
        related_model=lead_models.Lead)
    question_id = custom_fields.IdencodeField(
        related_model=lead_models.Question)
    option_id = custom_fields.IdencodeField(
        related_model=lead_models.Option)    

    class Meta:
        """Meta Info"""

        model = lead_models.StageAnswer
        fields = (
            "idencode", "stage_id", "lead_id",
            "question_id", "option_id", "score",
        )


class GeneralAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for Question.
    """
    lead_id = custom_fields.IdencodeField(
        related_model=lead_models.Lead)
    question_id = custom_fields.IdencodeField(
        related_model=lead_models.Question)
    option_id = custom_fields.IdencodeField(
        related_model=lead_models.Option)    

    class Meta:
        """Meta Info"""

        model = lead_models.GeneralAnswer
        fields = (
            "idencode", "lead_id", "question_id", "option_id", "score", )


class StageSerializer(serializers.ModelSerializer):
    """
    Serializer for Stages.
    """

    class Meta:
        """Meta Info"""

        model = lead_models.Stage
        fields = ( "idencode", "name", "weightage", "credit", )


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Contact.
    """
    organization = custom_fields.IdencodeField(
        related_model=lead_models.Organization
    )
    
    class Meta:
        """Meta Info"""

        model = lead_models.Contact
        fields = ("idencode", "name", "email", 
                  "organization", "role", "linkedin" )


class LeadContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Lead Contact.
    """

    class Meta:
        """Meta Info"""

        model = lead_models.LeadContact
        fields = (
            "idencode", "contact_id", "lead_id", "stage_id",
            "is_decision_maker", "is_board_member", )
