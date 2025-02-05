from django.db import models
import random

class Person(models.Model):
    """Represents a quotable person."""
    name = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
    
    def get_random_image(self):
        """Returns any random image of this Person."""
        images = Image.objects.filter(person=self)
        return random.choice(images)
 
    def get_all_images(self):
        """Returns any random image of this Person."""
        images = Image.objects.filter(person=self)
        return images

    def get_all_quotes(self):
        """Returns any random image of this Person."""
        quotes = Quote.objects.filter(person=self)
        return quotes


class Quote(models.Model):
    """Represents a quote by a famous person."""
    text = models.TextField(blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True) # quote-to-person = many-to-one

    def __str__(self) -> str:
        return f'"{self.text}" - {self.person}'
    

class Image(models.Model):
    """Represents an image_url for a person."""
    image_url = models.URLField(blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True) # image-to-person = one-to-one

    def __str__(self) -> str:
        return self.image_url