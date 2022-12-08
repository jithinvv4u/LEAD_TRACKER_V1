from django.contrib import admin
from common.library import encode


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("idencode", "created_on", "updated_on", "creator", "updater")

    list_display = ("__str__", "idencode")

    def encoded_id(self, obj):
        return encode(obj.id)
