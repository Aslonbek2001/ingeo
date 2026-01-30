from rest_framework import serializers
from menus.models import Employee, Page

class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
                    "id", 
                    "full_name_uz", "full_name_ru", "full_name_en",
                    "position_uz", "position_ru", "position_en",
                    "order", "pages",
                    "phone", "email", "image"
                ]



class EmployeeDetailSerializer(serializers.ModelSerializer):
    pages = serializers.PrimaryKeyRelatedField(
        queryset=Page.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Employee
        fields = [
                    "id", 
                    "full_name_uz", "full_name_ru", "full_name_en",
                    "position_uz", "position_ru", "position_en",
                    "description_uz", "description_ru", "description_en",
                    "order", "pages",
                    "phone", "email", "image"
                ]

    def create(self, validated_data):
        pages = validated_data.pop("pages", [])
        employee = Employee.objects.create(**validated_data)
        if pages:
            employee.pages.set(pages)
        return employee
    
    def update(self, instance, validated_data):
        pages = validated_data.pop("pages", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if pages is not None:
            instance.pages.set(pages)
        return instance
        
