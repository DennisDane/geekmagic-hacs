"""Template helpers for widget option resolution."""

from __future__ import annotations

import logging
import math
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.template import Template, TemplateError

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


def _parse_float(value: Any) -> float | None:
    """Parse a float value, returning None on invalid input."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _render_template(hass: HomeAssistant, template: Any, *, label: str = "") -> str | None:
    """Render a Home Assistant Jinja template to a raw string."""
    if not isinstance(template, str):
        return None

    source = template.strip()
    if not source:
        return None

    try:
        rendered = Template(source, hass).render(parse_result=False)
    except TemplateError as err:
        if label:
            _LOGGER.debug("Failed to render template for %s: %s", label, err)
        else:
            _LOGGER.debug("Failed to render template: %s", err)
        return None
    except Exception as err:  # pragma: no cover - defensive guard
        if label:
            _LOGGER.debug("Unexpected template render error for %s: %s", label, err)
        else:
            _LOGGER.debug("Unexpected template render error: %s", err)
        return None

    return str(rendered)


def render_string_template(hass: HomeAssistant, template: Any, *, label: str = "") -> str | None:
    """Render a Home Assistant Jinja template and return a string."""
    return _render_template(hass, template, label=label)


def render_numeric_template(hass: HomeAssistant, template: Any, *, label: str = "") -> float | None:
    """Render a Home Assistant Jinja template and coerce to finite float."""
    rendered = _render_template(hass, template, label=label)
    if rendered is None:
        return None

    parsed = _parse_float(rendered)
    if parsed is None:
        if label:
            _LOGGER.debug("Template for %s did not resolve to a number: %s", label, rendered)
        else:
            _LOGGER.debug("Template did not resolve to a number: %s", rendered)
        return None

    if not math.isfinite(parsed):
        if label:
            _LOGGER.debug("Template for %s resolved to non-finite value: %s", label, rendered)
        else:
            _LOGGER.debug("Template resolved to non-finite value: %s", rendered)
        return None

    return parsed


def _resolve_multi_progress_items(
    hass: HomeAssistant, options: dict[str, Any]
) -> list[dict[str, Any]] | None:
    """Resolve template-backed multi-progress item fields."""
    items = options.get("items")
    if not isinstance(items, list):
        return None

    resolved_items: list[dict[str, Any]] = []
    any_resolved = False

    for idx, item in enumerate(items):
        item_options = item if isinstance(item, dict) else {}
        resolved_item: dict[str, Any] = {}

        label_value = render_string_template(
            hass,
            item_options.get("label_template"),
            label=f"multi_progress.items[{idx}].label_template",
        )
        if label_value is not None:
            resolved_item["label"] = label_value
            any_resolved = True

        target_value = render_numeric_template(
            hass,
            item_options.get("target_template"),
            label=f"multi_progress.items[{idx}].target_template",
        )
        if target_value is not None:
            resolved_item["target"] = target_value
            any_resolved = True

        resolved_items.append(resolved_item)

    if not any_resolved:
        return None
    return resolved_items


def resolve_widget_template_options(
    hass: HomeAssistant,
    widget_type: str,
    options: dict[str, Any],
) -> dict[str, Any]:
    """Resolve template-backed widget options."""
    resolved: dict[str, Any] = {}

    if widget_type == "gauge":
        min_value = render_numeric_template(
            hass,
            options.get("min_template"),
            label="gauge.min_template",
        )
        if min_value is not None:
            resolved["min"] = min_value

        max_value = render_numeric_template(
            hass,
            options.get("max_template"),
            label="gauge.max_template",
        )
        if max_value is not None:
            resolved["max"] = max_value

    elif widget_type == "text":
        text_value = render_string_template(
            hass,
            options.get("text_template"),
            label="text.text_template",
        )
        if text_value is not None:
            resolved["text"] = text_value

    elif widget_type == "progress":
        target_value = render_numeric_template(
            hass,
            options.get("target_template"),
            label="progress.target_template",
        )
        if target_value is not None:
            resolved["target"] = target_value

    elif widget_type == "multi_progress":
        title_value = render_string_template(
            hass,
            options.get("title_template"),
            label="multi_progress.title_template",
        )
        if title_value is not None:
            resolved["title"] = title_value

        item_values = _resolve_multi_progress_items(hass, options)
        if item_values is not None:
            resolved["items"] = item_values

    elif widget_type == "status":
        on_text_value = render_string_template(
            hass,
            options.get("on_text_template"),
            label="status.on_text_template",
        )
        if on_text_value is not None:
            resolved["on_text"] = on_text_value

        off_text_value = render_string_template(
            hass,
            options.get("off_text_template"),
            label="status.off_text_template",
        )
        if off_text_value is not None:
            resolved["off_text"] = off_text_value

    elif widget_type == "status_list":
        title_value = render_string_template(
            hass,
            options.get("title_template"),
            label="status_list.title_template",
        )
        if title_value is not None:
            resolved["title"] = title_value

    return resolved
