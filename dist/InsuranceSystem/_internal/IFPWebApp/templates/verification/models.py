# verification/models.py
from django.db import models
from django.utils import timezone
import random

class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = str(random.randint(100000, 999999))
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=3)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def remaining_time(self):
        return self.expires_at - timezone.now()