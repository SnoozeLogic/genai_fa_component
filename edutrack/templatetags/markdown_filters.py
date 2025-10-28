from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()


@register.filter(name='format_markdown')
def format_markdown(text):
    """
    Convert markdown text to beautifully formatted HTML.
    Uses the Python markdown library with extensions for better formatting.
    """
    if not text:
        return ""
    
    # Convert to string if needed
    text = str(text)
    
    # Use markdown library with extensions
    html = md.markdown(
        text,
        extensions=[
            'extra',      # Tables, footnotes, fenced code blocks, etc.
            'nl2br',      # Newline to break
            'sane_lists', # Better list handling
        ]
    )
    
    return mark_safe(html)

