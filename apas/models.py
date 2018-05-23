from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Rungtynes(models.Model):
    komanda1 = models.CharField(max_length=100)
    komanda2 = models.CharField(max_length=100)
    kofas1 = models.FloatField(default=0)
    kofas2 = models.FloatField(default=0)
    kofasx = models.FloatField(default=0)
    data = models.DateTimeField(default=timezone.now())
    prasidejo = models.BooleanField(default=False)
    baigtis = models.CharField(max_length=2, default='NA')
    rezultatas = models.CharField(max_length=5, default=' : ')

    def __str__(self):
        return self.komanda1 + '-' + self.komanda2 + ': ' + self.rezultatas


class Zaidejas(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='zaidejas')
    taskai = models.FloatField(default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Zaidejas.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.zaidejas.save()


class Stavke(models.Model):
    zaidejas = models.ForeignKey(Zaidejas, on_delete=models.CASCADE, related_name='zaidejas')
    rungtynes = models.ForeignKey(Rungtynes, on_delete=models.CASCADE, related_name='rungtynes')
    pasirinkimas = models.CharField(max_length=1, default='')
    laimeta = models.BooleanField(default=False)
    laimejimas = models.FloatField(default=0)

    def __str__(self):
        return self.rungtynes.__str__() + ': ' + self.zaidejas.__str__() + '--' + self.pasirinkimas
