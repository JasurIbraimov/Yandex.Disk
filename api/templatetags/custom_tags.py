from django import template

register = template.Library()

@register.filter(name='bytes_to_gb')
def bytes_to_gb(value):
    """Convert bytes to gigabytes"""
    try:
        # Convert bytes to GB (1 GB = 1024^3 bytes)
        gigabytes = value / (1024 ** 3)
        return f"{gigabytes:.2f} GB"
    except (ValueError, TypeError):
        return "Invalid value"