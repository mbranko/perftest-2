# Primer webshop aplikacije: SPA, REST, Docker

## Potrebne stvari

* Python
* Django
* Docker

## Podešavanje za razvoj

Kreiranje virtuelnog okruženja:
```bash
python3 -m venv ~/path/to/new/venv
source ~/path/to/new/venv/bin/activate
```

Sve naredne operacije obavljaju se iz korenskog direktorijuma Django
projekta, dakle `backend`.

Instaliranje potrebnih paketa
```bash
pip install -r requirements.txt
```

Migracija baze na poslednju verziju:
```bash
python manage.py migrate
```

Pokretanje testova:
```bash
python manage.py test
```

Pokretanje razvojnog servera:
```bash
python manage.py runserver
```

Pokretanje Angular servera:
```bash
cd frontend
ng serve
```

Tokom razvoja frontend aplikacije je dostupan na adresi http://localhost:4200/. Zahtevi koji se upućuju
backendu će biti proksirani kroz Angular server.

## Kreiranje image-a za produkciju

Postaviti se u direktorijum gde stoji fajl `Dockerfile`.

Kreiranje Docker image-a:
```bash
docker build -t malamatura:latest .
docker tag malamatura:latest brankomilosavljevic/malamatura:latest
docker push brankomilosavljevic/malamatura:latest
```

Pokretanje PostgreSQL baze:
```bash
docker run --name malamaturadb -e POSTGRES_USER=malamatura -e POSTGRES_PASSWORD=malamatura -d postgres:12.2
```

Pokretanje aplikacije:
```bash
docker run \
  --name malamatura \
  -p 8000:8000 \
  --link malamaturadb \
  -v `pwd`/malamatura.log:/app/log/malamatura.log \
  -v `pwd`/uwsgi.log:/app/log/uwsgi.log \
  --detach \
  malamatura:latest
```

Ili ako cemo da zabranimo da se isti test radi vise puta:
```bash
docker run --name malamatura -e ALLOW_REPEATED_TESTS=False -p 8000:8000 --link malamaturadb -d malamatura:latest
```

