import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Category


def main(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryListCreateView(View):
    def get(self, request):
        categories = Category.objects.all()
        return JsonResponse([{"id": cat.pk, "name": cat.name} for cat in categories], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new = Category.objects.create(name=data.get("name"))
        return JsonResponse({"id": new.pk, "name": new.name})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({"id": cat.pk, "name": cat.name})