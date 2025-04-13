from django.test import TestCase
from contacts_app.utils import generate_svg_circle_with_initials, _svg_profile_pic, get_initials_from_name


class TestUtils(TestCase):
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
        self.assertTrue(any(f'fill="{color}"' in svg for color in colors))
        self.assertIn('width="120"', svg)
        self.assertIn('height="120"', svg)

    def test_svg_profile_pic(self):
        color = "#FF0000"
        initials = "JD"
        width = 100
        height = 100
        svg = _svg_profile_pic(color, initials, height, width)

        self.assertIn("JD", svg)
        self.assertIn('fill="#FF0000"', svg)
        self.assertIn('width="100"', svg)
        self.assertIn('height="100"', svg)
        self.assertIn(f'cx="{width / 2.0}"', svg)
        self.assertIn(f'cy="{height / 2.0}"', svg)
        self.assertIn(f'r="{min(width, height) / 2.0 - 5}"', svg)

    def test_get_initials_from_name_two_words(self):
        self.assertEqual(get_initials_from_name("John Doe"), "JD")
        self.assertEqual(get_initials_from_name("  Jane   Smith  "), "JS")

    def test_get_initials_from_name_one_word(self):
        self.assertEqual(get_initials_from_name("Single"), "S")
        self.assertEqual(get_initials_from_name(" another "), "A")

    def test_get_initials_from_name_multiple_words(self):
        self.assertEqual(get_initials_from_name("Mary Anne Jones"), "MJ")
        self.assertEqual(get_initials_from_name("Peter van der Beek"), "PB")

    def test_get_initials_from_name_empty_or_whitespace(self):
        self.assertEqual(get_initials_from_name(""), "N/A")
        self.assertEqual(get_initials_from_name("   "), "N/A")
        self.assertEqual(get_initials_from_name(None), "N/A")

    def test_get_initials_from_name_lowercase(self):
        self.assertEqual(get_initials_from_name("john doe"), "JD")
        self.assertEqual(get_initials_from_name("single"), "S")
