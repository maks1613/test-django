from django.contrib import admin
from .models import Owner, Product, User, ProductAccess, Lesson, ProductLessons, LessonViews


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner_id']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']


@admin.register(ProductAccess)
class ProductAccessAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'user_id']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'video_link', 'vidio_duration']


@admin.register(ProductLessons)
class ProductLessonsAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(LessonViews)
class LessonViewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'time_watched', 'status', 'viewing_time']
