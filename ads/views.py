import json

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView

from rest_framework.permissions import IsAuthenticated

from ads.models import Ad

from main import settings

from ads.models import Selection
from ads.serializers import SelectionDetailSerializer, SelectionListSerializer, SelectionSerializer

from ads.permissions import SelectionUpdatePermission

from ads.serializers import AdDetailSerializer

from user.models import User

from ads.models import Category


def root(request):
    return JsonResponse({
        "status": "ok"
    })


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionRetrieveView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]




@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.all()


    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        categories = request.GET.getlist("cat", [])
        if categories:
            self.object_list = self.object_list.filter(category_id__in=categories)

        if request.GET.get("text", None):
            text_rmv = request.GET.get('text', None).replace('\"', '')
            self.object_list = self.object_list.filter(name__icontains=text_rmv)

        if request.GET.get("location", None):
            self.object_list = self.object_list.filter(author__locations__name__icontains=request.GET.get("location"))

        if request.GET.get("price_from", None):
            self.object_list = self.object_list.filter(price__gte=request.GET.get("price_from"))

        if request.GET.get("price_to", None):
            self.object_list = self.object_list.filter(price__lte=request.GET.get("price_to"))


        self.object_list = self.object_list.order_by("-price")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        all_ads = []

        for ad in page_obj:
            all_ads.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "author": ad.author.first_name,
                "price": ad.price,
                "description": ad.description,
                # "address": ad.address,
                "is_published": ad.is_published,
                "category_id": ad.category_id,
                "image": ad.image.url if ad.image else None,
            })

        response = {
            "items": all_ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }

        return JsonResponse(response, safe=False)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]

@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = [ "name", "author", "price", "description", "address", "is_published" ]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        print(ad_data)
        ad_data["author"] = User.objects.get(id=int(ad_data["author"]))
        ad_data["category"] = Category.objects.get(id=int(ad_data["category"]))

        ad = Ad.objects.create(**ad_data)

        return JsonResponse({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.id,
                "price": ad.price,
                "description": ad.description,
                # "address": ad.address,
                "is_published": ad.is_published,
                "category": ad.category.id,
                "image": None,
            }, safe=False, json_dumps_params={"ensure_ascii": False}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = [ "name", "author", "price", "description", "address", "is_published" ]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

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
