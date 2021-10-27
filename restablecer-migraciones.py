import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webecogestion.settings")
django.setup()

from django.conf import settings

# eliminamos el contenido de las carpetas migrations y si no existen se crean
ext_apps = ["django_filters", "rest_framework", "rest_framework_xml", "storages", "crispy_forms", "widget_tweaks",
            "rest_framework.authtoken"]

aplicaciones = settings.INSTALLED_APPS
for a in aplicaciones:

    if a not in ext_apps and len(a.split('.')) == 2:
        print('\nAplicacion:', a)
        # convierto el nombre de la aplicacion en una ruta
        a = a.replace('.', '/')

        if not os.path.isdir(a + "/migrations"):
            print(' La aplicacion no tiene carpeta migrations')
            os.mkdir(a + "/migrations")
            open(a + "/migrations/__init__.py", "w+")
            print(" -creando carpeta: " + a + "/migrations  y archivo __init__.py")
        else:
            print(' La aplicacion no tiene carpeta migrations')
            for file in os.scandir(a + "/migrations/"):
                if file.name.endswith(".py"):
                    os.unlink(file.path)
                    print(" -limpiando contenido de carpeta " + a + "/migrations/")
            if not os.path.isfile(a + "/migrations/__init__.py"):
                open(a + "/migrations/__init__.py", "w+")
                print(" -Creando archivo " + a + "/migrations/__init__.py")
