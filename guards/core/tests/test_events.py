from guards.core.events import GuardEventKey

TEST_ID_1 = "TEST_EVENT_1"
TEST_ID_2 = "TEST_EVENT_2"


class TestGuardEvent:
    def test_guard_event_equals_for_same_id_and_type(self):
        event_1 = GuardEventKey(TEST_ID_1)
        event_2 = GuardEventKey(TEST_ID_1)
        assert event_1 == event_2

    def test_guard_event_does_not_equal_for_different_id_and_same_type(self):
        event_1 = GuardEventKey(TEST_ID_1)
        event_2 = GuardEventKey(TEST_ID_2)
        assert event_1 != event_2

    def test_guard_event_equals_for_same_id_and_same_subtype(self):
        class SubEventKey(GuardEventKey):
            pass

        event_1 = SubEventKey(TEST_ID_1)
        event_2 = SubEventKey(TEST_ID_1)
        assert event_1 == event_2

    def test_guard_event_does_not_equal_for_same_id_and_different_type(self):
        class SubEventKey(GuardEventKey):
            pass

        event_1 = GuardEventKey(TEST_ID_1)
        event_2 = SubEventKey(TEST_ID_1)
        assert event_1 != event_2

    def test_guard_event_str(self):
        class SubEventKey(GuardEventKey):
            pass

        event_1 = GuardEventKey(TEST_ID_1)
        event_2 = SubEventKey(TEST_ID_1)
        assert event_1 != event_2
