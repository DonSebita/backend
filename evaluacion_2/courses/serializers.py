from rest_framework import serializers
from .models import Course, Area # Asegúrate de importar Area
from django.contrib.auth import get_user_model

User = get_user_model()

# 1. Asegúrate de que AreaSerializer siga existiendo
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__' # o los campos específicos que tuvieras antes

# 2. Tu nuevo InstructorSerializer
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

# 3. El CourseSerializer modificado
class CourseSerializer(serializers.ModelSerializer):
    instructor_detalle = InstructorSerializer(source='instructor', read_only=True)
    instructor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='INSTRUCTOR'))

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'instructor_detalle', 'enrollment_cost']