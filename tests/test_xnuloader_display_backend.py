import unittest

from tools.xnuloader_display_backend import (
    CommandKind,
    DisplayCommand,
    DisplayFrame,
    DisplayServiceReport,
    PresentStatus,
    ServiceState,
    TransferMethod,
    validate_presentation,
)
from tools.xnuloader_display_layout import DisplayMode, Rect


MODE = DisplayMode(480, 800, 512, "PixelBlueGreenRedReserved8BitPerColor")
AVAILABLE = DisplayServiceReport(
    ServiceState.AVAILABLE, MODE, (TransferMethod.GOP_BLT,)
)


class DisplayServiceReportTests(unittest.TestCase):
    def test_valid_available_report(self):
        AVAILABLE.validate()

    def test_available_requires_mode_and_transfer(self):
        with self.assertRaises(ValueError):
            DisplayServiceReport(ServiceState.AVAILABLE).validate()
        with self.assertRaises(ValueError):
            DisplayServiceReport(ServiceState.AVAILABLE, MODE).validate()

    def test_unavailable_cannot_claim_mode(self):
        with self.assertRaises(ValueError):
            DisplayServiceReport(ServiceState.UNAVAILABLE, MODE).validate()

    def test_error_requires_code(self):
        with self.assertRaises(ValueError):
            DisplayServiceReport(ServiceState.ERROR).validate()
        DisplayServiceReport(ServiceState.ERROR, error_code="query_failed").validate()

    def test_not_checked_has_no_capabilities(self):
        DisplayServiceReport(ServiceState.NOT_CHECKED).validate()


class DisplayFrameTests(unittest.TestCase):
    def test_valid_logical_frame(self):
        frame = DisplayFrame((
            DisplayCommand(CommandKind.CLEAR),
            DisplayCommand(CommandKind.FILL_RECT, Rect(10, 10, 100, 40)),
            DisplayCommand(CommandKind.TEXT, Rect(20, 20, 180, 30), "XNULoader"),
        ))
        validate_presentation(AVAILABLE, frame)

    def test_rejects_out_of_bounds_rectangle(self):
        frame = DisplayFrame((
            DisplayCommand(CommandKind.FILL_RECT, Rect(470, 10, 20, 20)),
        ))
        with self.assertRaises(ValueError):
            validate_presentation(AVAILABLE, frame)

    def test_rejects_empty_text(self):
        frame = DisplayFrame((
            DisplayCommand(CommandKind.TEXT, Rect(0, 0, 100, 20), "  "),
        ))
        with self.assertRaises(ValueError):
            validate_presentation(AVAILABLE, frame)

    def test_rejects_malformed_clear(self):
        frame = DisplayFrame((
            DisplayCommand(CommandKind.CLEAR, Rect(0, 0, 10, 10)),
        ))
        with self.assertRaises(ValueError):
            validate_presentation(AVAILABLE, frame)

    def test_rejects_frame_without_available_service(self):
        frame = DisplayFrame((DisplayCommand(CommandKind.CLEAR),))
        for state in (ServiceState.NOT_CHECKED, ServiceState.UNAVAILABLE, ServiceState.ERROR):
            report = DisplayServiceReport(
                state, error_code="query_failed" if state is ServiceState.ERROR else None
            )
            with self.subTest(state=state), self.assertRaises(ValueError):
                validate_presentation(report, frame)

    def test_rejects_empty_frame(self):
        with self.assertRaises(ValueError):
            validate_presentation(AVAILABLE, DisplayFrame(()))

    def test_present_status_is_explicit(self):
        self.assertEqual(PresentStatus.ACCEPTED.value, "accepted")
        self.assertEqual(PresentStatus.FAILED.value, "failed")


if __name__ == "__main__":
    unittest.main()
