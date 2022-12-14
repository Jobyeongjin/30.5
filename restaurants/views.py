from django.shortcuts import render, redirect
from .models import Restaurant, Tag
from reviews.models import Review
from stories.models import Story
from .forms import RestaurantsForm
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.http import JsonResponse
from django.db.models import Q


def top_lists(request):
    korea_restaurants = Restaurant.objects.filter(
            Q(tags__name="한식") |
            Q(name__icontains="한식") |
            Q(subtext__icontains="한식")
            )
    korea_restaurants = sorted(korea_restaurants, key=lambda a: -a.grade)[:5]
    china_restaurants = Restaurant.objects.filter(
            Q(tags__name="중식") |
            Q(name__icontains="중식") |
            Q(subtext__icontains="중식")
            )
    china_restaurants = sorted(china_restaurants, key=lambda a: -a.grade)[:5]
    japan_restaurants = Restaurant.objects.filter(
            Q(tags__name="일식") |
            Q(name__icontains="일식") |
            Q(subtext__icontains="일식")
            )
    japan_restaurants = sorted(japan_restaurants, key=lambda a: -a.grade)[:5]
    western_restaurants = Restaurant.objects.filter(
            Q(tags__name="양식") |
            Q(name__icontains="양식") |
            Q(subtext__icontains="양식")
            )
    western_restaurants = sorted(western_restaurants, key=lambda a: -a.grade)[:5]
    school_restaurants = Restaurant.objects.filter(
            Q(tags__name="분식") |
            Q(name__icontains="분식") |
            Q(subtext__icontains="분식")
            )
    school_restaurants = sorted(school_restaurants, key=lambda a: -a.grade)[:5]
    return render(
        request,
        "restaurants/top_lists.html",
        {
            "korea_restaurants": len(korea_restaurants),
            "china_restaurants": len(china_restaurants),
            "japan_restaurants": len(japan_restaurants),
            "western_restaurants": len(western_restaurants),
            "school_restaurants": len(school_restaurants),
        },
    )


def list(request):
    tags = request.POST.get("tag").replace(" ", "").split(",")

    if len(tags) == 1:
        restaurants = Restaurant.objects.filter(
            Q(tags__name=tags[0]) |
            Q(name__icontains=tags[0]) |
            Q(subtext__icontains=tags[0])
            )
        restaurants = sorted(restaurants, key=lambda a: -a.grade)[:5]  # 임의로 5개씩 보여줌.
        tags = tags[0]
    elif len(tags) == 2:
        restaurants = Restaurant.objects.filter(
            Q(tags__name=tags[0]) |
            Q(name__icontains=tags[0]) |
            Q(subtext__icontains=tags[0])
            ).filter(
            Q(tags__name=tags[1]) |
            Q(name__icontains=tags[1]) |
            Q(subtext__icontains=tags[1])
        )
        restaurants = sorted(restaurants, key=lambda a: -a.grade)[:5]  # 임의로 5개까지 보여줌.
        tags = f"{tags[0]} {tags[1]}"
    total_hits = 0
    for restaurant in restaurants:
        total_hits += restaurant.hits

    context = {
        "restaurants": restaurants,
        "restaurants_count": len(restaurants),
        "tags": tags,
        "total_hits": total_hits,
    }
    return render(request, "restaurants/list.html", context)


def korea(request):
    korea_restaurants = Restaurant.objects.filter(
            Q(tags__name="한식") |
            Q(name__icontains="한식") |
            Q(subtext__icontains="한식")
            )
    korea_restaurants = sorted(korea_restaurants, key=lambda a: -a.grade)[:5]
    restaurants = Restaurant.objects.order_by("-pk")
    context = {
        "restaurants": restaurants,
        "korea_restaurants": korea_restaurants.count(),
    }
    return render(request, "restaurants/korea.html", context)


def china(request):
    china_restaurants = Restaurant.objects.filter(
            Q(tags__name="중식") |
            Q(name__icontains="중식") |
            Q(subtext__icontains="중식")
            )
    china_restaurants = sorted(china_restaurants, key=lambda a: -a.grade)[:5]
    restaurants = Restaurant.objects.order_by("-pk")
    context = {
        "restaurants": restaurants,
        "china_restaurants": china_restaurants.count(),
    }
    return render(request, "restaurants/china.html", context)


def japan(request):
    japan_restaurants = Restaurant.objects.filter(
            Q(tags__name="일식") |
            Q(name__icontains="일식") |
            Q(subtext__icontains="일식")
            )
    japan_restaurants = sorted(japan_restaurants, key=lambda a: -a.grade)[:5]
    restaurants = Restaurant.objects.order_by("-pk")
    context = {
        "restaurants": restaurants,
        "japan_restaurants": japan_restaurants.count(),
    }
    return render(request, "restaurants/japan.html", context)


