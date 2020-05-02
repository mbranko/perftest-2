from django.conf import settings
from django.utils.timezone import now
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from pitanja.models import Test, Pitanje, TestUcenika, OdgovorUcenika
from pitanja.serializers import OdgovorUcenikaSerializer, TestSerializer


def index(request):
    return render(request, 'pitanja/index.html')


@api_view(['POST'])
def pocni_test(request):
    try:
        ucenik = request.user.ucenik
        test = Test.objects.get(id=request.data['test'])
        test_ucenika = TestUcenika.objects.filter(test=test, ucenik=ucenik)
        if len(test_ucenika) > 0 and not settings.ALLOW_REPEATED_TESTS:
            return Response(status=status.HTTP_409_CONFLICT)
        else:
            test_ucenika = TestUcenika.objects.create(test=test, ucenik=ucenik)
            test_ucenika.save()
            return Response({'test_ucenika': test_ucenika.id}, status=status.HTTP_201_CREATED, content_type='application/json')
    except Test.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def unesi_odgovor(request):
    try:
        ucenik = request.user.ucenik
        test_ucenika = TestUcenika.objects.get(id=request.data['test_ucenika'])
        if ucenik != test_ucenika.ucenik:
            return Response(status=status.HTTP_403_FORBIDDEN)
        pitanje = Pitanje.objects.get(id=request.data['pitanje'])
        if test_ucenika.test != pitanje.test:
            return Response(status=status.HTTP_403_FORBIDDEN)
        odgovor = request.data['odgovor']
        try:
            odgovor_ucenika = OdgovorUcenika.objects.get(test_ucenika=test_ucenika, pitanje=pitanje)
            odgovor_ucenika.odgovor = odgovor
            odgovor_ucenika.save()
        except OdgovorUcenika.DoesNotExist:
            odgovor_ucenika = OdgovorUcenika.objects.create(test_ucenika=test_ucenika, pitanje=pitanje, odgovor=odgovor)
            odgovor_ucenika.save()
        return Response(status=status.HTTP_201_CREATED)
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except TestUcenika.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Pitanje.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def zavrsi_test(request):
    try:
        ucenik = request.user.ucenik
        test_ucenika = TestUcenika.objects.get(id=request.data['test_ucenika'])
        if ucenik != test_ucenika.ucenik:
            return Response(status=status.HTTP_403_FORBIDDEN)
        test_ucenika.kraj_rada = now()
        test_ucenika.save()
        return Response({'status': 'OK'}, status=status.HTTP_201_CREATED, content_type='application/json')
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except TestUcenika.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def rezime(request, test_ucenika_id):
    try:
        ucenik = request.user.ucenik
        test_ucenika = TestUcenika.objects.get(id=test_ucenika_id)
        if ucenik != test_ucenika.ucenik:
            return Response(status=status.HTTP_403_FORBIDDEN)
        odgovori = OdgovorUcenika.objects.filter(test_ucenika=test_ucenika).order_by('pitanje__redni_broj')
        serializer = OdgovorUcenikaSerializer(odgovori, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')
    except TestUcenika.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


from django.views.decorators.cache import cache_page

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@cache_page(60*60)
def test(request, pk):
    print(request.headers)
    try:
        test_ = Test.objects.get(pk=pk)
        serializer = TestSerializer(test_)
        return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
