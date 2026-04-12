from django.contrib import admin

from .models import FruitGallery, FruitGalleryImage


RESTRICTED_ADMIN_USERNAME = "Ganesan"


def _is_restricted_admin_user(user):
    return user.is_authenticated and user.username.lower() == RESTRICTED_ADMIN_USERNAME.lower()


def _restrict_non_fruit_admin_modules():
    for model, model_admin in admin.site._registry.items():
        if model._meta.app_label == "fruits":
            continue

        original_has_module_permission = model_admin.has_module_permission
        original_has_view_permission = model_admin.has_view_permission
        original_has_add_permission = model_admin.has_add_permission
        original_has_change_permission = model_admin.has_change_permission
        original_has_delete_permission = model_admin.has_delete_permission

        def has_module_permission(request, _original=original_has_module_permission):
            if _is_restricted_admin_user(request.user):
                return False
            return _original(request)

        def has_view_permission(request, obj=None, _original=original_has_view_permission):
            if _is_restricted_admin_user(request.user):
                return False
            return _original(request, obj)

        def has_add_permission(request, _original=original_has_add_permission):
            if _is_restricted_admin_user(request.user):
                return False
            return _original(request)

        def has_change_permission(request, obj=None, _original=original_has_change_permission):
            if _is_restricted_admin_user(request.user):
                return False
            return _original(request, obj)

        def has_delete_permission(request, obj=None, _original=original_has_delete_permission):
            if _is_restricted_admin_user(request.user):
                return False
            return _original(request, obj)

        model_admin.has_module_permission = has_module_permission
        model_admin.has_view_permission = has_view_permission
        model_admin.has_add_permission = has_add_permission
        model_admin.has_change_permission = has_change_permission
        model_admin.has_delete_permission = has_delete_permission


class FruitGalleryImageInline(admin.TabularInline):
    model = FruitGalleryImage
    extra = 1


@admin.register(FruitGallery)
class FruitGalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "discount_percentage")
    search_fields = ("name",)
    inlines = [FruitGalleryImageInline]


_restrict_non_fruit_admin_modules()
