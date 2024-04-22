from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _

#This signal create Auth Token for users 
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    #groups = models.ForeignKey(Group, on_delete=models.CASCADE, default=2)
    username = models.CharField(blank=True, null=True,max_length=11)
    email = models.EmailField(_('email address'), unique=True)
    friends = models.ManyToManyField('self', symmetrical=False, through='Friendship', related_name='user_friends')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'



@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs ):
    if created:
        Token.objects.create(user=instance)



class Friendship(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['from_user', 'to_user']
       