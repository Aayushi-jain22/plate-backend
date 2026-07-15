from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from collections import Counter
from .models import Meal
from .serializers import MealSerializer
from rest_framework.pagination import PageNumberPagination
from datetime import timedelta
from django.db.models import Sum, Count
from django.conf import settings

from django.db.models.functions import TruncDate
from django.utils import timezone

@api_view(['GET', 'POST'])
def meals(request):

    # Create Meal
    if request.method == 'POST':

        serializer = MealSerializer(data=request.data)

            
        if serializer.is_valid():

            name = serializer.validated_data["name"]

            eaten_at = serializer.validated_data["eaten_at"]

            normalized_name = " ".join(
                name.lower().split()
            )

            duplicate = Meal.objects.filter(
                eaten_at__range=(
                    eaten_at - timedelta(minutes=30),
                    eaten_at + timedelta(minutes=30)
                )
            )

            for meal in duplicate:
                existing_name = " ".join(
                    meal.name.lower().split()
                )

                if existing_name == normalized_name:
                    return Response(
                        {
                            "error": "Duplicate meal entry"
                        },
                        status=status.HTTP_409_CONFLICT
                    )

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    
    elif request.method == "GET":

        queryset = Meal.objects.all().order_by("-eaten_at")

        date = request.GET.get("date")
        tag = request.GET.get("tag")
        search = request.GET.get("search")

        if date:
            queryset = queryset.filter(
                eaten_at__date=date
            )

        if tag:
            queryset = queryset.filter(
                tags__contains=[tag]
            )

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        paginator = PageNumberPagination()
        paginator.page_size = 10

        paginated_queryset = paginator.paginate_queryset(
            queryset,
            request
        )

        serializer = MealSerializer(
            paginated_queryset,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )



@api_view(["GET"])
def summary(request):

    date = request.GET.get("date")

    if not date:
        return Response(
            {
                "date": ["This field is required."]
            },
            status=400
        )

    queryset = Meal.objects.filter(
        eaten_at__date=date
    )

    aggregate_data = queryset.aggregate(
        total_calories=Sum("calories"),
        protein_g=Sum("protein_g"),
        carbs_g=Sum("carbs_g"),
        fat_g=Sum("fat_g"),
        meal_count=Count("id")
    )


    all_tags = []

    for meal in queryset:
        all_tags.extend(meal.tags)

    top_tags = [
    tag
    for tag, count in Counter(all_tags).most_common(2)
    ]

    total_calories = aggregate_data["total_calories"] or 0

    response_data = {
        "date": date,
        "total_calories": total_calories,
        "goal_kcal": settings.DAILY_GOAL_KCAL,
        "remaining_kcal": settings.DAILY_GOAL_KCAL - total_calories,
        "macros": {
            "protein_g": aggregate_data["protein_g"] or 0,
            "carbs_g": aggregate_data["carbs_g"] or 0,
            "fat_g": aggregate_data["fat_g"] or 0
        },
        "meal_count": aggregate_data["meal_count"] or 0,
        "top_tags": top_tags
    }

    return Response(response_data)


@api_view(['DELETE'])
def delete_meal(request, id):

    try:
        meal = Meal.objects.get(id=id)

    except Meal.DoesNotExist:

        return Response(
            {
                "message": "Meal not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    meal.delete()

    return Response(
        {
            "message": "Meal deleted successfully"
        },
        status=status.HTTP_200_OK
    )


##Trends View
@api_view(["GET"])
def trends(request):

    days = int(request.GET.get("days", 7))

    if days < 1 or days > 30:
        return Response(
            {
                "days": "Must be between 1 and 30"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days - 1)

    # SINGLE AGGREGATION QUERY
    db_data = (
        Meal.objects
        .filter(
            eaten_at__date__range=[start_date, end_date]
        )
        .annotate(
            day=TruncDate("eaten_at")
        )
        .values("day")
        .annotate(
            calories=Sum("calories"),
            meal_count=Count("id")
        )
        .order_by("day")
    )

    data_map = {
        item["day"]: item
        for item in db_data
    }

    series = []

    current_day = start_date

    while current_day <= end_date:

        day_data = data_map.get(current_day)

        if day_data:
            calories = day_data["calories"] or 0
            meal_count = day_data["meal_count"] or 0
        else:
            calories = 0
            meal_count = 0

        series.append(
            {
                "date": current_day.isoformat(),
                "calories": calories,
                "meal_count": meal_count
            }
        )

        current_day += timedelta(days=1)

    avg_daily_kcal = (
        sum(item["calories"] for item in series)
        / days
    )

    best_day = max(
        series,
        key=lambda x: x["calories"]
    )

    goal = settings.DAILY_GOAL_KCAL

    days_over_goal = len(
        [
            item
            for item in series
            if item["calories"] > goal
        ]
    )

    return Response(
        {
            "days": days,
            "series": series,
            "avg_daily_kcal": round(avg_daily_kcal, 2),
            "best_day": {
                "date": best_day["date"],
                "calories": best_day["calories"]
            },
            "days_over_goal": days_over_goal
        }
    )