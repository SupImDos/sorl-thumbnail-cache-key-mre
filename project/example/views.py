from django.views.generic import TemplateView
from .models import ExampleModel

class ExampleView(TemplateView):
    template_name = "example.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["example_records"] = ExampleModel.objects.all()
        return context
