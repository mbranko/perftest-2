# Primer aplikacije za ispitivanje performansi

## Potrebne stvari

* Python
* Django
* uWSGI
* Nginx
* Angular

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

Tokom razvoja frontend aplikacije je dostupan na adresi http://localhost:4200/. 
Zahtevi koji se upućuju backendu će biti proksirani kroz Angular server.

## Pokretanje u produkciji

**Server #1** izvršava [Nginx](https://www.nginx.com/). Primer konfiguracije za
Nginx je dat u fajlu `backend/config/nginx.conf`. Deklaracija `upstream`
definiše listu backend servera. Deklaracija `location` određuje kako će se
opsluživati pojedine vrste zahteva. U našem primeru postoje dve `location`
deklaracije: prva definiše prosleđivanje svih zahteva čiji URL počinje sa
`/api` na backend servere, a druga će obraditi sve preostale zahteve
serviranjem fajlova za frontend.

**Server #2** izvršava sistem za upravljanje bazama podataka. U našem primeru
lako je izabrati između PostgreSQL i MySQL sistema - izbor se vrši u
konfiguraciji aplikacije date u `backend/malamatura/app_settings/prod.py`.
Ako će bazi podataka pristupati backend serveri sa različitih mašina, potrebno
je obezbediti da oni mogu da joj pristupe - otvoriti firewall za port 5432
(PostgreSQL) odnosno 3306 (MySQL) za adrese backend servera. U konfiguraciji
baze potrebno je i podesiti da server baze podataka sluša na svim interfejsima
(`listen = '*'` ili `0.0.0.0` umesto `127.0.0.1`).

**Backend serveri** bi trebalo da imaju instaliran Python, definisano virtuelno
okruženje, u njemu instalirane sve potrebne biblioteke (kao i za razvoj), i
pokrenut backend server pomoću:
```bash
cd backend
uwsgi --config config/uwsgi-test.ini
```

Pre pokretanja backend servera pomoću par promenljivih okruženja potrebno je
definisati da se radi o produkcionom serveru i adresu na kojoj se nalazi SUBP.
```bash
export DJANGO_SETTINGS=prod
export POSTGRES_HOST=1.2.3.4
```

## Pokretanje testova

Za pokretanje testova performansi koristićemo biblioteku 
[Locust](https//www.locust.io). Skript koji definiše ponašanje jednog korisnika
sistema je dat u `loadtest/locustfile.py`. Pokretanje testa je najbolje uraditi
na posebnoj mašini (različitoj od servera). Za pokretanje je zgodno koristiti
gotov Docker image za Locust:
```bash
cd loadtest
docker run \
  -p 8089:8089 \
  -p 5557:5557 \
  -v $(pwd)/locustfile.py:/locustfile.py \
  -e TARGET_URL=http://116.203.220.167 \
  --rm \
  locustio/locust
```

Pokrenut server za izvršavanje testa ima svoj web interfejs na portu 8089, a 
na portu 5557 će osluškivati slave servere ukoliko postoje. Nakon pokretanja
servera za izvršavanje testa potrebno je otvoriti browser na njegovoj adresi
i portu 8089, i odatle definisati broj korisnika koji se simulira i pokrenuti
test.
