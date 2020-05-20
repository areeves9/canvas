import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
def create_action(user, verb, target=None):
    # prevent duplicate actions from being submitted
    # has a similar action occured within the previous 60 s?
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    # similar actions that have occured in the past 60s
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)

    if target:
        target_content = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_content=target_content, target_id=target.id)

    if not similar_actions:
        # there are no existing actions
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False


class Action(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='actions',
        db_index=True
    )
    verb = models.CharField(max_length=225)
    target_content = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='target_object'
    )
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_content', 'target_id')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
