import json

from django.core.management.base import BaseCommand
from django.conf import settings

from meals.models import Meal


class Command(BaseCommand):

    help = "Load seed meals"


    def handle(self, *args, **kwargs):

        with open(
            "meals/seed_meals.json",
            "r"
        ) as file:

            data = json.load(file)


        for meal in data:

            Meal.objects.get_or_create(
                name=meal["name"],
                eaten_at=meal["eaten_at"],
                defaults={
                    "calories": meal["calories"],
                    "protein_g": meal["protein_g"],
                    "carbs_g": meal["carbs_g"],
                    "fat_g": meal["fat_g"],
                    "tags": meal["tags"]
                }
            )


        self.stdout.write(
            self.style.SUCCESS(
                "Seed meals loaded successfully"
            )
        )