import unittest

from tools.xnuloader_touch_model import TouchEventModel, TouchRange, TouchSample


class TouchRangeTests(unittest.TestCase):
    def test_accepts_valid_range(self):
        TouchRange(0, 100, 0, 200)

    def test_rejects_empty_or_reversed_axis(self):
        with self.assertRaises(ValueError):
            TouchRange(10, 10, 0, 200)
        with self.assertRaises(ValueError):
            TouchRange(0, 100, 20, 10)

    def test_rejects_boolean_bounds(self):
        with self.assertRaises(ValueError):
            TouchRange(False, 100, 0, 200)


class TouchEventModelTests(unittest.TestCase):
    def setUp(self):
        self.model = TouchEventModel(TouchRange(0, 100, 0, 200))

    def test_contact_lifecycle_down_move_up(self):
        self.assertEqual(self.model.process(TouchSample(True, 10, 20)), 
                         __import__("tools.xnuloader_touch_model", fromlist=["TouchEvent"]).TouchEvent("down", 10, 20))
        self.assertEqual(self.model.process(TouchSample(True, 15, 25)).kind, "move")
        self.assertEqual(self.model.process(TouchSample(False)).kind, "up")
        self.assertFalse(self.model.contact_active)

    def test_idle_release_emits_nothing(self):
        self.assertIsNone(self.model.process(TouchSample(False)))

    def test_failed_read_cancels_active_contact(self):
        self.model.process(TouchSample(True, 10, 20))
        event = self.model.process(TouchSample(False, failed=True))
        self.assertEqual((event.kind, event.x, event.y), ("cancel", 10, 20))
        self.assertFalse(self.model.contact_active)

    def test_failure_while_idle_emits_nothing(self):
        self.assertIsNone(self.model.process(TouchSample(False, failed=True)))

    def test_out_of_range_active_sample_cancels(self):
        self.model.process(TouchSample(True, 10, 20))
        event = self.model.process(TouchSample(True, 101, 20))
        self.assertEqual(event.kind, "cancel")
        self.assertFalse(self.model.contact_active)

    def test_invalid_initial_contact_is_rejected(self):
        with self.assertRaises(ValueError):
            self.model.process(TouchSample(True, 101, 20))

    def test_missing_coordinates_are_rejected_for_contact(self):
        with self.assertRaises(ValueError):
            self.model.process(TouchSample(True))

    def test_boolean_coordinates_are_rejected(self):
        with self.assertRaises(ValueError):
            self.model.process(TouchSample(True, True, 20))

    def test_recovery_after_cancel_starts_new_contact(self):
        self.model.process(TouchSample(True, 10, 20))
        self.model.process(TouchSample(False, failed=True))
        event = self.model.process(TouchSample(True, 30, 40))
        self.assertEqual((event.kind, event.x, event.y), ("down", 30, 40))

    def test_contact_sample_after_release_starts_new_contact(self):
        self.model.process(TouchSample(True, 10, 20))
        self.model.process(TouchSample(False))
        event = self.model.process(TouchSample(True, 11, 21))
        self.assertEqual(event.kind, "down")

    def test_non_sample_input_is_rejected(self):
        with self.assertRaises(TypeError):
            self.model.process({"contact": True, "x": 1, "y": 2})

    def test_non_boolean_flags_are_rejected(self):
        with self.assertRaises(ValueError):
            self.model.process(TouchSample(1, 10, 20))


if __name__ == "__main__":
    unittest.main()
