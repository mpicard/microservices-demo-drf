"""
Models
======

Define relational objects using fields, foreign Keys and many-to-manys
as well as business logic related to the model.
"""
from django.db import models

import pygments

from . import LANGUAGE_CHOICES, STYLE_CHOICES


class Snippet(models.Model):
    """
    A short piece of code with syntax highlighting.
    """
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=100, blank=True, default='')

    code = models.TextField()

    linenos = models.BooleanField(default=False)

    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        default='python3',
        max_length=100)

    style = models.CharField(
        choices=STYLE_CHOICES,
        default='monokai',
        max_length=100)

    owner = models.ForeignKey(
        'auth.User',
        related_name='snippets',
        on_delete=models.CASCADE)

    highlighted = models.TextField()

    class Meta:
        ordering = ('created',)
        # db_table = 'some_other_table_name'
        # indexes = [models.Index(fields=['title'])]
        # unique_together = ('title', 'owner',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Business Logic: use `pygments` to highlight code.
        (called on create and update)
        """
        lexer = pygments.lexers.get_lexer_by_name(self.language)
        options = self.title and {'title': self.title} or {}
        formatter = pygments.formatters.html.HtmlFormatter(
            style=self.style,
            linenos=self.linenos,
            full=True,
            **options)
        self.highlighted = pygments.highlight(self.code, lexer, formatter)
        return super().save(*args, **kwargs)

    # def delete(self):

    # def create(self):

    # def update(self):
