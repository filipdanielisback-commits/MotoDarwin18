import unittest

from drivers.core import (
    CapabilityState,
    DriverCapability,
    DriverDescriptor,
    DriverErrorCode,
    DriverRegistry,
    DriverState,
    DuplicateDriverError,
    InvalidDriverDescriptorError,
    InvalidDriverStateError,
    UnknownDriverError,
)


class FakeDriver:
    def __init__(self, driver_id="example.core", init_error=None, stop_error=None):
        self._descriptor = DriverDescriptor(
            driver_id=driver_id,
            name="Example driver",
            version="0.1.0",
            capabilities=(DriverCapability("metadata_only"),),
        )
        self.init_error = init_error
        self.stop_error = stop_error
        self.initialize_calls = 0
        self.shutdown_calls = 0

    @property
    def descriptor(self):
        return self._descriptor

    def initialize(self):
        self.initialize_calls += 1
        if self.init_error:
            raise self.init_error

    def shutdown(self):
        self.shutdown_calls += 1
        if self.stop_error:
            raise self.stop_error


class DriverDescriptorTests(unittest.TestCase):
    def test_registration_preserves_unknown_capability(self):
        registry = DriverRegistry()
        snapshot = registry.register(FakeDriver())
        self.assertEqual(snapshot.state, DriverState.REGISTERED)
        self.assertEqual(
            snapshot.descriptor.capabilities[0].state,
            CapabilityState.UNKNOWN,
        )

    def test_rejects_invalid_identifier(self):
        driver = FakeDriver(driver_id="Not Valid")
        with self.assertRaises(InvalidDriverDescriptorError):
            DriverRegistry().register(driver)

    def test_rejects_empty_name(self):
        driver = FakeDriver()
        driver._descriptor = DriverDescriptor("valid.id", " ", "1")
        with self.assertRaises(InvalidDriverDescriptorError):
            DriverRegistry().register(driver)

    def test_rejects_duplicate_capability_names(self):
        driver = FakeDriver()
        driver._descriptor = DriverDescriptor(
            "valid.id",
            "Valid",
            "1",
            (DriverCapability("display"), DriverCapability("display")),
        )
        with self.assertRaises(InvalidDriverDescriptorError):
            DriverRegistry().register(driver)

    def test_rejects_non_capability_metadata(self):
        driver = FakeDriver()
        driver._descriptor = DriverDescriptor(
            "valid.id", "Valid", "1", ("display",)
        )
        with self.assertRaises(InvalidDriverDescriptorError):
            DriverRegistry().register(driver)

    def test_rejects_available_capability_without_evidence(self):
        driver = FakeDriver()
        driver._descriptor = DriverDescriptor(
            "valid.id",
            "Valid",
            "1",
            (DriverCapability("display", CapabilityState.AVAILABLE),),
        )
        with self.assertRaises(InvalidDriverDescriptorError):
            DriverRegistry().register(driver)

    def test_accepts_evidence_backed_capability(self):
        driver = FakeDriver()
        driver._descriptor = DriverDescriptor(
            "valid.id",
            "Valid",
            "1",
            (DriverCapability(
                "display", CapabilityState.AVAILABLE, "docs/display-evidence.md"
            ),),
        )
        snapshot = DriverRegistry().register(driver)
        self.assertEqual(
            snapshot.descriptor.capabilities[0].state,
            CapabilityState.AVAILABLE,
        )

    def test_rejects_duplicate_driver_identifier(self):
        registry = DriverRegistry()
        registry.register(FakeDriver())
        with self.assertRaises(DuplicateDriverError):
            registry.register(FakeDriver())


class DriverRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = DriverRegistry()
        self.driver = FakeDriver()
        self.registry.register(self.driver)

    def test_initialize_transitions_to_ready(self):
        snapshot = self.registry.initialize("example.core")
        self.assertEqual(snapshot.state, DriverState.READY)
        self.assertEqual(self.driver.initialize_calls, 1)
        self.assertIsNone(snapshot.last_error)

    def test_shutdown_transitions_to_stopped(self):
        self.registry.initialize("example.core")
        snapshot = self.registry.shutdown("example.core")
        self.assertEqual(snapshot.state, DriverState.STOPPED)
        self.assertEqual(self.driver.shutdown_calls, 1)

    def test_stopped_driver_can_restart(self):
        self.registry.initialize("example.core")
        self.registry.shutdown("example.core")
        snapshot = self.registry.initialize("example.core")
        self.assertEqual(snapshot.state, DriverState.READY)
        self.assertEqual(self.driver.initialize_calls, 2)

    def test_initialization_failure_is_recorded(self):
        driver = FakeDriver(init_error=RuntimeError("controlled failure"))
        registry = DriverRegistry()
        registry.register(driver)
        snapshot = registry.initialize("example.core")
        self.assertEqual(snapshot.state, DriverState.FAILED)
        self.assertEqual(
            snapshot.last_error.code,
            DriverErrorCode.INITIALIZATION_FAILED,
        )
        self.assertIn("controlled failure", snapshot.last_error.message)

    def test_shutdown_failure_is_recorded(self):
        driver = FakeDriver(stop_error=RuntimeError("controlled failure"))
        registry = DriverRegistry()
        registry.register(driver)
        registry.initialize("example.core")
        snapshot = registry.shutdown("example.core")
        self.assertEqual(snapshot.state, DriverState.FAILED)
        self.assertEqual(
            snapshot.last_error.code,
            DriverErrorCode.SHUTDOWN_FAILED,
        )

    def test_cannot_shutdown_before_ready(self):
        with self.assertRaises(InvalidDriverStateError):
            self.registry.shutdown("example.core")

    def test_cannot_initialize_twice_without_shutdown(self):
        self.registry.initialize("example.core")
        with self.assertRaises(InvalidDriverStateError):
            self.registry.initialize("example.core")

    def test_active_driver_cannot_be_unregistered(self):
        self.registry.initialize("example.core")
        with self.assertRaises(InvalidDriverStateError):
            self.registry.unregister("example.core")

    def test_registered_driver_can_be_unregistered(self):
        snapshot = self.registry.unregister("example.core")
        self.assertEqual(snapshot.state, DriverState.REGISTERED)
        with self.assertRaises(UnknownDriverError):
            self.registry.get("example.core")

    def test_stopped_driver_can_be_unregistered(self):
        self.registry.initialize("example.core")
        self.registry.shutdown("example.core")
        self.registry.unregister("example.core")
        self.assertEqual(self.registry.list(), ())

    def test_unknown_driver_raises(self):
        with self.assertRaises(UnknownDriverError):
            self.registry.initialize("missing.driver")

    def test_list_is_sorted_by_identifier(self):
        self.registry.register(FakeDriver("zeta"))
        self.registry.register(FakeDriver("alpha"))
        ids = [item.descriptor.driver_id for item in self.registry.list()]
        self.assertEqual(ids, ["alpha", "example.core", "zeta"])


if __name__ == "__main__":
    unittest.main()
