"""Layout helper functions for widget rendering.

These helpers provide common layout patterns used across multiple widgets,
reducing code duplication and ensuring consistent spacing/positioning.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..const import COLOR_GRAY, COLOR_WHITE

if TYPE_CHECKING:
    from ..render_context import RenderContext


def layout_icon_label_value(
    ctx: RenderContext,
    icon: str | None,
    label: str,
    value: str,
    color: tuple[int, int, int],
    label_color: tuple[int, int, int] = COLOR_GRAY,
    value_color: tuple[int, int, int] = COLOR_WHITE,
    padding_percent: float = 0.05,
    icon_size_percent: float = 0.35,
) -> None:
    """Render horizontal layout: [Icon] [Label] ... [Value].

    Common pattern for widgets showing an icon, label on left, value on right.

    Args:
        ctx: RenderContext for drawing
        icon: Icon name (can be None to skip icon)
        label: Label text (displayed left-aligned after icon)
        value: Value text (displayed right-aligned)
        color: Icon color
        label_color: Label text color (default: COLOR_GRAY)
        value_color: Value text color (default: COLOR_WHITE)
        padding_percent: Horizontal padding as percentage of width
        icon_size_percent: Icon size as percentage of height
    """
    center_y = ctx.height // 2
    padding = int(ctx.width * padding_percent)
    icon_size = max(10, int(ctx.height * icon_size_percent))

    font = ctx.get_font("small")

    # Draw icon if present
    text_x = padding
    if icon:
        ctx.draw_icon(icon, (padding, center_y - icon_size // 2), icon_size, color)
        text_x = padding + icon_size + 4

    # Draw label
    ctx.draw_text(label, (text_x, center_y), font, label_color, anchor="lm")

    # Draw value
    ctx.draw_text(value, (ctx.width - padding, center_y), font, value_color, anchor="rm")


def layout_centered_value(
    ctx: RenderContext,
    value: str,
    label: str | None = None,
    color: tuple[int, int, int] = COLOR_WHITE,
    label_color: tuple[int, int, int] = COLOR_GRAY,
    value_font: str = "large",
    label_font: str = "tiny",
    show_label: bool = True,
) -> None:
    """Render centered value with optional label below.

    Common pattern for entity values displayed prominently in center.

    Args:
        ctx: RenderContext for drawing
        value: Main value text
        label: Optional label text below value
        color: Value text color
        label_color: Label text color
        value_font: Font size name for value
        label_font: Font size name for label
        show_label: Whether to show the label
    """
    center_x = ctx.width // 2
    center_y = ctx.height // 2

    font_value = ctx.get_font(value_font)
    font_label = ctx.get_font(label_font)

    # Offset value up if showing label
    offset_y = int(ctx.height * 0.07) if show_label and label else 0
    value_y = center_y - offset_y

    # Draw value
    ctx.draw_text(value, (center_x, value_y), font_value, color, anchor="mm")

    # Draw label
    if show_label and label:
        label_y = ctx.height - int(ctx.height * 0.12)
        ctx.draw_text(label.upper(), (center_x, label_y), font_label, label_color, anchor="mm")


def layout_icon_centered_value(
    ctx: RenderContext,
    icon: str,
    value: str,
    label: str | None = None,
    color: tuple[int, int, int] = COLOR_WHITE,
    label_color: tuple[int, int, int] = COLOR_GRAY,
    show_label: bool = True,
) -> None:
    """Render icon at top, value in middle, label at bottom.

    Common pattern for compact entity displays with icon.

    Args:
        ctx: RenderContext for drawing
        icon: Icon name
        value: Main value text
        label: Optional label text at bottom
        color: Icon and value color
        label_color: Label text color
        show_label: Whether to show the label
    """
    center_x = ctx.width // 2

    font_value = ctx.get_font("medium", bold=True)
    font_label = ctx.get_font("tiny")

    # Layout: icon at top, value in middle, label at bottom
    icon_size = max(12, min(24, int(ctx.height * 0.25)))
    padding = int(ctx.height * 0.08)

    # Draw icon
    ctx.draw_icon(icon, (center_x - icon_size // 2, padding), icon_size, color)

    # Draw value
    value_y = int(ctx.height * 0.55)
    ctx.draw_text(value, (center_x, value_y), font_value, COLOR_WHITE, anchor="mm")

    # Draw label
    if show_label and label:
        ctx.draw_text(
            label.upper(),
            (center_x, ctx.height - int(ctx.height * 0.12)),
            font_label,
            label_color,
            anchor="mm",
        )


def layout_bar_with_label(
    ctx: RenderContext,
    percent: float,
    label: str,
    value: str,
    color: tuple[int, int, int],
    background: tuple[int, int, int],
    icon: str | None = None,
    label_color: tuple[int, int, int] = COLOR_GRAY,
    value_color: tuple[int, int, int] = COLOR_WHITE,
) -> None:
    """Render progress bar with label/value above.

    Common pattern for gauge and progress widgets.

    Args:
        ctx: RenderContext for drawing
        percent: Progress percentage (0-100)
        label: Label text
        value: Value text
        color: Bar fill color
        background: Bar background color
        icon: Optional icon name
        label_color: Label text color
        value_color: Value text color
    """
    font_label = ctx.get_font("tiny")
    font_value = ctx.get_font("medium", bold=True)

    # Calculate layout
    padding = int(ctx.height * 0.13)
    icon_size = max(10, int(ctx.height * 0.23))
    label_y = int(ctx.height * 0.33)
    bar_height = max(6, int(ctx.height * 0.17))
    bar_y = int(ctx.height * 0.67) - bar_height // 2

    # Draw icon if present
    text_start_x = padding
    if icon:
        ctx.draw_icon(icon, (padding, label_y - icon_size // 2), icon_size, color)
        text_start_x = padding + icon_size + 4

    # Draw label
    if label:
        ctx.draw_text(label.upper(), (text_start_x, label_y), font_label, label_color, anchor="lm")

    # Draw value
    ctx.draw_text(value, (ctx.width - padding, label_y), font_value, value_color, anchor="rm")

    # Draw bar
    bar_rect = (padding, bar_y, ctx.width - padding, bar_y + bar_height)
    ctx.draw_bar(bar_rect, percent, color, background)


def layout_list_rows(
    ctx: RenderContext,
    item_count: int,
    title: str | None = None,
    max_row_height_percent: float = 0.35,
    title_height_percent: float = 0.15,
    padding_percent: float = 0.05,
) -> list[tuple[int, int]]:
    """Calculate row positions for list-based widgets.

    Returns list of (y_position, row_height) tuples for each item.

    Args:
        ctx: RenderContext for drawing
        item_count: Number of items to display
        title: Optional title (affects starting Y position)
        max_row_height_percent: Maximum row height as percent of container
        title_height_percent: Title height as percent of container
        padding_percent: Padding as percent of width

    Returns:
        List of (y, height) tuples for each row
    """
    padding = int(ctx.width * padding_percent)
    current_y = padding

    # Account for title
    if title:
        title_height = int(ctx.height * title_height_percent)
        current_y += title_height

    # Calculate row height
    available_height = ctx.height - current_y - padding
    max_row_height = int(ctx.height * max_row_height_percent)
    row_height = min(max_row_height, available_height // max(item_count, 1))

    # Generate row positions
    return [(current_y + i * row_height, row_height) for i in range(item_count)]


def draw_title(
    ctx: RenderContext,
    title: str,
    color: tuple[int, int, int] = COLOR_GRAY,
    padding_percent: float = 0.05,
) -> int:
    """Draw a title at the top of the widget.

    Args:
        ctx: RenderContext for drawing
        title: Title text
        color: Title color
        padding_percent: Padding as percent of width

    Returns:
        Y position after title (for content below)
    """
    padding = int(ctx.width * padding_percent)
    font_title = ctx.get_font("small")

    ctx.draw_text(title.upper(), (padding, padding), font_title, color, anchor="lm")

    return padding + int(ctx.height * 0.15)
