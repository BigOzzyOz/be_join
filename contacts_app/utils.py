import random


def generate_svg_circle_with_initials(name, width=120, height=120):
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
    initials = "".join([word[0] for word in name.split()]).upper()
    return svg_profile_pic(random_color, initials, height, width)


def svg_profile_pic(color, initials, height, width):
    return f"""
    <svg class="profilePic" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="{width / 2}" cy="{height / 2}" r="{min(width, height) / 2 - 5}" stroke="white" stroke-width="3" fill="{color}"/>
      <text x="50%" y="52%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="48px">{initials}</text>
    </svg>
    """
