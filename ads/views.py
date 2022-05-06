import json

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Category, Ad


def index(request):
    return HttpResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(DetailView):
    def get(self, request):
        categories = Category.objects.all()
        response = []

        for cat in categories:
            print(cat)
            response.append({
                "id": cat.id,
                "name": cat.name,
            })

        return JsonResponse(response, safe=False)

    def get_by_id(request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return JsonResponse({
                "error": "not found",
            }, status=404)

        return JsonResponse({
                "id": category.id,
                "name": category.name
            }, safe=False, json_dumps_params={"ensure_ascii": False})
    #
    def post(self, request):
        cat_data = json.loads(request.body)
        cat = Category.objects.create(**cat_data)

        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdView(DetailView):
    def get(self, request):
        ads = Ad.objects.all()
        response = []

        for ad in ads:
            print(ad)
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
            })

        return JsonResponse(response, safe=False)

    def get_by_id(request, ad_id):
        try:
            ad = Ad.objects.get(pk=ad_id)
        except Ad.DoesNotExist:
            return JsonResponse({
                "error": "not found",
            }, status=404)

        return JsonResponse({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
            }, safe=False, json_dumps_params={"ensure_ascii": False})

    def post(self, request):
        ad_data = json.loads(request.body)
        ad = Ad.objects.create(**ad_data)

        return JsonResponse({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
            }, safe=False, json_dumps_params={"ensure_ascii": False})


# Loading data into DB
def json_to_cat(request):
    file = "datasets\\categories.json"
    with open(file, encoding='utf-8') as f:
        json_data = json.loads(f.read())

        for item in json_data:
            cat = Category.objects.get_or_create(**item)

    file = "datasets\\ads.json"
    with open(file, encoding='utf-8') as f:
        json_data = json.loads(f.read())

        for item in json_data:
            print(item)
            ad = Ad.objects.get_or_create(**item)
            # movie and genres created
    return JsonResponse("OK", safe=False)
# json_to_cat("categories.json")