from rest_framework import serializers
from pitanja.models import Test, Pitanje, Odgovor, OdgovorUcenika


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class PitanjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitanje
        fields = '__all__'


class OdgovorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odgovor
        fields = '__all__'


class KompletOdgovorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odgovor
        fields = ['id', 'redni_broj', 'tekst']


class KompletPitanjeSerializer(serializers.ModelSerializer):
    odgovor_set = KompletOdgovorSerializer(many=True, read_only=True)

    class Meta:
        model = Pitanje
        fields = ['id', 'redni_broj', 'tip', 'tekst', 'odgovor_set']


class KompletTestSerializer(serializers.ModelSerializer):
    pitanje_set = KompletPitanjeSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'naziv', 'datum_vazenja', 'pitanje_set']


class OdgovorUcenikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OdgovorUcenika
        fields = '__all__'
