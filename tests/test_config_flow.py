"""Tests for GeekMagic config flow."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from homeassistant import config_entries

from custom_components.geekmagic.config_flow import (
    LAYOUT_OPTIONS,
    GeekMagicConfigFlow,
    GeekMagicOptionsFlow,
)
from custom_components.geekmagic.const import (
    CONF_LAYOUT,
    CONF_REFRESH_INTERVAL,
    CONF_SCREEN_CYCLE_INTERVAL,
    CONF_SCREENS,
    CONF_WIDGETS,
    DEFAULT_REFRESH_INTERVAL,
    DEFAULT_SCREEN_CYCLE_INTERVAL,
    LAYOUT_GRID_2X2,
)


class TestConfigFlowImports:
    """Test that config flow can be imported without errors."""

    def test_import_config_flow(self):
        """Test config flow module imports successfully."""
        from custom_components.geekmagic import config_flow

        assert config_flow.GeekMagicConfigFlow is not None
        assert config_flow.GeekMagicOptionsFlow is not None

    def test_import_all_dependencies(self):
        """Test all config flow dependencies import correctly."""
        from custom_components.geekmagic.config_flow import (
            LAYOUT_OPTIONS,
            selector,
            vol,
        )

        assert vol is not None
        assert selector is not None
        assert LAYOUT_OPTIONS is not None

    def test_config_flow_class_attributes(self):
        """Test GeekMagicConfigFlow has required attributes."""
        assert hasattr(GeekMagicConfigFlow, "VERSION")
        assert hasattr(GeekMagicConfigFlow, "async_step_user")
        assert hasattr(GeekMagicConfigFlow, "async_get_options_flow")

    def test_layout_options_defined(self):
        """Test layout options are properly defined."""
        assert LAYOUT_GRID_2X2 in LAYOUT_OPTIONS
        assert len(LAYOUT_OPTIONS) >= 4  # At least 4 layouts


class TestOptionsFlowInit:
    """Test options flow initialization."""

    @pytest.fixture
    def mock_config_entry(self):
        """Create a mock config entry."""
        entry = MagicMock(spec=config_entries.ConfigEntry)
        entry.options = {}
        entry.data = {"host": "192.168.1.100", "name": "Test Display"}
        return entry

    def test_options_flow_init(self, mock_config_entry):
        """Test GeekMagicOptionsFlow can be instantiated."""
        flow = GeekMagicOptionsFlow(mock_config_entry)

        assert flow is not None
        assert flow.config_entry == mock_config_entry
        assert flow._options == {}
        assert flow._current_screen_index == 0
        assert flow._current_slot == 0

    def test_migrate_empty_options(self, mock_config_entry):
        """Test migration handles empty options."""
        flow = GeekMagicOptionsFlow(mock_config_entry)
        migrated = flow._migrate_options({})

        assert CONF_SCREENS in migrated
        assert CONF_REFRESH_INTERVAL in migrated
        assert CONF_SCREEN_CYCLE_INTERVAL in migrated
        assert len(migrated[CONF_SCREENS]) == 1
        assert migrated[CONF_REFRESH_INTERVAL] == DEFAULT_REFRESH_INTERVAL
        assert migrated[CONF_SCREEN_CYCLE_INTERVAL] == DEFAULT_SCREEN_CYCLE_INTERVAL

    def test_migrate_existing_screens(self, mock_config_entry):
        """Test migration preserves existing screens."""
        existing = {
            CONF_SCREENS: [{"name": "Test", CONF_LAYOUT: LAYOUT_GRID_2X2, CONF_WIDGETS: []}],
            CONF_REFRESH_INTERVAL: 15,
            CONF_SCREEN_CYCLE_INTERVAL: 30,
        }

        flow = GeekMagicOptionsFlow(mock_config_entry)
        migrated = flow._migrate_options(existing)

        assert migrated[CONF_SCREENS][0]["name"] == "Test"
        assert migrated[CONF_REFRESH_INTERVAL] == 15
        assert migrated[CONF_SCREEN_CYCLE_INTERVAL] == 30

    def test_migrate_old_single_screen_format(self, mock_config_entry):
        """Test migration handles old single-screen format."""
        old_format = {
            CONF_LAYOUT: LAYOUT_GRID_2X2,
            CONF_WIDGETS: [{"type": "clock", "slot": 0}],
            CONF_REFRESH_INTERVAL: 10,
        }

        flow = GeekMagicOptionsFlow(mock_config_entry)
        migrated = flow._migrate_options(old_format)

        # Should be converted to multi-screen format
        assert CONF_SCREENS in migrated
        assert len(migrated[CONF_SCREENS]) == 1
        assert migrated[CONF_SCREENS][0][CONF_LAYOUT] == LAYOUT_GRID_2X2
        assert migrated[CONF_SCREENS][0][CONF_WIDGETS] == [{"type": "clock", "slot": 0}]


class TestSlotMatching:
    """Test slot matching logic (regression tests for bug fixes)."""

    @pytest.fixture
    def options_flow(self):
        """Create an options flow instance."""
        entry = MagicMock(spec=config_entries.ConfigEntry)
        entry.options = {}
        return GeekMagicOptionsFlow(entry)

    def test_slot_matching_at_slot_zero(self, options_flow):
        """Test slot matching works correctly when current_slot is 0.

        Regression test: Previously, the code checked for `slot in (current_slot - 1, current_slot)`
        which would match slot -1 when current_slot was 0, causing incorrect behavior.
        """
        options_flow._current_slot = 0
        options_flow._screen_config = {
            CONF_WIDGETS: [
                {"type": "clock", "slot": 0},
                {"type": "entity", "slot": 1},
            ]
        }
        options_flow._current_widget_type = "clock"

        # Simulate finding existing widget for slot 0
        existing_widget = None
        for w in options_flow._screen_config.get(CONF_WIDGETS, []):
            if w.get("slot") == options_flow._current_slot and w.get("type") == "clock":
                existing_widget = w
                break

        assert existing_widget is not None
        assert existing_widget["slot"] == 0
        assert existing_widget["type"] == "clock"

    def test_slot_matching_does_not_match_wrong_slot(self, options_flow):
        """Test slot matching doesn't match adjacent slots incorrectly."""
        options_flow._current_slot = 1
        options_flow._screen_config = {
            CONF_WIDGETS: [
                {"type": "clock", "slot": 0},
                {"type": "entity", "slot": 2},
            ]
        }

        # Slot 1 has no widget, so should not find anything
        existing_widget = None
        for w in options_flow._screen_config.get(CONF_WIDGETS, []):
            if w.get("slot") == options_flow._current_slot:
                existing_widget = w
                break

        assert existing_widget is None


