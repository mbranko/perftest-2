from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from pitanja.views_api import *
from pitanja.views import test
from django.views.decorators.cache import cache_page

app_name = 'pitanja'

urlpatterns = [
    path('testovi/', cache_page(60*60)(TestList.as_view())),
    path('testovi/<int:pk>/', cache_page(60*60)(TestDetail.as_view())),
    # path('testovi/<int:pk>/', test),
    path('pitanja/', cache_page(60*60)(PitanjeList.as_view())),
    path('pitanja/<int:pk>/', cache_page(60*60)(PitanjeDetail.as_view())),
    path('odgovori/', OdgovorList.as_view()),
    path('odgovori/<int:pk>/', OdgovorDetail.as_view()),
    path('komplet-test/<int:pk>/', cache_page(60*60)(KompletTestDetail.as_view())),
    path('komplet-pitanje/<int:pk>/', KompletPitanjeDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
