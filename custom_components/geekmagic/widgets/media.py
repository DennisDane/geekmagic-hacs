"""Media player widget for GeekMagic displays."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from PIL import Image

from ..const import COLOR_CYAN
from .base import Widget, WidgetConfig
from .components import (
    THEME_TEXT_PRIMARY,
    THEME_TEXT_SECONDARY,
    Bar,
    Color,
    Column,
    Component,
    Icon,
    Row,
    Spacer,
    Text,
)

if TYPE_CHECKING:
    from ..render_context import RenderContext
    from .state import WidgetState


def _format_time(seconds: float) -> str:
    """Format seconds as MM:SS or HH:MM:SS."""
    seconds = int(seconds)
    if seconds >= 3600:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours}:{minutes:02d}:{secs:02d}"
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


@dataclass
class ImageFill(Component):
    """Component that fills its area with an image."""

    image: Image.Image
    fit: str = "cover"  # "cover", "contain", "fill"

    def measure(self, ctx: RenderContext, max_width: int, max_height: int) -> tuple[int, int]:
        return (max_width, max_height)

    def render(self, ctx: RenderContext, x: int, y: int, width: int, height: int) -> None:
        ctx.draw_image(self.image, rect=(x, y, x + width, y + height), fit_mode=self.fit)


@dataclass
class DarkOverlay(Component):
    """Dark overlay that sits at the bottom portion of its container."""

    height_ratio: float = 0.35  # Portion of height to cover
    color: Color = (10, 10, 10)

    def measure(self, ctx: RenderContext, max_width: int, max_height: int) -> tuple[int, int]:
        return (max_width, max_height)

    def render(self, ctx: RenderContext, x: int, y: int, width: int, height: int) -> None:
        overlay_height = int(height * self.height_ratio)
        overlay_y = y + height - overlay_height
        ctx.draw_rect((x, overlay_y, x + width, y + height), fill=self.color)


@dataclass
class AlbumArt(Component):
    """Album art display with overlay showing track info.

    Uses Stack to layer: image -> dark overlay -> text info -> progress bar.
    Inspired by Spotify/Apple Music now playing screens.
    """

    image: Image.Image
    title: str = ""
    artist: str = ""
    position: float = 0
    duration: float = 0
    color: Color = COLOR_CYAN
    show_progress: bool = True
    show_overlay: bool = True

    def measure(self, ctx: RenderContext, max_width: int, max_height: int) -> tuple[int, int]:
        return (max_width, max_height)

    def render(self, ctx: RenderContext, x: int, y: int, width: int, height: int) -> None:
        """Render album art with overlay using component composition."""
        # Layer 1: Album art background
        ImageFill(image=self.image, fit="cover").render(ctx, x, y, width, height)

        if not self.show_overlay:
            return

        # Determine sizing based on available space
        # 3x3 grid on 240px = ~75px cells, 2x1 = ~115px height
        is_micro = height < 78  # Very small cells - title only, tiny font
        is_tiny = height < 120  # Small cells - title only
        is_small = height < 180  # Medium cells - title + artist (no time)

        # Overlay ratio varies by size - smaller for small cells
        if is_micro:
            overlay_ratio = 0.28  # Minimal overlay for micro
        elif is_tiny:
            overlay_ratio = 0.32
        elif is_small:
            overlay_ratio = 0.30
        else:
            overlay_ratio = 0.28

        # Layer 2: Dark overlay at bottom
        DarkOverlay(height_ratio=overlay_ratio).render(ctx, x, y, width, height)

        # Layer 3: Text content positioned at bottom
        overlay_height = int(height * overlay_ratio)
        text_area_y = y + height - overlay_height
        # Smaller padding for micro cells to fit more text
        padding = max(2, int(width * 0.02)) if is_micro else max(4, int(width * 0.04))

        # Build text components
        text_children: list[Component] = []

        # Title - always show, smaller font for micro cells
        if self.title:
            if is_micro:
                title_font = "tiny"
                title_bold = False
            elif is_tiny:
                title_font = "tiny"
                title_bold = True
            else:
                title_font = "small"
                title_bold = True

            text_children.append(
                Text(
                    self.title,
                    font=title_font,
                    color=(255, 255, 255),
                    bold=title_bold,
                    align="start",
                    truncate=True,
                )
            )

        # Artist - hide in micro/tiny mode
        if self.artist and not is_tiny and not is_micro:
            text_children.append(
                Text(
                    self.artist,
                    font="tiny",
                    color=(160, 160, 160),
                    align="start",
                    truncate=True,
                )
            )

        # Time display for larger cells only
        if self.duration > 0 and not is_small and not is_tiny and not is_micro:
            pos_str = _format_time(self.position)
            dur_str = _format_time(self.duration)
            time_str = f"{pos_str} / {dur_str}"
            text_children.append(
                Text(
                    time_str,
                    font="tiny",
                    color=(120, 120, 120),
                    align="start",
                )
            )

        # Render text column in overlay area
        if text_children:
            text_column = Column(
                children=text_children,
                align="start",
                justify="end",  # Stack from bottom up
                padding=padding,
                gap=1,  # Minimal gap between items
            )
            # Position text in overlay area (leaving room for progress bar)
            bar_height = max(2, int(height * 0.015)) if self.show_progress else 0
            text_height = overlay_height - bar_height - padding
            text_column.render(ctx, x, text_area_y, width, text_height)

        # Layer 4: Progress bar at very bottom
        if self.show_progress and self.duration > 0:
            progress = min(100, (self.position / self.duration) * 100)
            bar_height = max(2, int(height * 0.015))
            bar_y = y + height - bar_height

            # Use Bar component
            Bar(
                percent=progress,
                color=self.color,
                background=(40, 40, 40),
                height=bar_height,
            ).render(ctx, x, bar_y, width, bar_height)


@dataclass
class NowPlaying(Component):
    """Now playing display component (text-only version)."""

    title: str
    artist: str = ""
    album: str = ""
    position: float = 0
    duration: float = 0
    color: Color = COLOR_CYAN
    show_artist: bool = True
    show_album: bool = False
    show_progress: bool = True

    def measure(self, ctx: RenderContext, max_width: int, max_height: int) -> tuple[int, int]:
        return (max_width, max_height)

    def render(self, ctx: RenderContext, x: int, y: int, width: int, height: int) -> None:
        """Render now playing info."""
        padding = int(width * 0.05)

        # Truncate text
        max_chars = (width - padding * 2) // 8
        title = self.title[: max_chars - 2] + ".." if len(self.title) > max_chars else self.title
        artist = (
            self.artist[: max_chars - 2] + ".." if len(self.artist) > max_chars else self.artist
        )
        album = self.album[: max_chars - 2] + ".." if len(self.album) > max_chars else self.album

        # Build component tree
        children = [
            Text("NOW PLAYING", font="small", color=THEME_TEXT_SECONDARY),
            Spacer(min_size=int(height * 0.03)),
            Text(title, font="regular", color=THEME_TEXT_PRIMARY),
        ]

        if self.show_artist and artist:
            children.append(Spacer(min_size=int(height * 0.02)))
            children.append(Text(artist, font="small", color=THEME_TEXT_SECONDARY))

        if self.show_album and self.album:
            children.append(Spacer(min_size=int(height * 0.02)))
            children.append(Text(album, font="small", color=THEME_TEXT_SECONDARY))

        # Add spacer before progress section
        children.append(Spacer())

        # Progress bar and time labels
        if self.show_progress and self.duration > 0:
            progress = min(100, (self.position / self.duration) * 100)
            pos_str = _format_time(self.position)
            dur_str = _format_time(self.duration)

            children.extend(
                [
                    Bar(
                        percent=progress,
                        color=self.color,
                        height=max(4, int(height * 0.05)),
                    ),
                    Spacer(min_size=int(height * 0.02)),
                    Row(
                        children=[
                            Text(pos_str, font="small", color=THEME_TEXT_SECONDARY, align="start"),
                            Spacer(),
                            Text(dur_str, font="small", color=THEME_TEXT_SECONDARY, align="end"),
                        ]
                    ),
                ]
            )

        # Render the column
        Column(children=children, padding=padding, align="center").render(ctx, x, y, width, height)


@dataclass
class MediaIdle(Component):
    """Idle/paused state display."""

    def measure(self, ctx: RenderContext, max_width: int, max_height: int) -> tuple[int, int]:
        return (max_width, max_height)

    def render(self, ctx: RenderContext, x: int, y: int, width: int, height: int) -> None:
        """Render paused state."""
        # Calculate icon size
        icon_size = max(24, int(height * 0.25))

        # Build component tree
        Column(
            children=[
                Icon("pause", size=icon_size, color=THEME_TEXT_SECONDARY),
                Spacer(min_size=int(height * 0.08)),
                Text("PAUSED", font="small", color=THEME_TEXT_SECONDARY),
            ],
            align="center",
            justify="center",
        ).render(ctx, x, y, width, height)


class MediaWidget(Widget):
    """Widget that displays media player information."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the media widget."""
        super().__init__(config)
        self.show_artist = config.options.get("show_artist", True)
        self.show_album = config.options.get("show_album", False)
        self.show_progress = config.options.get("show_progress", True)
        self.show_album_art = config.options.get("show_album_art", True)

    def render(self, ctx: RenderContext, state: WidgetState) -> Component:
        """Render the media player widget.

        Args:
            ctx: RenderContext for drawing
            state: Widget state with entity data
        """
        entity = state.entity

        if entity is None or entity.state in ("off", "unavailable", "unknown", "idle"):
            return MediaIdle()

        # Use album art if available and enabled
        if self.show_album_art and state.image is not None:
            return AlbumArt(
                image=state.image.convert("RGB") if state.image.mode != "RGB" else state.image,
                title=entity.get("media_title", ""),
                artist=entity.get("media_artist", ""),
                position=entity.get("media_position", 0),
                duration=entity.get("media_duration", 0),
                color=self.config.color or COLOR_CYAN,
                show_progress=self.show_progress,
                show_overlay=True,
            )

        return NowPlaying(
            title=entity.get("media_title", "Unknown"),
            artist=entity.get("media_artist", ""),
            album=entity.get("media_album_name", ""),
            position=entity.get("media_position", 0),
            duration=entity.get("media_duration", 0),
            color=self.config.color or COLOR_CYAN,
            show_artist=self.show_artist,
            show_album=self.show_album,
            show_progress=self.show_progress,
        )
