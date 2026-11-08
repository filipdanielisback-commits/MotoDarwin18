import unittest

from tools.xnuloader_display_layout import DisplayMode, calculate_menu_layout


class DisplayModeTests(unittest.TestCase):
    def test_accepts_known_format_and_larger_stride(self):
        DisplayMode(480, 800, 512, "PixelBlueGreenRedReserved8BitPerColor").validate()

    def test_accepts_blt_only_as_metadata(self):
        DisplayMode(320, 600, 320, "PixelBltOnly").validate()

    def test_rejects_non_positive_dimensions(self):
        with self.assertRaises(ValueError):
            DisplayMode(0, 600, 600, "PixelBltOnly").validate()

    def test_rejects_stride_smaller_than_width(self):
        with self.assertRaises(ValueError):
            DisplayMode(480, 800, 479, "PixelBltOnly").validate()

    def test_rejects_unknown_pixel_format(self):
        with self.assertRaises(ValueError):
            DisplayMode(480, 800, 480, "UnknownFormat").validate()

    def test_rejects_boolean_dimensions(self):
        with self.assertRaises(ValueError):
            DisplayMode(True, 800, 800, "PixelBltOnly").validate()


class DisplayLayoutTests(unittest.TestCase):
    def assert_layout_inside(self, mode, layout):
        for rect in (layout.title, *layout.items, layout.status):
            self.assertTrue(rect.inside(mode.width, mode.height))

    def test_portrait_layout_is_inside_surface(self):
        mode = DisplayMode(480, 800, 480, "PixelBltOnly")
        layout = calculate_menu_layout(mode, 2)
        self.assertEqual(len(layout.items), 2)
        self.assert_layout_inside(mode, layout)

    def test_landscape_layout_is_inside_surface(self):
        mode = DisplayMode(1280, 720, 1280, "PixelRedGreenBlueReserved8BitPerColor")
        layout = calculate_menu_layout(mode, 2)
        self.assert_layout_inside(mode, layout)

    def test_items_are_vertically_ordered_and_separated(self):
        mode = DisplayMode(480, 800, 480, "PixelBltOnly")
        layout = calculate_menu_layout(mode, 3)
        self.assertLess(layout.items[0].y, layout.items[1].y)
        self.assertLess(layout.items[1].y, layout.items[2].y)
        self.assertGreaterEqual(layout.items[1].y, layout.items[0].y + layout.items[0].height)

    def test_rejects_zero_items(self):
        with self.assertRaises(ValueError):
            calculate_menu_layout(DisplayMode(480, 800, 480, "PixelBltOnly"), 0)

    def test_rejects_too_small_surface(self):
        with self.assertRaises(ValueError):
            calculate_menu_layout(DisplayMode(100, 100, 100, "PixelBltOnly"), 2)

    def test_rejects_boolean_item_count(self):
        with self.assertRaises(ValueError):
            calculate_menu_layout(DisplayMode(480, 800, 480, "PixelBltOnly"), True)


if __name__ == "__main__":
    unittest.main()
