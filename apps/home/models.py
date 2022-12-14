from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from tinymce.models import HTMLField

def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "servicios/%s/%s.%s" % (instance.id, instance.id, extension)
    # return "%s/%s" % (instance.id, filename)

def upload_location_equipo(instance, filename):
    filebase, extension = filename.split(".")
    return "equipo/%s/%s.%s" % (instance.id, instance.id, extension)
    # return "%s/%s" % (instance.id, filename)

def upload_location_certificacion(instance, filename):
    filebase, extension = filename.split(".")
    return "certificacion/%s/%s.%s" % (instance.id, instance.id, extension)
    # return "%s/%s" % (instance.id, filename)

def upload_location_pdf(instance, filename):
    filebase, extension = filename.split(".")
    return "pdf/%s/%s.%s" % (instance.id, instance.id, extension)
    # return "%s/%s" % (instance.id, filename)

class Servcio(models.Model):
    CATEGORIA = (
        ('1', 'Vigilancia'),
        ('2', 'Estudios'),
        ('3', 'Monitoreos'),
        ('4', 'Laboratorio'),
    )
    nombre = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=1000, null=True, blank=True)
    categoria = models.CharField(choices=CATEGORIA, max_length=20)
    descripcion = HTMLField('Descripcion')
    img = models.ImageField(upload_to=upload_location,
                                  null=True,
                                  blank=True,
                                  editable=True)
    publicado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

def create_slug(instance, new_slug=None):
    slug = slugify(instance.nombre)
    if new_slug is not None:
        slug = new_slug
    qs = Servcio.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_servicio_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_servicio_receiver, sender=Servcio)

class Equipo(models.Model):
    nombre_completo = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    url_twitter = models.URLField(blank=True, null=True)
    url_linkedin = models.URLField(blank=True, null=True)
    img = models.ImageField(upload_to=upload_location_equipo,
                            null=True,
                            blank=True,
                            editable=True)
    publicado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_completo

    class Meta:
        verbose_name = 'Integrante'
        verbose_name_plural = 'Integrantes'

class Certificacion(models.Model):
    nombre_certificacion = models.CharField(max_length=50)
    img = models.ImageField(upload_to=upload_location_certificacion,
                            null=True,
                            blank=True,
                            editable=True)
    pdf_file = models.FileField(upload_to=upload_location_pdf,
                                null=True,
                                blank=True,
                                editable=True)
    publicado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_certificacion

    class Meta:
        verbose_name = 'Certificaci??n'
        verbose_name_plural = 'Certificaciones'

class Contacto(models.Model):
    TEMA = (
        ('1', 'Quejas'),
        ('2', 'Segerencias'),
        ('3', 'Cotizaciones'),
        ('4', 'Otro'),
    )
    nombre_completo = models.CharField(max_length=250)
    email = models.EmailField()
    fono = models.CharField(max_length=14)
    tema = models.CharField(max_length=250, choices=TEMA, blank=True, null=True)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.nombre_completo

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'