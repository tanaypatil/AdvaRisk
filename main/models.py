from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models


class Review(models.Model):
    product = models.CharField(max_length=15, blank=False)
    user = models.CharField(max_length=15, blank=False)
    name = models.CharField(max_length=100, blank=False)
    helpfulness = models.CharField(max_length=20, blank=False)
    score = models.FloatField(blank=False)
    timestamp = models.DateTimeField(blank=False)
    summary = models.CharField(max_length=500, blank=False)
    text = models.TextField(max_length=2000, blank=False)
    search_vector = SearchVectorField(null=True)

    def __str__(self):
        return f"{self.product}_{self.user}"

    class Meta:
        indexes = [GinIndex(fields=["search_vector"], name="search_gin_idx")]

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        Review.objects.filter(pk=self.pk).update(search_vector=SearchVector('text'))
