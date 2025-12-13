"""Data update coordinator for GeekMagic integration."""

from __future__ import annotations

import logging
import time
from datetime import timedelta
from typing import Any, cast

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_LAYOUT,
    CONF_REFRESH_INTERVAL,
    CONF_SCREEN_CYCLE_INTERVAL,
    CONF_SCREENS,
    CONF_WIDGETS,
    DEFAULT_REFRESH_INTERVAL,
    DEFAULT_SCREEN_CYCLE_INTERVAL,
    DOMAIN,
    LAYOUT_GRID_2X2,
    LAYOUT_GRID_2X3,
    LAYOUT_HERO,
    LAYOUT_SPLIT,
)
from .device import GeekMagicDevice
from .layouts.grid import Grid2x2, Grid2x3
from .layouts.hero import HeroLayout
from .layouts.split import SplitLayout
from .renderer import Renderer
from .widgets.base import WidgetConfig
from .widgets.chart import ChartWidget
from .widgets.clock import ClockWidget
from .widgets.entity import EntityWidget
from .widgets.gauge import GaugeWidget
from .widgets.media import MediaWidget
from .widgets.progress import MultiProgressWidget, ProgressWidget
from .widgets.status import StatusListWidget, StatusWidget
from .widgets.text import TextWidget
from .widgets.weather import WeatherWidget

_LOGGER = logging.getLogger(__name__)

LAYOUT_CLASSES = {
    LAYOUT_GRID_2X2: Grid2x2,
    LAYOUT_GRID_2X3: Grid2x3,
    LAYOUT_HERO: HeroLayout,
    LAYOUT_SPLIT: SplitLayout,
}

WIDGET_CLASSES = {
    "clock": ClockWidget,
    "entity": EntityWidget,
    "media": MediaWidget,
    "chart": ChartWidget,
    "text": TextWidget,
    "gauge": GaugeWidget,
    "progress": ProgressWidget,
    "multi_progress": MultiProgressWidget,
    "status": StatusWidget,
    "status_list": StatusListWidget,
    "weather": WeatherWidget,
}


