from django.urls import path, include
from pitanja.views import index, pocni_test, unesi_odgovor, zavrsi_test, rezime

app_name = 'pitanja'

urlpatterns = [
    path('api/', include('pitanja.urls_api', namespace='pitanja_api')),
    path('api/pocetak/', pocni_test),
    path('api/odgovor/', unesi_odgovor),
    path('api/rezime/<int:test_ucenika_id>/', rezime),
    path('api/kraj/', zavrsi_test),
    path('', index),
]
