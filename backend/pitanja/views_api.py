from django.utils.timezone import now
from rest_framework import permissions, generics, status
from pitanja.models import Test, Pitanje, Odgovor
from pitanja.serializers import *


class TestList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Test.objects.all()  # .filter(datum_vazenja=now())
    serializer_class = TestSerializer
    filter_fields = ['naziv']


class TestDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Test.objects.all()  # .filter(datum_vazenja=now())
    serializer_class = TestSerializer


class PitanjeList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Pitanje.objects.all()  # .filter(test__datum_vazenja=now())
    serializer_class = PitanjeSerializer
    filter_fields = ['test']


class PitanjeDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Pitanje.objects.all()  # .filter(test__datum_vazenja=now())
    serializer_class = PitanjeSerializer


class OdgovorList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Odgovor.objects.all()  # .filter(pitanje__test__datum_vazenja=now())
    serializer_class = OdgovorSerializer
    filter_fields = ['pitanje']


class OdgovorDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Odgovor.objects.all()  # .filter(pitanje__test__datum_vazenja=now())
    serializer_class = OdgovorSerializer


class KompletPitanjeDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Pitanje.objects.all()  # .filter(test__datum_vazenja=now())
    serializer_class = KompletPitanjeSerializer


class KompletTestDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Test.objects.all()  # .filter(test__datum_vazenja=now())
    serializer_class = KompletTestSerializer
