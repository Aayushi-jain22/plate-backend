from rest_framework import serializers
from .models import Meal
from django.utils import timezone


ALLOWED_TAGS = {
    "vegetarian",
    "non-vegetarian",
    "vegan",
    "high-protein",
    "low-carb",
    "snack"
}


class MealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meal
        fields = "__all__"


    def validate_calories(self, value):

        if value < 1 or value > 5000:
            raise serializers.ValidationError(
                "Calories must be between 1 and 5000"
            )

        return value


    def validate_name(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Name cannot be empty"
            )

        if len(value) > 100:
            raise serializers.ValidationError(
                "Name cannot exceed 100 characters"
            )

        return value


    def validate_tags(self, value):

        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Tags must be a list"
            )

        invalid_tags = set(value) - ALLOWED_TAGS

        if invalid_tags:
            raise serializers.ValidationError(
                f"Invalid tags: {list(invalid_tags)}"
            )

        return value


    def validate_eaten_at(self, value):

        if value > timezone.now():
            raise serializers.ValidationError(
                "eaten_at cannot be in the future"
            )

        return value