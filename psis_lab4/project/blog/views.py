from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View

from .models import Article
from .forms import ArticleForm


def generate_lights_data(value):
    try:
        lightning_value = int(value.split(' ')[1])  # Перевод из строки в число
    except ValueError:
        lightning_value = 0

    if lightning_value > settings.MAX_SENSOR_VALUE:
        lights_count = settings.MAX_LIGHTS_NUMBER
    else:
        lights_count = lightning_value // 100  # WTKFZ XFCNM JN LTKTYBZ YF 100

    # 1-длинна списка равна числу загорревшихся
    # 0-  длинна списка равна числу потухших
    lights = [1 for x in range(lights_count)] + \
        [0 for i in range(settings.MAX_LIGHTS_NUMBER - lights_count)]

    return {
        'lights': lights,
        'lightning_value': lightning_value
    }


class ArticlesList(generic.ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'blog/main.html'

    def get(self, *args, **kwargs):

        with open('logs/check_lightning.log', 'r') as file:
            try:
                lightning_list = list(file)[-5: -1]
                lightning_list = [generate_lights_data(
                    x) for x in lightning_list]
            except IndexError:
                lightning_list = []

        # Возращает ответ
        return render(
            self.request,
            self.template_name,
            {
                'articles': self.get_queryset(),
                'lights_list': lightning_list
            }
        )


class ArticleCreate(generic.CreateView):
    form_class = ArticleForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('main')
