from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='ticket')
    time_created = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    name = models.CharField(max_length=100)
    ticket = models.ForeignKey(to=Ticket, null=True, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    @property
    def display_rating(self):
        full_star = ''
        empty_star = ''
        for i in range(self.rating):
            full_star += '<i class="bi bi-star-fill"></i>'
        for i in range(5-self.rating):
            empty_star += '<i class="bi bi-star"></i>'
        return full_star + empty_star

class UserFollows(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='followed_by')
    class Meta:
        unique_together = ('user', 'followed_user', )
        verbose_name_plural = 'UserFollows'
