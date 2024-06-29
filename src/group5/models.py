from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Part(models.Model):
    category = models.ForeignKey(Category, related_name='parts', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Word(models.Model):
    part = models.ForeignKey(Part, related_name='words', on_delete=models.CASCADE)
    exact_word = models.CharField(max_length=100)
    definition = models.TextField()
    image = models.ImageField(upload_to='word_images/')

    def __str__(self):
        return self.exact_word
