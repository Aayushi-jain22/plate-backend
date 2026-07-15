#!/bin/sh

python manage.py migrate

python manage.py shell -c "
import json
from meals.models import Meal

with open('meals/seed_meals.json') as f:
    meals = json.load(f)

for meal in meals:
    exists = Meal.objects.filter(
        name=meal['name'],
        eaten_at=meal['eaten_at']
    ).exists()

    if not exists:
        Meal.objects.create(**meal)

print('Seed sync completed')
"

gunicorn config.wsgi:application --bind 0.0.0.0:$PORT