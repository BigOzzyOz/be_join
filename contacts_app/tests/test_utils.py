import unittest
from contacts_app.utils import generate_svg_circle_with_initials, svg_profile_pic


class TestUtils(unittest.TestCase):
    def test_generate_svg_circle_with_initials(self):
        name = "John Doe"
        svg = generate_svg_circle_with_initials(name)

        self.assertIn("JD", svg)
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
        self.assertTrue(any(color in svg for color in colors))
        self.assertIn('width="120"', svg)
        self.assertIn('height="120"', svg)

    def test_svg_profile_pic(self):
        color = "#FF0000"
        initials = "JD"
        width = 100
        height = 100
        svg = svg_profile_pic(color, initials, height, width)

        self.assertIn("JD", svg)
        self.assertIn('fill="#FF0000"', svg)
        self.assertIn('width="100"', svg)
        self.assertIn('height="100"', svg)
        self.assertIn(f'cx="{width / 2}"', svg)
        self.assertIn(f'cy="{height / 2}"', svg)
        self.assertIn(f'r="{min(width, height) / 2 - 5}"', svg)


if __name__ == "__main__":
    unittest.main()
