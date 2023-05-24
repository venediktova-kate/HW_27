import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from users.models import User, Location


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        locations = data.pop("locations")
        new = User.objects.create(**data, commit=False)
        for loc_name in locations:
            loc, created = Location.objects.get_or_create(name=loc_name)
            new.locations.add(loc)
        new.save()
        return JsonResponse({"id": new.pk,
                             "first_name": new.first_name,
                             "last_name": new.last_name,
                             "username": new.username,
                             "role": new.role,
                             "age": new.age,
                             "locations": [loc.name for loc in new.locations.all()]
                             })


class UserListView(ListView):
    queryset = User.objects.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True))).order_by("username")
    objects_on_page = 5

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, self.objects_on_page)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return JsonResponse(
            {"total": paginator.count,
             "num_page": paginator.num_pages,
             "items": [{"id": user.pk,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "username": user.username,
                        "role": user.role,
                        "age": user.age,
                        "locations": [loc.name for loc in user.locations.all()],
                        "total_ads": user.total_ads
                        } for user in page_obj]}, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({"id": user.pk,
                             "first_name": user.first_name,
                             "last_name": user.last_name,
                             "username": user.username,
                             "role": user.role,
                             "age": user.age,
                             "locations": [loc.name for loc in user.locations.all()]
                             })


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = "__all__"

    def putch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        if "first_name" in data:
            self.object.first_name = data.get("first_name")
        if "last_name" in data:
            self.object.last_name = data.get("last_name")
        if "username" in data:
            self.object.username = data.get("username")
        if "age" in data:
            self.object.age = data.get("age")
        if "locations" in data:
            self.object.locations.clear()
            for loc_name in data.get("locations"):
                loc, _ = Location.objects.get_or_create(name=loc_name)
                self.object.locations.add(loc)

        return JsonResponse({"id": self.object.pk,
                             "first_name": self.object.first_name,
                             "last_name": self.object.last_name,
                             "username": self.object.username,
                             "role": self.object.role,
                             "age": self.object.age,
                             "locations": [loc.name for loc in self.object.locations.all()]
                             })


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"})
