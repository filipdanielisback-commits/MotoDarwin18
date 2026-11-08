import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from xnuloader_ui_model import MenuItem, MenuModel, Rect, SelectionIntent


class MenuModelTests(unittest.TestCase):
    def setUp(self):
        self.menu = MenuModel([
            MenuItem("ios18", "Boot iOS 18", enabled=False),
            MenuItem("android", "Boot Original Android", enabled=False),
        ])
        self.menu.set_hit_regions({
            "ios18": Rect(20, 100, 280, 64),
            "android": Rect(20, 190, 280, 64),
        })

    def test_both_conceptual_entries_disabled_by_default(self):
        self.assertFalse(self.menu.has_enabled_items)
        self.assertIsNone(self.menu.focused_item)
        self.assertIsNone(self.menu.activate_focused())

    def test_navigation_skips_disabled_entries(self):
        menu = MenuModel([
            MenuItem("a", "A", True),
            MenuItem("b", "B", False),
            MenuItem("c", "C", True),
        ])
        self.assertEqual(menu.focused_item, "a")
        self.assertEqual(menu.navigate("next"), "c")
        self.assertEqual(menu.navigate("next"), "a")
        self.assertEqual(menu.navigate("previous"), "c")

    def test_navigation_without_enabled_items_is_noop(self):
        self.assertIsNone(self.menu.navigate("next"))

    def test_invalid_navigation_direction_rejected(self):
        with self.assertRaises(ValueError):
            self.menu.navigate("sideways")

    def test_touch_on_disabled_item_does_not_select(self):
        self.menu.touch_down(40, 120)
        self.assertIsNone(self.menu.touch_up(40, 120))

    def test_enabled_touch_tap_returns_selection_intent(self):
        menu = MenuModel([MenuItem("demo", "Demo", True)])
        menu.set_hit_regions({"demo": Rect(10, 10, 100, 50)})
        menu.touch_down(20, 20)
        self.assertEqual(menu.touch_up(20, 20), SelectionIntent("demo"))

    def test_touch_moving_outside_cancels_activation(self):
        menu = MenuModel([MenuItem("demo", "Demo", True)])
        menu.set_hit_regions({"demo": Rect(10, 10, 100, 50)})
        menu.touch_down(20, 20)
        menu.touch_move(200, 200)
        self.assertIsNone(menu.touch_up(20, 20))

    def test_touch_up_outside_does_not_activate(self):
        menu = MenuModel([MenuItem("demo", "Demo", True)])
        menu.set_hit_regions({"demo": Rect(10, 10, 100, 50)})
        menu.touch_down(20, 20)
        self.assertIsNone(menu.touch_up(200, 200))

    def test_touch_cancel_clears_pending_selection(self):
        menu = MenuModel([MenuItem("demo", "Demo", True)])
        menu.set_hit_regions({"demo": Rect(10, 10, 100, 50)})
        menu.touch_down(20, 20)
        menu.touch_cancel()
        self.assertIsNone(menu.touch_up(20, 20))

    def test_unknown_hit_region_rejected(self):
        with self.assertRaises(ValueError):
            self.menu.set_hit_regions({"not-a-menu-item": Rect(0, 0, 1, 1)})

    def test_duplicate_item_ids_rejected(self):
        with self.assertRaises(ValueError):
            MenuModel([MenuItem("same", "One"), MenuItem("same", "Two")])

    def test_selection_intent_is_not_an_execution_action(self):
        menu = MenuModel([MenuItem("ios18", "Boot iOS 18", True)])
        self.assertEqual(menu.activate_focused(), SelectionIntent("ios18"))
        self.assertFalse(hasattr(menu, "boot"))
        self.assertFalse(hasattr(menu, "execute"))


if __name__ == "__main__":
    unittest.main()
