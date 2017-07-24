from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


LEXERS = [i for i in get_all_lexers() if i[1]]
LANGUAGE_CHOICES = sorted([(i[1][0], i[0]) for i in LEXERS])
STYLE_CHOICES = sorted((i, i) for i in get_all_styles())
