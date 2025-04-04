# Instrukcja instalacji i uruchomienia

<img src="https://pbs.twimg.com/media/Gckuo8OXMAARQqZ.png" alt="average documentation reader" width=250>

Drzewo projektu:
```
.
└── ./rejProjekt/
    ├── ./rejProjekt/rej_project/
    │   ├── ./rejProjekt/rej_project/rej_app/
    │   ├── ./rejProjekt/rej_project/rej_project/
    │   ├── ./rejProjekt/rej_project/db.sqlite3
    │   └── ./rejProjekt/rej_project/manage.py
    ├── ./rejProjekt/testowe_pliki/ # można usunąć
    ├── ./rejProjekt/venv/ # Windows (można usunąć - info niżej)
    ├── ./rejProjekt/venv_mac/ # MacOS (można usunąć - info niżej)
    └── ./rejProjekt/requirements.txt
```
## Podstawowe wymagania projektu
 
 - Python 3.12.3
 - IDE (VSC lub inne obsługujące Pythona)
 - Utworzenie pliku ```.env``` w głównej lokalizacji projektu ```cd rejProjekt``` oraz wpisanie w nim zmiennej ```DJANGO_SECRET_KEY=klucz```, klucz został przesłany w wiadomości.

### Instalacja wymagań: **Linux**
Z uwagi na częste braki ```pip``` oraz ```venv``` w przypadku Linuxa dokonaj weryfikacji czy je posiadasz:

**PIP**

```
pip3 --version
# lub
python3 -m pip --version
```

Jeśli powyższe komendy nie działają - brakuje ```pip``` - doinstaluj:
```
sudo dnf install python3-pip    # RHEL/Fedora/CentOS 8+
sudo yum install python3-pip    # Starsze RHEL/CentOS
sudo apt install python3-pip    # Debian/Ubuntu
```

**VENV**

```
python3 -m venv --help
```

Jeśli powyższa komenda nie działa - brakuje ```venv``` - doinstaluj:
```
sudo dnf install python3-venv   # Dla RHEL 8+/Fedora
sudo yum install python3-venv   # Dla starszych wersji
sudo apt install python3-venv   # Dla Debian/Ubuntu
```

> [!WARNING]
> Jeśli projekt jest świeżo pobrany - usuń utworzone venv (venv, venv_mac).<br>
> **Poniższe komendy wpisuj w terminalu będąc w lokalizacji głównej: ```cd rejProjekt```**
1. Utwórz nowe venv:
```
python3 -m venv venv_linux
```

2. Aktywacja środowiska:
```
source venv_linux/bin/activate
```
   
> [!NOTE]
> Po prawidłowej aktywacji środowiska konsola powinna wyglądać tak:<br>
> ```(venv_linux) [user@host ~]$```<br>
> Komenda do deaktywacji: ```deactivate```

3. Zainstaluj wymagane paczki (będąć w aktywnym środowisku ```venv_linux``` i poprawnej lokalizacji):
```
pip install -r requirements.txt
```

Jeśli z jakiegoś powodu komenda nie działa spróbuj wymusić użycie Pythona:
```
python3 -m pip install -r requirements.txt
```

4. Utwórz plik .env w głównej lokalizacji (jeśli do tworzenia pliku używasz terminala to przed tworzeniem opuść ```venv``` komendą ```deactivate```.<br>
W pliku .env wpisz zmienną:
```
DJANGO_SECRET_KEY=klucz #klucz został udostępniony w wiadomości
```

5. Uruchomienie projektu (ponownie uruchom venv jeśli dezaktywowałeś je w poprzednim kroku):
Przejdź do ściezki ```cd rej_project```, powinieneś znajdować się w tej części drzewa:
```
.
└── ./rejProjekt/
    ├── ./rejProjekt/rej_project/
```
Uruchom plik manage.py:
```
python3 manage.py runserver
```
> [!NOTE]
> Jeśli wszystko poszło poprawnie w konsoli powinieneś zobaczyć:
>```
>System check identified no issues (0 silenced).
>April 01, 2025 - 22:30:14
>Django version 5.1.7, using settings 'rej_project.settings'
>Starting development server at http://127.0.0.1:8000/
>Quit the server with CTRL-BREAK.
>```

Serwer wystartował zgodnie z ustawieniami na 127.0.0.1 oraz porcie 8000.<br>
> [!TIP]
> Aby zmienić te ustawienia, przejdź do pliku settings.py (folder ```rej_project/rej_project```).<br>
> W zmiennej ```ALLOWED_HOSTS = [127.0.0.1]``` wpisz adres, na którym chcesz uruchomić projekt - domenę lub numeryczny (**bez portu!**).<br>
> Jeśli chcesz zmienić port to przy starcie ```python3 manage.py runserver``` dopisz port (dla przykładu użyję ```8080```):<br>
> ```python3 manage.py runserver 8080```<br>
> Pelna komenda do uruchomienia po dokonaniu zmian:<br>
> ```python3 manage.py runserver IP:PORT```

Gotowe :)

### Windows/MacOS

Windows oraz MacOS mają gotowe ```venv```, przy instalacji Pythona ```pip``` i ```venv``` instalują się automatycznie.

W zależności od systemu uruchom ```venv``` będąc w głównym folderze ```rejProjekt```:
- Windows:
  ```venv\Scripts\activate```
- MacOS:
  ```source venv_mac/bin/activate```

Następnie gdy masz aktywowane środowisko przejdź do aktualizacji paczek.
Wpisz komendę:
```pip install -r requirements.txt```

Przejdź do ```rej_project```, a następnie wpisz ```py manage.py runserver```.

## Konfiguracja gunicorn + myapp.service
Do poprawnego działania myapp.service (aby Django obsługiwało >1 request) zainstaluj gunicorn wewnątrz ```venv_linux```:<br>
```pip install gunicorn```<br>

Pobierz plik myapp.service, skonfiguruj w nim (niektóre wartości w pliku są już ustawione, zweryfikuj czy ścieżka u Ciebie jest poprawna): 
-```User```,<br>
-```Group``` (domyślnie www-data),<br>
-```WorkingDirectory``` - wskaż ścieżkę do projektu,<br>
-```Environment``` - wskaż ścieżkę do venv/bin,<br>
-```ExecStart``` - wskaż ścieżkę do gunicorn (po /bin/) oraz wprowadź komendę ```/twoja_sciezka/uzytkownik/rejProjekt/venv/bin/gunicorn --workers 3 --bind IP:PORT rej_project.wsgi:application```,<br>
-```Restart```.<br>
> [!IMPORTANT]  
> Plik musi znajdować się w ```/etc/systemd/system/myapp.service```<br>
> Wymuś wykrycie pliku - ```sudo systemctl daemon-reload```<br>
> Uruchom - ```sudo systemctl start myapp```<br>
> Autostart (opcjonalne) - ```sudo systemctl enable myapp```<br>
> Weryfikacja statusu - ```sudo systemctl status myapp```<br>
