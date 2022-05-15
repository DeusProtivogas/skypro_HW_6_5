import json

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView

from ads.models import Ad

from main import settings


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        # main = Ad.objects.all()

        self.object_list = self.object_list.order_by("-price")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        all_ads = []

        for ad in page_obj:
            all_ads.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.username,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
                "category": ad.category.name,
            })

        response = {
            "items": all_ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):

        try:
            ad = self.get_object()
        except Ad.DoesNotExist:
            return JsonResponse({
                "error": "not found",
            }, status=404)

        return JsonResponse({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.username,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
                "category": ad.category.name,
            }, safe=False, json_dumps_params={"ensure_ascii": False})

@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = [ "name", "author", "price", "description", "address", "is_published" ]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        ad = Ad.objects.create(**ad_data)

        return JsonResponse({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.username,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
                "category": ad.category.name,
            }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = [ "name", "author", "price", "description", "address", "is_published" ]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        # ad = Ad.objects.create(**ad_data)

        self.object.name = ad_data["name"]
        self.object.author = ad_data["author"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.address = ad_data["address"]
        self.object.is_published = ad_data["is_published"]

        self.object.save()

        return JsonResponse({
                "id": self.object.id,
                "name": self.object.name,
                "author": self.object.author.username,
                "price": self.object.price,
                "description": self.object.description,
                "address": self.object.address,
                "is_published": self.object.is_published,
                "category": self.object.category.name,
            }, safe=False, json_dumps_params={"ensure_ascii": False})



@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = [ "name", "author", "price", "description", "address", "is_published", "image" ]

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()

        self.object.image = request.FILES["image"]

        super().post(request, *args, **kwargs)

        self.object.save()

        return JsonResponse({
                "id": self.object.id,
                "name": self.object.name,
                "author": self.object.author.username,
                "price": self.object.price,
                "description": self.object.description,
                "address": self.object.address,
                "is_published": self.object.is_published,
                "image": self.object.image.url if self.object.image else None,
            }, safe=False, json_dumps_params={"ensure_ascii": False})

@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return HttpResponse({"status": "200"}, status=200)
