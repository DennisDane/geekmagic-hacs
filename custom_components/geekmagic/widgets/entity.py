"""Entity widget for GeekMagic displays."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..const import (
    COLOR_CYAN,
    COLOR_PANEL,
    PLACEHOLDER_NAME,
    PLACEHOLDER_VALUE,
)
from .base import Widget, WidgetConfig
from .helpers import (
    estimate_max_chars,
    format_value_with_unit,
    get_unit,
    resolve_label,
    truncate_text,
)
from .layout_helpers import layout_centered_value, layout_icon_centered_value

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from ..render_context import RenderContext


class EntityWidget(Widget):
    """Widget that displays a Home Assistant entity state."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the entity widget."""
        super().__init__(config)
        self.show_name = config.options.get("show_name", True)
        self.show_unit = config.options.get("show_unit", True)
        self.icon = config.options.get("icon")
        self.show_panel = config.options.get("show_panel", False)

    def render(
        self,
        ctx: RenderContext,
        hass: HomeAssistant | None = None,
    ) -> None:
        """Render the entity widget.

        Args:
            ctx: RenderContext for drawing
            hass: Home Assistant instance
        """
        # Draw panel background if enabled
        if self.show_panel:
            ctx.draw_panel((0, 0, ctx.width, ctx.height), COLOR_PANEL, radius=4)

        # Get entity state
        state = self.get_entity_state(hass)

        if state is None:
            value = PLACEHOLDER_VALUE
            unit = ""
            name = self.config.label or self.config.entity_id or PLACEHOLDER_NAME
        else:
            value = state.state
            unit = get_unit(state) if self.show_unit else ""
            name = resolve_label(self.config, state, state.entity_id)

        # Truncate value and name using consistent helpers
        max_value_chars = estimate_max_chars(ctx.width, char_width=10, padding=10)
        max_name_chars = estimate_max_chars(ctx.width, char_width=7, padding=5)
        value = truncate_text(value, max_value_chars)
        name = truncate_text(name, max_name_chars)

        color = self.config.color or COLOR_CYAN

        # Layout depends on whether we have an icon
        if self.icon:
            self._render_with_icon(ctx, value, unit, name, color)
        else:
            self._render_centered(ctx, value, unit, name, color)

    def _render_centered(
        self,
        ctx: RenderContext,
        value: str,
        unit: str,
        name: str,
        color: tuple[int, int, int],
    ) -> None:
        """Render with value centered and name below."""
        value_text = format_value_with_unit(value, unit)
        layout_centered_value(
            ctx,
            value=value_text,
            label=name if self.show_name else None,
            color=color,
            show_label=self.show_name,
        )

    def _render_with_icon(
        self,
        ctx: RenderContext,
        value: str,
        unit: str,
        name: str,
        color: tuple[int, int, int],
    ) -> None:
        """Render with icon on top, value below, name at bottom."""
        assert self.icon is not None
        value_text = format_value_with_unit(value, unit)
        layout_icon_centered_value(
            ctx,
            icon=self.icon,
            value=value_text,
            label=name if self.show_name else None,
            color=color,
            show_label=self.show_name,
        )
