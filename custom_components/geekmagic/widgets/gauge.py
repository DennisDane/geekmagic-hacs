"""Gauge widget for GeekMagic displays."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..const import COLOR_DARK_GRAY
from .base import Widget, WidgetConfig
from .component_helpers import ArcGauge, BarGauge, RingGauge
from .components import Component
from .helpers import calculate_percent, format_value_with_unit

if TYPE_CHECKING:
    from ..render_context import RenderContext
    from .state import EntityState, WidgetState


def _parse_float(value: object) -> float | None:
    """Parse a numeric value, returning None on failure."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _coerce_float(value: object, default: float) -> float:
    """Coerce a value to float with fallback default."""
    parsed = _parse_float(value)
    if parsed is None:
        return default
    return parsed


def _coerce_precision(value: object, default: int = 2) -> int:
    """Coerce precision to an integer in [0, 6]."""
    try:
        precision = int(value)
    except (ValueError, TypeError):
        precision = default
    return max(0, min(6, precision))


def _extract_numeric(entity: EntityState | None, attribute: str | None = None) -> float:
    """Extract numeric value from entity state."""
    if entity is None:
        return 0.0
    value = entity.get(attribute) if attribute else entity.state
    parsed = _parse_float(value)
    if parsed is None:
        return 0.0
    return parsed


def _resolve_label(config: WidgetConfig, entity: EntityState | None) -> str:
    """Get label from config or entity friendly_name."""
    if config.label:
        return config.label
    if entity:
        return entity.friendly_name
    return ""


class GaugeWidget(Widget):
    """Widget that displays a value as a gauge (bar or ring)."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the gauge widget."""
        super().__init__(config)
        self.style = config.options.get("style", "bar")  # bar, ring, arc
        self.min_value = _coerce_float(config.options.get("min", 0), 0.0)
        self.max_value = _coerce_float(config.options.get("max", 100), 100.0)
        self.min_entity = config.options.get("min_entity")
        self.max_entity = config.options.get("max_entity")
        self.icon = config.options.get("icon")
        self.show_value = config.options.get("show_value", True)
        legacy_decimal_places = config.options.get("decimal_places")
        precision_raw = (
            config.options.get("precision")
            if config.options.get("precision") is not None
            else legacy_decimal_places
        )
        self.precision = _coerce_precision(precision_raw, default=2)
        # Backward-compatible alias used by tests/configs.
        self.decimal_places = self.precision
        self.unit = config.options.get("unit", "")
        # Attribute to read value from
        self.attribute = config.options.get("attribute")
        # Color thresholds
        self.color_thresholds = config.options.get("color_thresholds", [])

    def get_entities(self) -> list[str]:
        """Return list of entity IDs this widget depends on."""
        entities = super().get_entities()
        for entity_id in (self.min_entity, self.max_entity):
            if entity_id and entity_id not in entities:
                entities.append(entity_id)
        return entities

    def _resolve_bound(
        self,
        state: WidgetState,
        key: str,
        entity_id: str | None,
        fallback: float,
    ) -> float:
        """Resolve bound from template result/entity with static fallback."""
        resolved_template_value = _parse_float(state.get_resolved_option(key))
        if resolved_template_value is not None:
            return resolved_template_value

        if not entity_id:
            return fallback
        entity = state.get_entity(entity_id)
        if entity is None:
            return fallback
        parsed = _parse_float(entity.state)
        if parsed is None:
            return fallback
        return parsed

    def _get_threshold_color(self, value: float) -> tuple[int, int, int] | None:
        """Get color based on value and thresholds."""
        if not self.color_thresholds:
            return None

        sorted_thresholds = sorted(
            self.color_thresholds,
            key=lambda t: _coerce_float(t.get("value", 0), 0.0),
        )
        matching_color = None
        for threshold in sorted_thresholds:
            threshold_value = _coerce_float(threshold.get("value", 0), 0.0)
            threshold_color = threshold.get("color")
            if value >= threshold_value and threshold_color:
                matching_color = tuple(threshold_color)

        return matching_color  # type: ignore[return-value]

    def render(self, ctx: RenderContext, state: WidgetState) -> Component:
        """Render the gauge widget.

        Args:
            ctx: RenderContext for drawing
            state: Widget state with entity data

        Returns:
            Component tree for rendering
        """
        entity = state.entity

        # Extract numeric value
        value = _extract_numeric(entity, self.attribute)
        decimal_format = f"{{:.{self.precision}f}}"
        display_value = decimal_format.format(value) if entity is not None else "--"

        # Get unit from entity if not configured
        unit = self.unit
        if not unit and entity is not None:
            unit = entity.unit or ""

        # Calculate percentage
        min_value = self._resolve_bound(
            state,
            "min",
            self.min_entity,
            self.min_value,
        )
        max_value = self._resolve_bound(
            state,
            "max",
            self.max_entity,
            self.max_value,
        )
        percent = calculate_percent(value, min_value, max_value)

        # Get label
        name = _resolve_label(self.config, entity)

        # Determine color
        threshold_color = self._get_threshold_color(value)
        color = threshold_color or self.config.color or ctx.theme.get_accent_color(self.config.slot)

        # Format value with unit
        value_text = format_value_with_unit(display_value, unit) if self.show_value else ""

        if self.style == "ring":
            return RingGauge(
                percent=percent,
                value=value_text,
                label=name,
                color=color,
                background=COLOR_DARK_GRAY,
            )
        if self.style == "arc":
            return ArcGauge(
                percent=percent,
                value=value_text,
                label=name,
                color=color,
                background=COLOR_DARK_GRAY,
            )
        return BarGauge(
            percent=percent,
            value=value_text,
            label=name,
            color=color,
            icon=self.icon,
            background=COLOR_DARK_GRAY,
        )
