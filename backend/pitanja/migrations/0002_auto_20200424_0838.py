import random
from pitanja.models import *
from django.db import migrations
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def add_pitanja(apps, schema_editor):
    test = Test.objects.create(naziv='Matematika')
    test.save()
    for i in range(20):
        pitanje = Pitanje.objects.create(test=test, redni_broj=i+1, tip='1',
                                         tekst=f'Pitanje {i+1}: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur id sapien luctus, vulputate sem in, elementum augue. Cras at quam vitae nulla commodo commodo et a ante. Etiam quis diam laoreet, varius purus et, varius neque. Morbi ante mauris, porta ac varius a, sodales at risus. Maecenas eu nisl ut enim congue ultricies. Mauris neque justo, vulputate at convallis varius, rhoncus sed erat. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse molestie eleifend magna, at maximus nulla molestie at. Aenean eget dictum mi, vel volutpat neque. Curabitur ut ipsum eget elit finibus tincidunt sed non justo. Vivamus pretium erat ac dui ullamcorper viverra. Vestibulum ornare eros in risus hendrerit porttitor at ac ex. Nullam venenatis et massa eu hendrerit. Nullam vel ante interdum, tempus tellus quis, viverra nibh. Maecenas quam mauris, congue a eros ut, euismod placerat mi. ')
        pitanje.save()
        tacan_odgovor = random.randrange(4)
        for j in range(4):
            odgovor = Odgovor.objects.create(pitanje=pitanje, redni_broj=j+1, tacan=(tacan_odgovor == j),
                                             tekst=f'Odgovor br {j+1} na pitanje {i+1}')
            odgovor.save()


def add_skole(apps, schema_editor):
    Skola.objects.bulk_create([
        Skola(naziv=f'OŠ {i+1}', adresa=f'Adresa {i+1}', mesto=f'Mesto {i+1}')
        for i in range(1000)])


def add_ucenici(apps, schema_editor):
    # schema_editor.atomic.__exit__(None, None, None)  # izadji iz atomic bloka
    password = make_password('12345')

    User.objects.bulk_create([
        User(username=f'ucenik.{i+1}@gmail.com', email=f'ucenik.{i+1}@gmail.com', password=password, first_name=f'Učenik{i+1}', last_name='Učeniković', is_active=True)
        for i in range(70000)])

    Ucenik.objects.bulk_create([
        Ucenik(user=User.objects.get(id=i+1), skola=Skola.objects.get(id=i//70+1))
        for i in range(70000)])


def add_admin(apps, schema_editor):
    admin = User.objects.create_superuser('mbranko@uns.ac.rs', 'mbranko@uns.ac.rs', '12345')
    admin.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pitanja', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_pitanja),
        migrations.RunPython(add_skole),
        migrations.RunPython(add_ucenici),
        migrations.RunPython(add_admin),
    ]
