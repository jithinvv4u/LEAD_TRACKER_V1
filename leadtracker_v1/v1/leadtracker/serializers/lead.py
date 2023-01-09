from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

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

    def validate(self, attrs):
        if len(attrs['name']) > 3:
            return attrs
        raise serializers.ValidationError(
            _("Tag Name should be greater than 3"))


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
            "website", "country", )


class LeadSerializer(serializers.ModelSerializer):
    """
    Serializer for Lead, create with organization(
        user can select or create one).
    """

    # organizations = OrganizationSerializer(required=False)
    organization = custom_fields.IdencodeField(
        related_model=lead_models.Organization)
    
    class Meta:
        """Meta Info"""

        model = lead_models.Lead
        fields = (
            "idencode", "name", "pipedrive", "team_size",
            "revenue", "lead_source", "organization"
        )
        
    def validate_name(self, attrs):
        if len(attrs['name']) > 3:
            return attrs
        raise serializers.ValidationError(
            _("Lead Name should be greater than 3"))

    # def to_representation(self, instance):
    #     data = {
    #     'idencode' : instance.idencode,
    #     'name' : instance.name,
    #     'organization' : instance.organization.name,
    #     'updated_on' : instance.updated_on,
    #     'current_stage' : instance.current_stage.name,
    #     'status' : instance.status,
    #     }
    #     return data
    
    def create(self, validated_data):
        organization_data = validated_data["organization"]
        if lead_models.Organization.objects.filter(name=organization_data):
            lead = lead_models.Lead.objects.create(**validated_data)
        lead_models.Organization.objects.create(name=organization_data,)
        return lead
    
    # def create(self, validated_data):
    #     organization_data = validated_data.pop("organization")
    #     lead = lead_models.Lead.objects.create(**validated_data)
    #     for organization in organization_data:
    #         lead_models.Organization.objects.create(lead_id=lead, **organization)
    #     return lead


class OptionSerializer(serializers.ModelSerializer):
    """
    serializer for Answer.
    """

    class Meta:
        """Meta Info"""

        model = lead_models.Option
        fields = ("idencode", "option", "question_id", "points", )

    def create(self, validated_data):
        if lead_models.Option.objects.filter(
            question_id=validated_data['question_id'],
            option=validated_data['option']):
            raise serializers.ValidationError("Already exist.")
        stage_answer = lead_models.Option.objects.create(**validated_data)
        return stage_answer
    
    def to_representation(self, instance):
        data = {
        'id' : instance.idencode,
        'option' : instance.option,
        }
        return data


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for Question.
    Nested representaion of options.
    """

    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        """Meta Info"""

        model = lead_models.Question
        fields = ("idencode", "question", "type", "field_type", "options")


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

    def create(self, validated_data):
        if lead_models.Option.objects.filter(
            question_id__question=validated_data['question_id'],
            option=validated_data['option_id']).exists():
            if lead_models.StageAnswer.objects.filter(
                lead_id=validated_data['lead_id'],
                stage_id=validated_data['stage_id'],
                question_id=validated_data['question_id'],
                option_id=validated_data['option_id']).exists():
                raise serializers.ValidationError("Already selected.")
            stage_answer = lead_models.StageAnswer.objects.create(
                **validated_data)
        else:
            raise serializers.ValidationError(
                'no question with selected option')
        return stage_answer
    
    def update(self, instance, validated_data):
        if lead_models.Option.objects.filter(
            question_id__question=validated_data['question_id'],
            option=validated_data['option_id']).exists():
            return super().update(instance, validated_data)
        raise serializers.ValidationError('no question with selected option')
    
    
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
        
    def create(self, validated_data):
        if lead_models.Option.objects.filter(
            question_id__question=validated_data['question_id'],
            option=validated_data['option_id']).exists():
            if lead_models.GeneralAnswer.objects.filter(
                lead_id=validated_data['lead_id'],
                question_id=validated_data['question_id'],
                option_id=validated_data['option_id']).exists():
                raise serializers.ValidationError("Already selected.")
            general_answer = lead_models.GeneralAnswer.objects.create(
                **validated_data)
        else:
            raise serializers.ValidationError(
                'no question with selected option')
        return general_answer

    def update(self, instance, validated_data):
        if lead_models.Option.objects.filter(
            question_id__question=validated_data['question_id'],
            option=validated_data['option_id']).exists():
            return super().update(instance, validated_data)
        raise serializers.ValidationError('no question with selected option')
    

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
    contact_id = custom_fields.IdencodeField(
        related_model=lead_models.Contact)
    lead_id = custom_fields.IdencodeField(
        related_model=lead_models.Lead)
    stage_id = custom_fields.IdencodeField(
        related_model=lead_models.Stage)
    
    class Meta:
        """Meta Info"""

        model = lead_models.LeadContact
        fields = (
            "idencode", "contact_id", "lead_id", "stage_id",
            "is_decision_maker", "is_board_member", )