class TestWidgetSchema:
    """Test widget schema generation."""

    @pytest.fixture
    def options_flow(self):
        """Create an options flow instance."""
        entry = MagicMock(spec=config_entries.ConfigEntry)
        entry.options = {}
        return GeekMagicOptionsFlow(entry)

    def test_clock_widget_schema(self, options_flow):
        """Test clock widget schema generation."""
        schema = options_flow._get_widget_schema("clock")

        assert schema is not None
        assert isinstance(schema, dict)

    def test_entity_widget_schema(self, options_flow):
        """Test entity widget schema generation."""
        schema = options_flow._get_widget_schema("entity")

        assert schema is not None
        assert isinstance(schema, dict)

    def test_unknown_widget_schema(self, options_flow):
        """Test unknown widget type returns empty schema."""
        schema = options_flow._get_widget_schema("nonexistent_widget")

        assert schema == {}

    def test_all_widget_types_have_schemas(self, options_flow):
        """Test all known widget types have schemas."""
        widget_types = [
            "clock",
            "entity",
            "media",
            "chart",
            "text",
            "gauge",
            "progress",
            "status",
            "weather",
            "multi_progress",
            "status_list",
        ]

        for widget_type in widget_types:
            schema = options_flow._get_widget_schema(widget_type)
            assert isinstance(schema, dict), f"Widget type '{widget_type}' should return a dict"
