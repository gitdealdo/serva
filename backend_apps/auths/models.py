from uuid import uuid4

from django.contrib.auth.models import AbstractUser, UserManager, Permission
from django.db import models


# Create your models here.

class Person(models.Model):
    """Model Person.

        Model for authenticate user and save personal dates.
    """
    DNI = 'DNI'
    FOREING_CARD = 'FC'
    OTHER = 'OTROS'
    IDENTITY_TYPE_CHOICES = (
        (DNI, 'DNI'),
        (FOREING_CARD, 'Canet de Extranjería'),
        (OTHER, 'Otros'),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    # first_name = models.CharField("Firs Name", max_length=50)
    identity_type = models.CharField(
        max_length=15, choices=IDENTITY_TYPE_CHOICES, default=DNI)
    identity_num = models.CharField(
        max_length=20, error_messages={'unique': "eeeee ee"})
    photo = models.ImageField(upload_to='persons', default='persons/user.png')
    cellphone = models.CharField(max_length=15, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField("Address", max_length=100)

    updated_at = models.DateTimeField("Updated at", auto_now=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return '%s, %s' % (self.user.first_name, self.user.last_name)


class User(AbstractUser):
    u"""
    Curtom User.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    person = models.OneToOneField(
        Person, verbose_name="Person", blank=True, null=True)
    theme = models.CharField(max_length=20, default="default")
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        permissions = (
            ('list_user', 'Can list user'),
            ('get_user', 'Can get user'),
        )

    def __str__(self):
        return self.username


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(u'Título', max_length=50)
    url = models.CharField(max_length=150, default='#')
    pos = models.IntegerField('Position', default=1)
    icon = models.CharField('Icon', max_length=50,
                            null=True, blank=True, default='')
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    permission = models.ForeignKey(
        Permission, verbose_name="permission", null=True, blank=True)
    parent = models.ForeignKey(
        'self', verbose_name='Parent', null=True, blank=True)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        permissions = (
            ('list_menu', 'Can list menu'),
            ('get_menu', 'Can get menu'),
        )

    def __str__(self):
        return "%s" % (self.title)
