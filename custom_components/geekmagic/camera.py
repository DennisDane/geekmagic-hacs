"""Camera platform for GeekMagic display preview."""

from __future__ import annotations

import logging
from functools import lru_cache
from io import BytesIO
from typing import TYPE_CHECKING

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from PIL import Image, ImageDraw

from .const import DISPLAY_HEIGHT, DISPLAY_WIDTH, DOMAIN

if TYPE_CHECKING:
    from .coordinator import GeekMagicCoordinator

_LOGGER = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_placeholder_png() -> bytes:
    """Generate a 240x240 placeholder PNG image.

    Returns a dark gray image with "Loading..." text.
    Generated once and cached for reuse.
    """
    # Create a 240x240 dark image
    img = Image.new("RGB", (DISPLAY_WIDTH, DISPLAY_HEIGHT), (32, 32, 32))
    draw = ImageDraw.Draw(img)

    # Draw "Loading..." text centered
    text = "Loading..."
    bbox = draw.textbbox((0, 0), text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (DISPLAY_WIDTH - text_width) // 2
    y = (DISPLAY_HEIGHT - text_height) // 2
    draw.text((x, y), text, fill=(128, 128, 128))

    # Convert to PNG bytes
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    result = buffer.getvalue()

    _LOGGER.debug("Generated placeholder PNG: %d bytes", len(result))
    return result


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up GeekMagic camera from a config entry."""
    coordinator: GeekMagicCoordinator = hass.data[DOMAIN][entry.entry_id]

    _LOGGER.debug("Setting up GeekMagic camera for %s", entry.data.get(CONF_HOST))
    async_add_entities([GeekMagicPreviewCamera(coordinator, entry)])


class GeekMagicPreviewCamera(Camera):
    """Camera entity showing the GeekMagic display preview."""

    _attr_has_entity_name = True
    _attr_name = "Display Preview"
    _attr_frame_interval = 10.0

    def __init__(
        self,
        coordinator: GeekMagicCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the camera."""
        super().__init__()
        self.coordinator = coordinator
        self._entry = entry
        self._last_image: bytes | None = None

        # Set content type to PNG since that's what the coordinator returns
        self.content_type = "image/png"

        # Entity attributes
        self._attr_unique_id = f"{entry.data[CONF_HOST]}_preview"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data[CONF_HOST])},
            "name": entry.data.get(CONF_NAME, "GeekMagic Display"),
            "manufacturer": "GeekMagic",
            "model": "SmallTV Pro",
        }

        # Update frame interval from coordinator
        if coordinator.update_interval:
            self._attr_frame_interval = coordinator.update_interval.total_seconds()

        _LOGGER.debug(
            "Initialized GeekMagic camera %s with content_type=%s, frame_interval=%s",
            self._attr_unique_id,
            self.content_type,
            self._attr_frame_interval,
        )

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        # Listen to coordinator updates
        self.async_on_remove(self.coordinator.async_add_listener(self._handle_coordinator_update))
        # Initialize with current image
        self._last_image = self.coordinator.last_image

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        new_image = self.coordinator.last_image
        if new_image is not None:
            self._last_image = new_image
        self.async_write_ha_state()

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes:
        """Return the current camera image.

        Always returns an image - either the current display or a placeholder.
        This ensures MJPEG streams don't break when no image is ready.
        """
        try:
            # Use cached image from coordinator
            image = self._last_image or self.coordinator.last_image
            if image is not None:
                self._last_image = image
                _LOGGER.debug(
                    "Camera %s: Returning image of %d bytes",
                    self._attr_unique_id,
                    len(image),
                )
                return image

            # Return placeholder to prevent stream from breaking
            _LOGGER.debug(
                "Camera %s: No image available yet, returning placeholder",
                self._attr_unique_id,
            )
            return _get_placeholder_png()
        except Exception:
            _LOGGER.exception("Camera %s: Error getting image", self._attr_unique_id)
            return _get_placeholder_png()

    @property
    def available(self) -> bool:
        """Return True if the camera is available."""
        available = self.coordinator.last_update_success
        if not available:
            _LOGGER.debug(
                "Camera %s: Not available (coordinator last_update_success=%s)",
                self._attr_unique_id,
                available,
            )
        return available
