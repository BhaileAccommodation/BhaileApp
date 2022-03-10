from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # set date posted to timezone
    date_posted = models.DateTimeField(default=timezone.now)
    # if user is deleted, delete their posts
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ACCOMMODATION_CATEGORIES = (
        ('TWN', 'Twin'),
        ('SIN', 'Single'),
        ('DOB', 'Double'),
        ('SIN-EN', 'Single EnSuite'),
        ('DOB-EN', 'Double EnSuite'),
        ('HSE', 'Whole House')
    )
    category = models.CharField(max_length=6, choices=ACCOMMODATION_CATEGORIES, null=True)
    capacity = models.IntegerField(null=True)

    # magic method
    def __str__(self):
        return self.title

    def get_accommodation_category(self):
        accommodation_categories = dict(self.ACCOMMODATION_CATEGORIES)
        accommodation_category = accommodation_categories.get(self.category)
        return accommodation_category

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Booking(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(default=timezone.now)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Post, on_delete=models.CASCADE)
    move_in = models.DateTimeField()
    move_out = models.DateTimeField()

    def __str__(self):
        return f'{self.author} has booked {self.accommodation} from {self.move_in} to {self.move_out}'

    def get_accommodation_category(self):
        accommodation_categories = dict(self.accommodation.ACCOMMODATION_CATEGORIES)
        accommodation_category = accommodation_categories.get(self.accommodation.category)
        return accommodation_category

    def get_absolute_url(self):
        return reverse('booking-detail', kwargs={'pk': self.pk})
