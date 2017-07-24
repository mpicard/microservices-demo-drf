from pygments.styles import get_all_styles


LANGUAGE_CHOICES = [
    ('python', 'Python'),
    ('python3', 'Python 3'),
    ('rb', 'Ruby'),
    ('sql', 'SQL'),
    ('ts', 'TypeScript'),
    ('typoscript', 'TypoScript'),
    ('yaml', 'YAML')]

STYLE_CHOICES = sorted((i, i) for i in get_all_styles())
