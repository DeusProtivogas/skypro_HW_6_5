import json

from django.db.models import Count, When, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pycparser.c_ast import Case

from user.models import User

from location.models import Location


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True)))

        # main = Ad.objects.all()

        # paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        # page_number = request.GET.get("page")
        # page_obj = paginator.get_page(page_number)

        self.object_list = self.object_list.order_by("username")

        users = []

        # total_adds =

        for user in self.object_list:
            users.append({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "total ads": user.total_ads,
                "locations": list(map(str, user.locations.all())),
            })

        response = {
            "items": users,
            # "num_pages": paginator.num_pages,
            # "total": paginator.count,
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):

        try:
            user = self.get_object()
        except User.DoesNotExist:
            return JsonResponse({
                "error": "not found",
            }, status=404)

        return JsonResponse({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.locations.all())),
            }, safe=False, json_dumps_params={"ensure_ascii": False})

@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = [ "first_name", "last_name", "username", "password", "role", "age", "locations" ]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        # user = User.objects.create(**ad_data)
        user = User.objects.create(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
            age=user_data["age"],
        )

        for location_name in user_data["locations"]:
            location, _ = Location.objects.get_or_create(name=location_name)
            user.locations.add(location)

        return JsonResponse({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.locations.all())),
            }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = [ "first_name", "last_name", "username", "password", "role", "age", "locations" ]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        # ad = Ad.objects.create(**ad_data)

        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.password = user_data["password"]
        self.object.role = user_data["role"]
        self.object.age = user_data["age"]
        self.object.location = user_data["location_id"]

        self.object.save()

        return JsonResponse({
                "first_name": self.object.first_name,
                "last_name": self.object.last_name,
                "username": self.object.username,
                "password": self.object.password,
                "role": self.object.role,
                "age": self.object.age,
                "locations": self.object.location_id,
            }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return HttpResponse({"User deleted": "200"}, status=200)
