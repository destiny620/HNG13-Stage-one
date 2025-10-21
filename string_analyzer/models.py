from django.db import models
from django.utils import timezone


class StringAnalysis(models.Model):
    string_value = models.CharField(max_length=255, unique=True)
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.JSONField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length=64)
    character_frequency_map = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.string_value
