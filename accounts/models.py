from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    Per-user profile. Keep minimal for the take-home:
    - display_name: shown in the UI (optional, falls back to username)
    - avatar: optional profile image (requires Pillow)
    - bio: short text about the user
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name or getattr(self.user, 'username', str(self.user))

# Automatically create/update profile when a User is created/updated
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # ensure profile exists; save in case you later add computed fields
        UserProfile.objects.get_or_create(user=instance)