class GeekMagicCoordinator(DataUpdateCoordinator):
    """Coordinator for GeekMagic display updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        device: GeekMagicDevice,
        options: dict[str, Any],
    ) -> None:
        """Initialize the coordinator.

        Args:
            hass: Home Assistant instance
            device: GeekMagic device client
            options: Integration options
        """
        self.device = device
        self.options = self._migrate_options(options)
        self.renderer = Renderer()
        self._layouts: list = []  # List of layouts for each screen
        self._current_screen: int = 0
        self._last_screen_change: float = time.time()
        self._last_image: bytes | None = None  # PNG bytes for camera preview

        # Get refresh interval from options
        interval = self.options.get(CONF_REFRESH_INTERVAL, DEFAULT_REFRESH_INTERVAL)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=interval),
        )

        # Initialize screens
        self._setup_screens()

    def _migrate_options(self, options: dict[str, Any]) -> dict[str, Any]:
        """Migrate old single-screen options to new multi-screen format.

        Args:
            options: Original options dictionary

        Returns:
            Migrated options with screens structure
        """
        if CONF_SCREENS in options:
            return options  # Already in new format

        # Convert old format to new format
        return {
            CONF_REFRESH_INTERVAL: options.get(CONF_REFRESH_INTERVAL, DEFAULT_REFRESH_INTERVAL),
            CONF_SCREEN_CYCLE_INTERVAL: DEFAULT_SCREEN_CYCLE_INTERVAL,
            CONF_SCREENS: [
                {
                    "name": "Screen 1",
                    CONF_LAYOUT: options.get(CONF_LAYOUT, LAYOUT_GRID_2X2),
                    CONF_WIDGETS: options.get(CONF_WIDGETS, [{"type": "clock", "slot": 0}]),
                }
            ],
        }

    def _setup_screens(self) -> None:
        """Set up all screens with their layouts and widgets."""
        self._layouts = []
        screens = self.options.get(CONF_SCREENS, [])

        for screen_config in screens:
            layout = self._create_layout(screen_config)
            self._layouts.append(layout)

        # Ensure current screen is valid
        if self._current_screen >= len(self._layouts):
            self._current_screen = 0

    def _create_layout(self, screen_config: dict[str, Any]):
        """Create a layout from screen configuration.

        Args:
            screen_config: Screen configuration dictionary

        Returns:
            Configured layout instance
        """
        layout_type = screen_config.get(CONF_LAYOUT, LAYOUT_GRID_2X2)
        layout_class = LAYOUT_CLASSES.get(layout_type, Grid2x2)
        layout = layout_class()

        widgets_config = screen_config.get(CONF_WIDGETS, [])

        # If no widgets configured, add default clock widget
        if not widgets_config:
            widgets_config = [{"type": "clock", "slot": 0}]

        for widget_config in widgets_config:
            widget_type = str(widget_config.get("type", "text"))
            slot = int(widget_config.get("slot", 0))

            if slot >= layout.get_slot_count():
                continue

            widget_class = WIDGET_CLASSES.get(widget_type)
            if widget_class is None:
                continue

            entity_id = widget_config.get("entity_id")
            label = widget_config.get("label")
            raw_color = widget_config.get("color")
            widget_options = widget_config.get("options") or {}

            # Parse color - can be tuple/list of RGB values
            parsed_color: tuple[int, int, int] | None = None
            if isinstance(raw_color, list | tuple) and len(raw_color) == 3:
                parsed_color = (int(raw_color[0]), int(raw_color[1]), int(raw_color[2]))

            config = WidgetConfig(
                widget_type=widget_type,
                slot=slot,
                entity_id=str(entity_id) if entity_id is not None else None,
                label=str(label) if label is not None else None,
                color=parsed_color,
                options=cast("dict[str, Any]", widget_options),
            )

            widget = widget_class(config)
            layout.set_widget(slot, widget)

        return layout

    @property
    def current_screen(self) -> int:
        """Get current screen index."""
        return self._current_screen

    @property
    def screen_count(self) -> int:
        """Get total number of screens."""
        return len(self._layouts)

    @property
    def current_screen_name(self) -> str:
        """Get current screen name."""
        screens = self.options.get(CONF_SCREENS, [])
        if 0 <= self._current_screen < len(screens):
            return screens[self._current_screen].get("name", f"Screen {self._current_screen + 1}")
        return "Unknown"

    async def async_set_screen(self, screen_index: int) -> None:
        """Switch to a specific screen.

        Args:
            screen_index: Screen index (0-based)
        """
        if 0 <= screen_index < len(self._layouts):
            self._current_screen = screen_index
            self._last_screen_change = time.time()
            await self.async_request_refresh()

    async def async_next_screen(self) -> None:
        """Switch to the next screen."""
        if len(self._layouts) > 0:
            next_screen = (self._current_screen + 1) % len(self._layouts)
            await self.async_set_screen(next_screen)

    async def async_previous_screen(self) -> None:
        """Switch to the previous screen."""
        if len(self._layouts) > 0:
            prev_screen = (self._current_screen - 1) % len(self._layouts)
            await self.async_set_screen(prev_screen)

    def update_options(self, options: dict[str, Any]) -> None:
        """Update coordinator options.

        Args:
            options: New options dictionary
        """
        self.options = self._migrate_options(options)

        # Update refresh interval
        interval = self.options.get(CONF_REFRESH_INTERVAL, DEFAULT_REFRESH_INTERVAL)
        self.update_interval = timedelta(seconds=interval)

        # Rebuild all screens
        self._setup_screens()

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data and update display.

        Returns:
            Dictionary with update status
        """
        try:
            # Check for auto-cycling
            cycle_interval = self.options.get(
                CONF_SCREEN_CYCLE_INTERVAL, DEFAULT_SCREEN_CYCLE_INTERVAL
            )
            if cycle_interval > 0 and len(self._layouts) > 1:
                now = time.time()
                if now - self._last_screen_change >= cycle_interval:
                    self._current_screen = (self._current_screen + 1) % len(self._layouts)
                    self._last_screen_change = now

            # Create canvas
            img, draw = self.renderer.create_canvas()

            # Render current screen's layout
            if self._layouts and 0 <= self._current_screen < len(self._layouts):
                layout = self._layouts[self._current_screen]
                layout.render(self.renderer, draw, self.hass)

            # Store PNG for camera preview
            self._last_image = self.renderer.to_png(img)

            # Convert to JPEG and upload
            jpeg_data = self.renderer.to_jpeg(img)
            await self.device.upload_and_display(jpeg_data, "dashboard.jpg")

            return {
                "success": True,
                "size_kb": len(jpeg_data) / 1024,
                "current_screen": self._current_screen,
                "screen_name": self.current_screen_name,
            }

        except Exception as err:
            _LOGGER.exception("Error updating GeekMagic display")
            raise UpdateFailed(f"Error updating display: {err}") from err

    @property
    def last_image(self) -> bytes | None:
        """Get the last rendered image as PNG bytes."""
        return self._last_image

    async def async_set_brightness(self, brightness: int) -> None:
        """Set display brightness.

        Args:
            brightness: Brightness level 0-100
        """
        await self.device.set_brightness(brightness)

    async def async_refresh_display(self) -> None:
        """Force an immediate display refresh."""
        await self.async_request_refresh()
