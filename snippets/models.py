from django.db import models

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

from . import LANGUAGE_CHOICES, STYLE_CHOICES


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Snippet(TimeStampedMixin):
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python3', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='monokai', max_length=100)
    highlighted = models.TextField()

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        """
        Business Logic: use `pygments` to highlight code.
        (called on create and update)
        """
        lexer = get_lexer_by_name(self.language)
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style,
                                  linenos=self.linenos,
                                  full=True,
                                  **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        return super().save(*args, **kwargs)
