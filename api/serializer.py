from rest_framework import serializers
from .models import programmer,Libro, Lector, Autor, Editorial, Prestamo

class ProgrammerSerializer(serializers.ModelSerializer):
    class Meta:
        model = programmer
        fields = '__all__'

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

class LectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lector
        fields = '__all__'

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = '__all__'

class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'