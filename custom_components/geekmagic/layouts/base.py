"""Base layout class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..const import DISPLAY_HEIGHT, DISPLAY_WIDTH
from ..render_context import RenderContext

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from PIL import ImageDraw

    from ..renderer import Renderer
    from ..widgets.base import Widget


@dataclass
class Slot:
    """Represents a widget slot in a layout."""

    index: int
    rect: tuple[int, int, int, int]  # x1, y1, x2, y2
    widget: Widget | None = None


class Layout(ABC):
    """Base class for display layouts."""

    def __init__(self, padding: int = 8, gap: int = 8) -> None:
        """Initialize the layout.

        Args:
            padding: Padding around the edges
            gap: Gap between widgets
        """
        self.padding = padding
        self.gap = gap
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        self.slots: list[Slot] = []
        self._calculate_slots()

    @abstractmethod
    def _calculate_slots(self) -> None:
        """Calculate the slot rectangles. Override in subclasses."""

    def _available_space(self) -> tuple[int, int]:
        """Calculate available width and height after padding.

        Returns:
            Tuple of (available_width, available_height)
        """
        return (
            self.width - 2 * self.padding,
            self.height - 2 * self.padding,
        )

    def _grid_cell_size(self, rows: int, cols: int) -> tuple[int, int]:
        """Calculate cell size for a grid layout.

        Args:
            rows: Number of rows
            cols: Number of columns

        Returns:
            Tuple of (cell_width, cell_height)
        """
        aw, ah = self._available_space()
        return (
            (aw - (cols - 1) * self.gap) // cols,
            (ah - (rows - 1) * self.gap) // rows,
        )

    def _split_dimension(self, total: int, ratio: float) -> tuple[int, int]:
        """Split a dimension by ratio, accounting for gap.

        Args:
            total: Total available dimension (excluding gap)
            ratio: Ratio for first section (0.0-1.0)

        Returns:
            Tuple of (first_size, second_size)
        """
        content = total - self.gap
        first = int(content * ratio)
        second = content - first
        return first, second

    def get_slot_count(self) -> int:
        """Return the number of widget slots."""
        return len(self.slots)

    def get_slot(self, index: int) -> Slot | None:
        """Get a slot by index."""
        if 0 <= index < len(self.slots):
            return self.slots[index]
        return None

    def set_widget(self, index: int, widget: Widget) -> None:
        """Set a widget in a slot.

        Args:
            index: Slot index
            widget: Widget to place
        """
        if 0 <= index < len(self.slots):
            self.slots[index].widget = widget

    def render(
        self,
        renderer: Renderer,
        draw: ImageDraw.ImageDraw,
        hass: HomeAssistant | None = None,
    ) -> None:
        """Render all widgets in the layout.

        Args:
            renderer: Renderer instance
            draw: ImageDraw instance
            hass: Home Assistant instance
        """
        for slot in self.slots:
            widget = slot.widget
            if widget is None:
                continue
            ctx = RenderContext(draw, slot.rect, renderer)
            widget.render(ctx, hass)

    def get_all_entities(self) -> list[str]:
        """Get all entity IDs from all widgets."""
        entities = []
        for slot in self.slots:
            if slot.widget is not None:
                entities.extend(slot.widget.get_entities())
        return entities
