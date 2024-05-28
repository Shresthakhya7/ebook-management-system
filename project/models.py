from django.db import models
from django.contrib.auth.models import User

class Ebook(models.Model):
    CATEGORY_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Biography', 'Biography'),
        ('Self Help', 'Self Help'),
    ]
        
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Fiction')
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    file = models.FileField(upload_to='ebooks/')
    
    def __str__(self):
        return self.title


class UserReading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    read_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.ebook.title} - {self.read_count}'