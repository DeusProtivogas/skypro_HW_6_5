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