def western(request):
    western_restaurants = Restaurant.objects.filter(
            Q(tags__name="양식") |
            Q(name__icontains="양식") |
            Q(subtext__icontains="양식")
            )
    western_restaurants = sorted(western_restaurants, key=lambda a: -a.grade)[:5]
    restaurants = Restaurant.objects.order_by("-pk")
    context = {
        "restaurants": restaurants,
        "western_restaurants": western_restaurants.count(),
    }
    return render(request, "restaurants/western.html", context)


def school(request):
    school_restaurants = Restaurant.objects.filter(
            Q(tags__name="분식") |
            Q(name__icontains="분식") |
            Q(subtext__icontains="분식")
            )
    school_restaurants = sorted(school_restaurants, key=lambda a: -a.grade)[:5]
    restaurants = Restaurant.objects.order_by("-pk")
    context = {
        "restaurants": restaurants,
        "school_restaurants": school_restaurants.count(),
    }
    return render(request, "restaurants/school.html", context)


def create(request):
    if request.method == "POST":
        restaurants_form = RestaurantsForm(request.POST, request.FILES)
        if restaurants_form.is_valid():
            new_restaurant = Restaurant(
                name=restaurants_form.cleaned_data["name"],
                address=restaurants_form.cleaned_data["address"],
                shop_number=restaurants_form.cleaned_data["shop_number"],
                between_pay=restaurants_form.cleaned_data["between_pay"],
                opening_time=restaurants_form.cleaned_data["opening_time"],
                break_day=restaurants_form.cleaned_data["break_day"],
            )
            new_restaurant.save()
            tags = restaurants_form.cleaned_data["tags"].split(",")
            for tag in tags:
                if not tag:
                    continue
                else:
                    tag = tag.strip()
                    _tag, _ = Tag.objects.get_or_create(name=tag)
                    new_restaurant.tags.add(_tag)
            return redirect("main:index")
    else:
        restaurants_form = RestaurantsForm()
    context = {
        "restaurants_form": restaurants_form,
    }
    return render(request, "restaurants/create.html", context=context)


def detail(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    reviews = restaurant.reviews.all()
    reviews_count = len(reviews)
    likes = restaurant.like_users.all()

    ratings = []
    for review in reviews:
        ratings.append(review.rating)

    upper, middle, lower = 0, 0, 0
    for rating in ratings:
        if int(rating) > 3:
            upper += 1
        elif int(rating) == 3:
            middle += 1
        else:
            lower += 1

    context = {
        "restaurant": restaurant,
        "reviews": reviews[::-1],
        "upper": upper,
        "middle": middle,
        "lower": lower,
        "reviews_count": reviews_count,
        "likes": len(likes),
    }

    response = render(request, "restaurants/detail.html", context)

    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get("hitboard", "_")

    if f"_{pk}_" not in cookie_value:
        cookie_value += f"_{pk}_"
        response.set_cookie(
            "hitboard", value=cookie_value, max_age=max_age, httponly=True
        )
        restaurant.hits += 1
        restaurant.save()

    return response


def update(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    if request.method == "POST":
        restaurants_form = RestaurantsForm(
            request.POST, request.FILES, instance=restaurant
        )
        if restaurants_form.is_valid():
            restaurant.tags.all().delete()
            tags = restaurants_form.cleaned_data["tags"].split(",")
            for tag in tags:
                if not tag:
                    continue
                else:
                    tag = tag.strip()
                    _tag, _ = Tag.objects.get_or_create(name=tag)
                    restaurant.tags.add(_tag)
            restaurants = restaurants_form.save(commit=False)
            restaurants.save()
            return redirect("restaurants:detail", pk)
    else:
        restaurants_form = RestaurantsForm(instance=restaurant)

    context = {
        "restaurants_form": restaurants_form,
    }
    return render(request, "restaurants/update.html", context=context)


def delete(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    restaurant.delete()
    return redirect("main:index")


@login_required
def like(request, pk):
    print(request.POST)
    if request.user.is_authenticated:
        restaurant = Restaurant.objects.get(pk=pk)
        if restaurant.like_users.filter(pk=request.user.pk).exists():
            restaurant.like_users.remove(request.user)
            is_liked = False
        else:
            restaurant.like_users.add(request.user)
            is_liked = True
    else:
        return redirect("restaurants:detail", pk)
    return JsonResponse(
        {
            "is_liked": is_liked,
            "like_count": restaurant.like_users.count(),
        }
    )
