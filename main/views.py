import json

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad


def index(request):
    return HttpResponse({"status TEST": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        # categories = Category.objects.all()

        self.object_list = self.object_list.order_by("name")

        response = []

        for cat in self.object_list:
            response.append({
                "id": cat.id,
                "name": cat.name,
            })

        return JsonResponse(response, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Category.DoesNotExist:
            return JsonResponse({
                "error": "not found",
            }, status=404)

        return JsonResponse({
                "id": category.id,
                "name": category.name
            }, safe=False, json_dumps_params={"ensure_ascii": False})

@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = [ "name" ]

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)
        cat = Category.objects.create(**cat_data)

        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        cat_data = json.loads(request.body)

        self.object.name = cat_data["name"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return HttpResponse({"status": "200"}, status=200)

# @method_decorator(csrf_exempt, name='dispatch')
# class AdListView(ListView):
#     model = Ad
#
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#         # main = Ad.objects.all()
#         response = []
#
#         for ad in self.object_list:
#             response.append({
#                 "id": ad.id,
#                 "name": ad.name,
#                 "author": ad.author,
#                 "price": ad.price,
#                 "description": ad.description,
#                 "address": ad.address,
#                 "is_published": ad.is_published,
#             })
#
#         return JsonResponse(response, safe=False)
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AdDetailView(DetailView):
#     model = Ad
#
#     def get(self, request, *args, **kwargs):
#
#         try:
#             ad = self.get_object()
#         except Ad.DoesNotExist:
#             return JsonResponse({
#                 "error": "not found",
#             }, status=404)
#
#         return JsonResponse({
#                 "id": ad.id,
#                 "name": ad.name,
#                 "author": ad.author,
#                 "price": ad.price,
#                 "description": ad.description,
#                 "address": ad.address,
#                 "is_published": ad.is_published,
#             }, safe=False, json_dumps_params={"ensure_ascii": False})
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AdCreateView(CreateView):
#     model = Ad
#     fields = [ "name", "author", "price", "description", "address", "is_published" ]
#
#     def post(self, request, *args, **kwargs):
#         ad_data = json.loads(request.body)
#         ad = Ad.objects.create(**ad_data)
#
#         return JsonResponse({
#                 "id": ad.id,
#                 "name": ad.name,
#                 "author": ad.author,
#                 "price": ad.price,
#                 "description": ad.description,
#                 "address": ad.address,
#                 "is_published": ad.is_published,
#             }, safe=False, json_dumps_params={"ensure_ascii": False})
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AdUpdateView(UpdateView):
#     model = Ad
#     fields = [ "name", "author", "price", "description", "address", "is_published" ]
#
#     def post(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#
#         ad_data = json.loads(request.body)
#         # ad = Ad.objects.create(**ad_data)
#
#         self.object.name = ad_data["name"]
#         self.object.author = ad_data["author"]
#         self.object.price = ad_data["price"]
#         self.object.description = ad_data["description"]
#         self.object.address = ad_data["address"]
#         self.object.is_published = ad_data["is_published"]
#
#         self.object.save()
#
#         return JsonResponse({
#                 "id": self.object.id,
#                 "name": self.object.name,
#                 "author": self.object.author,
#                 "price": self.object.price,
#                 "description": self.object.description,
#                 "address": self.object.address,
#                 "is_published": self.object.is_published,
#             }, safe=False, json_dumps_params={"ensure_ascii": False})
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AdDeleteView(DeleteView):
#     model = Ad
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({"status": "200"}, status=200)

# Loading data into DB
def json_to_cat(request):
    file = "datasets\\categories.json"
    with open(file, encoding='utf-8') as f:
        json_data = json.loads(f.read())

        for item in json_data:
            cat = Category.objects.get_or_create(**item)

    file = "datasets\\main.json"
    with open(file, encoding='utf-8') as f:
        json_data = json.loads(f.read())

        for item in json_data:
            print(item)
            ad = Ad.objects.get_or_create(**item)
    return JsonResponse("OK", safe=False)