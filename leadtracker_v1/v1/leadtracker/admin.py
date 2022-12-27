from django.contrib import admin
from common.admin import BaseAdmin
from v1.leadtracker import models as lead_models

# Register your models here.
"""leadtracker model registerd to admin panel"""


class TagAdmin(BaseAdmin):
    list_display = ("name",)


class StagePresetAdmin(BaseAdmin):
    list_display = ("name",)


class LeadAdmin(BaseAdmin):
    list_display = (
        "name", "pipedrive", "team_size",
        "revenue", "lead_source", "status",
        )
    search_fields = ["name"]


class OrganizationAdmin(BaseAdmin):
    list_display = ("name", "email", "website", "country", )
    search_fields = ["name"]


class StageAdmin(BaseAdmin):
    list_display = ("id", "name", "is_active", "weightage", "credit", )
    search_fields = ["name"]


class QuestionAdmin(BaseAdmin):
    list_display = ("question", "type", "weightage", "credit", )
    search_fields = ["question"]


class OptionAdmin(BaseAdmin):
    list_display = ("id", "question_id", "option", "points", "is_active", )
    search_fields = ["option"]


class ContactAdmin(BaseAdmin):
    list_display = (
        "name", "email", "organization",
        "role", "linkedin",
    )
    search_fields = ["name"]


class LeadTagAdmin(BaseAdmin):
    list_display = ("lead_id" , "tag_id", )
    search_fields = ["lead_id"]


class StageAnswerAdmin(BaseAdmin):
    list_display = (
        "stage_id", "question_id", "option_id",
        "lead_id", "is_active", "score",
        )
    search_fields = ["lead_id"]


class GeneralAnswerAdmin(BaseAdmin):
    list_display = (
        "question_id", "option_id",
        "lead_id", "is_active", "score",
    )
    search_fields = ["lead_id"]


class LeadContactAdmin(BaseAdmin):
    list_display = (
        "contact_id", "lead_id", "stage_id",
        "is_decision_maker", "is_board_member",
    )
    search_fields = ["lead_id"]


admin.site.register(lead_models.Tag, TagAdmin)
admin.site.register(lead_models.StagePreset, StagePresetAdmin)
admin.site.register(lead_models.Lead, LeadAdmin)
admin.site.register(lead_models.Organization, OrganizationAdmin)
admin.site.register(lead_models.Stage, StageAdmin)
admin.site.register(lead_models.Question, QuestionAdmin)
admin.site.register(lead_models.Option, OptionAdmin)
admin.site.register(lead_models.Contact, ContactAdmin)
admin.site.register(lead_models.LeadTag, LeadTagAdmin)
admin.site.register(lead_models.StageAnswer, StageAnswerAdmin)
admin.site.register(lead_models.GeneralAnswer, GeneralAnswerAdmin)
admin.site.register(lead_models.LeadContact, LeadContactAdmin)
