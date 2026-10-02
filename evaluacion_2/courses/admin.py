from django.contrib import admin
from .models import Area, Course

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'area', 'enrollment_cost', 'available_capacity', 'max_capacity')
    list_filter = ('area',)
