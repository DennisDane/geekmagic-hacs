"""Gauge widget for GeekMagic displays."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..const import COLOR_CYAN, COLOR_DARK_GRAY, COLOR_GRAY, COLOR_WHITE
from .base import Widget, WidgetConfig
from .helpers import (
    calculate_percent,
    extract_numeric,
    format_value_with_unit,
    get_unit,
    resolve_label,
)
from .layout_helpers import layout_bar_with_label

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from ..render_context import RenderContext


class GaugeWidget(Widget):
    """Widget that displays a value as a gauge (bar or ring)."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the gauge widget."""
        super().__init__(config)
        self.style = config.options.get("style", "bar")  # bar, ring, arc
        self.min_value = config.options.get("min", 0)
        self.max_value = config.options.get("max", 100)
        self.icon = config.options.get("icon")
        self.show_value = config.options.get("show_value", True)
        self.unit = config.options.get("unit", "")
        # Attribute to read value from (e.g., "temperature" for climate entities)
        self.attribute = config.options.get("attribute")

    def render(
        self,
        ctx: RenderContext,
        hass: HomeAssistant | None = None,
    ) -> None:
        """Render the gauge widget.

        Args:
            ctx: RenderContext for drawing
            hass: Home Assistant instance
        """
        # Get entity state
        state = self.get_entity_state(hass)

        # Extract numeric value and display string
        value = extract_numeric(state, self.attribute)
        display_value = f"{value:.0f}" if state is not None else "--"

        # Get unit from state if not configured
        if not self.unit and state is not None:
            self.unit = get_unit(state)

        # Calculate percentage using helper
        percent = calculate_percent(value, self.min_value, self.max_value)

        # Get label using helper
        name = resolve_label(self.config, state)

        color = self.config.color or COLOR_CYAN

        if self.style == "ring":
            self._render_ring(ctx, percent, display_value, name, color)
        elif self.style == "arc":
            self._render_arc(ctx, percent, display_value, name, color)
        else:
            self._render_bar(ctx, percent, display_value, name, color)

    def _render_bar(
        self,
        ctx: RenderContext,
        percent: float,
        value: str,
        name: str,
        color: tuple[int, int, int],
    ) -> None:
        """Render as horizontal progress bar."""
        value_text = format_value_with_unit(value, self.unit) if self.show_value else ""
        layout_bar_with_label(
            ctx,
            percent=percent,
            label=name,
            value=value_text,
            color=color,
            background=COLOR_DARK_GRAY,
            icon=self.icon,
        )

    def _render_ring(
        self,
        ctx: RenderContext,
        percent: float,
        value: str,
        name: str,
        color: tuple[int, int, int],
    ) -> None:
        """Render as ring gauge."""
        center_x = ctx.width // 2
        center_y = ctx.height // 2

        # Get scaled fonts
        font_value = ctx.get_font("large")
        font_label = ctx.get_font("tiny")

        # Calculate ring size relative to container
        margin = int(min(ctx.width, ctx.height) * 0.12)
        radius = min(ctx.width, ctx.height) // 2 - margin
        ring_width = max(4, radius // 5)

        # Draw ring
        ctx.draw_ring_gauge(
            center=(center_x, center_y - int(ctx.height * 0.04)),
            radius=radius,
            percent=percent,
            color=color,
            background=COLOR_DARK_GRAY,
            width=ring_width,
        )

        # Draw value in center
        if self.show_value:
            ctx.draw_text(
                format_value_with_unit(value, self.unit),
                (center_x, center_y - int(ctx.height * 0.04)),
                font=font_value,
                color=COLOR_WHITE,
                anchor="mm",
            )

        # Draw label below
        if name:
            ctx.draw_text(
                name.upper(),
                (center_x, ctx.height - int(ctx.height * 0.10)),
                font=font_label,
                color=COLOR_GRAY,
                anchor="mm",
            )

    def _render_arc(
        self,
        ctx: RenderContext,
        percent: float,
        value: str,
        name: str,
        color: tuple[int, int, int],
    ) -> None:
        """Render as arc gauge (semicircle)."""
        center_x = ctx.width // 2
        center_y = int(ctx.height * 0.55)

        # Get scaled fonts
        font_value = ctx.get_font("large")
        font_label = ctx.get_font("small")

        # Calculate arc size relative to container
        margin = int(min(ctx.width, ctx.height) * 0.08)
        radius = min(ctx.width, ctx.height) // 2 - margin

        # Draw arc using renderer's draw_arc method
        ctx.draw_arc(
            rect=(center_x - radius, center_y - radius, center_x + radius, center_y + radius),
            percent=percent,
            color=color,
            background=COLOR_DARK_GRAY,
        )

        # Draw value
        if self.show_value:
            ctx.draw_text(
                format_value_with_unit(value, self.unit),
                (center_x, center_y - int(ctx.height * 0.04)),
                font=font_value,
                color=COLOR_WHITE,
                anchor="mm",
            )

        # Draw label
        if name:
            ctx.draw_text(
                name.upper(),
                (center_x, int(ctx.height * 0.12)),
                font=font_label,
                color=COLOR_GRAY,
                anchor="mm",
            )
