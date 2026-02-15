"""Tests for template option helpers."""

from custom_components.geekmagic.template_utils import (
    render_numeric_template,
    render_string_template,
    resolve_widget_template_options,
)


class TestTemplateUtils:
    """Tests for template rendering and widget option resolution."""

    def test_render_string_template(self, hass):
        """Test valid string template rendering."""
        hass.states.async_set("sensor.foo", "hello")
        value = render_string_template(hass, "{{ states('sensor.foo') }}")
        assert value == "hello"

    def test_render_string_template_empty_string_is_valid(self, hass):
        """Test empty rendered strings are preserved as valid results."""
        value = render_string_template(hass, "{{ '' }}")
        assert value == ""

    def test_render_numeric_template(self, hass):
        """Test valid numeric template rendering."""
        hass.states.async_set("sensor.value", "12.5")
        value = render_numeric_template(hass, "{{ states('sensor.value') }}")
        assert value == 12.5

    def test_invalid_template_returns_none(self, hass):
        """Test invalid templates safely return None."""
        assert render_string_template(hass, "{{ states('sensor.foo' }}") is None
        assert render_numeric_template(hass, "{{ states('sensor.foo' }}") is None

    def test_numeric_template_rejects_non_numeric_and_non_finite(self, hass):
        """Test numeric templates reject invalid numeric values."""
        assert render_numeric_template(hass, "{{ 'not-a-number' }}") is None
        assert render_numeric_template(hass, "{{ 'nan' }}") is None
        assert render_numeric_template(hass, "{{ 'inf' }}") is None

    def test_resolve_widget_template_options_text(self, hass):
        """Test resolver shape for text widget templates."""
        hass.states.async_set("sensor.foo", "dynamic")
        resolved = resolve_widget_template_options(
            hass,
            "text",
            {"text_template": "{{ states('sensor.foo') }}"},
        )
        assert resolved == {"text": "dynamic"}

    def test_resolve_widget_template_options_progress(self, hass):
        """Test resolver shape for progress widget templates."""
        hass.states.async_set("sensor.goal", "42")
        resolved = resolve_widget_template_options(
            hass,
            "progress",
            {"target_template": "{{ states('sensor.goal') }}"},
        )
        assert resolved == {"target": 42.0}

    def test_resolve_widget_template_options_multi_progress(self, hass):
        """Test resolver shape for multi-progress template fields."""
        hass.states.async_set("sensor.title", "Fitness")
        hass.states.async_set("sensor.item_name", "Calories")
        hass.states.async_set("sensor.goal", "500")

        resolved = resolve_widget_template_options(
            hass,
            "multi_progress",
            {
                "title_template": "{{ states('sensor.title') }}",
                "items": [
                    {
                        "label_template": "{{ states('sensor.item_name') }}",
                        "target_template": "{{ states('sensor.goal') }}",
                    },
                    {"label": "No template"},
                ],
            },
        )

        assert resolved["title"] == "Fitness"
        assert isinstance(resolved.get("items"), list)
        assert resolved["items"][0] == {"label": "Calories", "target": 500.0}
        assert resolved["items"][1] == {}

    def test_resolve_widget_template_options_status(self, hass):
        """Test resolver shape for status widget templates."""
        resolved = resolve_widget_template_options(
            hass,
            "status",
            {
                "on_text_template": "{{ 'OPEN' }}",
                "off_text_template": "{{ 'CLOSED' }}",
            },
        )
        assert resolved == {"on_text": "OPEN", "off_text": "CLOSED"}

    def test_resolve_widget_template_options_status_list(self, hass):
        """Test resolver shape for status_list widget templates."""
        resolved = resolve_widget_template_options(
            hass,
            "status_list",
            {"title_template": "{{ 'Doors' }}"},
        )
        assert resolved == {"title": "Doors"}

    def test_resolve_widget_template_options_gauge_regression(self, hass):
        """Test gauge template resolution remains supported."""
        hass.states.async_set("sensor.min_bound", "10")
        hass.states.async_set("sensor.max_bound", "90")
        resolved = resolve_widget_template_options(
            hass,
            "gauge",
            {
                "min_template": "{{ states('sensor.min_bound') }}",
                "max_template": "{{ states('sensor.max_bound') }}",
            },
        )
        assert resolved == {"min": 10.0, "max": 90.0}
