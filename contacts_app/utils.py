"""
Utility functions for contacts, including SVG profile generation and name initials extraction.
"""

import random


def generate_svg_circle_with_initials(name, width=120, height=120):
    """
    Generate an SVG profile picture with initials for a given name.
    """
    colors = [
        "#0038FF",
        "#00BEE8",
        "#1FD7C1",
        "#6E52FF",
        "#9327FF",
        "#C3FF2B",
        "#FC71FF",
        "#FF4646",
        "#FF5EB3",
        "#FF745E",
        "#FF7A00",
        "#FFA35E",
        "#FFBB2B",
        "#FFC701",
        "#FFE62B",
    ]
    random_color = random.choice(colors)
    initials = get_initials_from_name(name)
    return _svg_profile_pic(random_color, initials, height, width)


def _svg_profile_pic(color, initials, height, width):
    """
    Return SVG markup for a colored circle with initials.
    """
    return f"""
    <svg class="profilePic" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="{width / 2}" cy="{height / 2}" r="{min(width, height) / 2 - 5}" stroke="white" stroke-width="3" fill="{color}"/>
      <text x="50%" y="52%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="48px">{initials}</text>
    </svg>
    """


def contact_is_no_user_and_user_not_guest(obj, request):
    """
    Check if a contact is not a user and the request user is authenticated and not 'guest'.
    """
    return not obj.is_user and request.user.is_authenticated and request.user.username != "guest"


def get_initials_from_name(name_string):
    """
    Extract initials from a name string. Returns 'N/A' if not possible.
    """
    if not name_string:
        return "N/A"
    name_parts = [n for n in name_string.strip().split() if n]
    if len(name_parts) == 0:
        return "N/A"
    elif len(name_parts) == 1:
        return name_parts[0][0].upper()
    else:
        return (name_parts[0][0] + name_parts[-1][0]).upper()
