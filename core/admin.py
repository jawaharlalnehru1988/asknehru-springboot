from django.contrib import admin

from conversations.models import Conversation
from medicines.models import Medicine
from planning.models import Epic, EpicAccess, Task
from roadmaps.models import Roadmap
from yoga.models import YogaPose


class EpicAccessInline(admin.TabularInline):
    model = EpicAccess
    extra = 1
    fields = ("user", "role", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Epic)
class EpicAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "client_name", "created_at", "updated_at")
    search_fields = ("title", "client_name")
    list_filter = ("client_name",)
    inlines = [EpicAccessInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "priority", "epic", "assigned_to", "due_date", "updated_at")
    list_filter = ("status", "priority", "epic")
    search_fields = ("title", "description")
    autocomplete_fields = ("epic",)
    date_hierarchy = "due_date"

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "main_topic", "sub_topic", "created_at")
    list_filter = ("main_topic",)
    search_fields = ("sub_topic", "article")


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "category", "quantity", "unit", "expiry_date")
    list_filter = ("category",)
    search_fields = ("name", "brand")
    date_hierarchy = "expiry_date"


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ("id", "main_topic", "intro", "created_at")
    search_fields = ("main_topic", "intro")


@admin.register(YogaPose)
class YogaPoseAdmin(admin.ModelAdmin):
    list_display = ("id", "yoga_name", "category")
    list_filter = ("category",)
    search_fields = ("yoga_name",)


@admin.register(EpicAccess)
class EpicAccessAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "epic", "role", "created_at")
    list_filter = ("role", "epic")
    search_fields = ("user__username", "epic__title")
    readonly_fields = ("created_at",)
