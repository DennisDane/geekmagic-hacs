"""Progress widget for GeekMagic displays."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar

from ..const import COLOR_CYAN, COLOR_DARK_GRAY
from ..render_context import SizeCategory, get_size_category
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
    from .state import EntityState, WidgetState


def _parse_float(value: object) -> float | None:
    """Parse a float value, returning None on invalid input."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _coerce_float(value: object, default: float) -> float:
    """Coerce a value to float with fallback."""
    parsed = _parse_float(value)
    if parsed is None:
        return default
    return parsed


def _coerce_precision(value: object, default: int) -> int:
    """Coerce precision to an integer in [0, 6]."""
    try:
        precision = int(value)
    except (ValueError, TypeError):
        precision = default
    return max(0, min(6, precision))


def _normalize_entity_id(value: object) -> str | None:
    """Normalize optional entity ID values."""
    if isinstance(value, str) and value:
        return value
    return None


def _format_fixed(value: float, precision: int) -> str:
    """Format a numeric value with fixed decimal places."""
    return f"{value:.{precision}f}"


def _extract_numeric(entity: EntityState | None) -> float:
    """Extract numeric value from entity state."""
    if entity is None:
        return 0.0
    parsed = _parse_float(entity.state)
    if parsed is None:
        return 0.0
    return parsed


@dataclass
class ProgressDisplay(Component):
    """Progress bar display component."""

    value: float
    target: float = 100
    label: str = "Progress"
    unit: str = ""
    color: Color = COLOR_CYAN
    icon: str | None = None
    show_target: bool = True
    bar_height_style: str = "normal"
    precision: int = 1

    BAR_HEIGHT_MULTIPLIERS: ClassVar[dict[str, float]] = {
        "thin": 0.10,
        "normal": 0.17,
        "thick": 0.25,
    }

    def measure(self, ctx: RenderContext, max_width: int, max_height: int) -> tuple[int, int]:
        return (max_width, max_height)

    def render(self, ctx: RenderContext, x: int, y: int, width: int, height: int) -> None:
        """Render progress display."""
        padding = int(width * 0.05)
        bar_height_mult = self.BAR_HEIGHT_MULTIPLIERS.get(self.bar_height_style, 0.17)
        bar_height = max(4, int(height * bar_height_mult))

        display_value = _format_fixed(self.value, self.precision)
        target = self.target
        display_target = _format_fixed(target, self.precision)
        percent = min(100, (self.value / target) * 100) if target > 0 else 0

        value_text = f"{display_value}/{display_target}" if self.show_target else display_value
        if self.unit:
            value_text += f" {self.unit}"
        label_text = self.label.upper()

        # Adaptive layout based on size using standard size categories
        # Compact: MICRO cells in dense grids
        # Standard: TINY/SMALL cells, horizontal layout
        # Expanded: MEDIUM/LARGE cells, vertical layout with icon/label separate from value
        size = get_size_category(height)
        is_compact = size == SizeCategory.MICRO
        is_expanded = size in (SizeCategory.MEDIUM, SizeCategory.LARGE)

        if is_expanded:
            # Expanded: icon + label on top, value below, bar + percent at bottom
            icon_size = max(16, int(height * 0.18))

            # Row 1: Icon + Label (centered)
            header_children: list[Component] = []
            if self.icon:
                header_children.append(Icon(name=self.icon, size=icon_size, color=self.color))
            header_children.append(
                Text(text=label_text, font="small", color=THEME_TEXT_SECONDARY, align="center")
            )

            # Row 2: Value (centered, larger)
            value_row = Row(
                children=[
                    Text(text=value_text, font="large", color=THEME_TEXT_PRIMARY, align="center")
                ],
                justify="center",
                padding=padding,
            )

            # Row 3: Bar + Percent
            bar_row = Row(
                children=[
                    Bar(
                        percent=percent,
                        color=self.color,
                        background=COLOR_DARK_GRAY,
                        height=bar_height,
                    ),
                    Text(
                        text=f"{percent:.0f}%", font="small", color=THEME_TEXT_PRIMARY, align="end"
                    ),
                ],
                gap=8,
                align="center",
                padding=padding,
            )

            Column(
                children=[
                    Row(children=header_children, gap=6, justify="center", padding=padding),
                    value_row,
                    bar_row,
                ],
                gap=int(height * 0.06),
                justify="center",
                align="stretch",
            ).render(ctx, x, y, width, height)

        elif is_compact:
            # Compact: icon + value on first line, bar + percent on second
            icon_size = max(10, int(height * 0.20))

            row1_children: list[Component] = []
            if self.icon:
                row1_children.append(Icon(name=self.icon, size=icon_size, color=self.color))
            row1_children.append(
                Text(text=value_text, font="small", color=THEME_TEXT_PRIMARY, align="start")
            )

            row2_children: list[Component] = [
                Bar(
                    percent=percent,
                    color=self.color,
                    background=COLOR_DARK_GRAY,
                    height=bar_height,
                ),
                Text(text=f"{percent:.0f}%", font="tiny", color=THEME_TEXT_PRIMARY, align="end"),
            ]

            Column(
                children=[
                    Row(children=row1_children, gap=4, align="center", padding=padding),
                    Row(children=row2_children, gap=8, align="center", padding=padding),
                ],
                gap=int(height * 0.10),
                justify="center",
                align="stretch",
            ).render(ctx, x, y, width, height)

        else:
            # Standard: icon + label + value on first line, bar + percent on second
            icon_size = max(10, int(height * 0.20))

            top_row_children: list[Component] = []
            if self.icon:
                top_row_children.append(Icon(name=self.icon, size=icon_size, color=self.color))

            # Check if label fits by measuring
            font_label = ctx.get_font("small")
            font_value = ctx.get_font("regular")
            label_width, _ = ctx.get_text_size(label_text, font_label)
            value_width, _ = ctx.get_text_size(value_text, font_value)
            icon_width = icon_size + 4 if self.icon else 0
            available_for_label = width - padding * 2 - icon_width - value_width - 8

            if available_for_label >= label_width:
                top_row_children.extend(
                    [
                        Text(
                            text=label_text, font="small", color=THEME_TEXT_SECONDARY, align="start"
                        ),
                        Spacer(),
                        Text(
                            text=value_text, font="regular", color=THEME_TEXT_PRIMARY, align="end"
                        ),
                    ]
                )
            else:
                top_row_children.append(
                    Text(text=value_text, font="regular", color=THEME_TEXT_PRIMARY, align="start")
                )

            bottom_row_children: list[Component] = [
                Bar(
                    percent=percent,
                    color=self.color,
                    background=COLOR_DARK_GRAY,
                    height=bar_height,
                ),
                Text(text=f"{percent:.0f}%", font="small", color=THEME_TEXT_PRIMARY, align="end"),
            ]

            Column(
                children=[
                    Row(children=top_row_children, gap=4, align="center", padding=padding),
                    Row(children=bottom_row_children, gap=8, align="center", padding=padding),
                ],
                gap=int(height * 0.10),
                justify="center",
                align="stretch",
            ).render(ctx, x, y, width, height)


class ProgressWidget(Widget):
    """Widget that displays progress with label."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the progress widget."""
        super().__init__(config)
        self.target = _coerce_float(config.options.get("target", 100), 100.0)
        self.target_entity = _normalize_entity_id(config.options.get("target_entity"))
        self.precision = _coerce_precision(config.options.get("precision", 1), default=1)
        self.unit = config.options.get("unit", "")
        self.show_target = config.options.get("show_target", True)
        self.icon = config.options.get("icon")
        self.bar_height_style = config.options.get("bar_height", "normal")

    def get_entities(self) -> list[str]:
        """Return list of entity IDs this widget depends on."""
        entities = super().get_entities()
        if self.target_entity and self.target_entity not in entities:
            entities.append(self.target_entity)
        return entities

    def _resolve_target(self, state: WidgetState) -> float:
        """Resolve target from template/entity/static options."""
        resolved_target = _parse_float(state.get_resolved_option("target"))
        if resolved_target is not None:
            return resolved_target

        if not self.target_entity:
            return self.target

        target_entity = state.get_entity(self.target_entity)
        if target_entity is None:
            return self.target

        parsed = _parse_float(target_entity.state)
        if parsed is None:
            return self.target
        return parsed

    def render(self, ctx: RenderContext, state: WidgetState) -> Component:
        """Render the progress widget."""
        entity = state.entity
        value = _extract_numeric(entity)
        target = self._resolve_target(state)

        unit = self.unit
        if not unit and entity:
            unit = entity.unit or ""

        label = self.config.label
        if not label and entity:
            label = entity.friendly_name
        label = label or "Progress"

        return ProgressDisplay(
            value=value,
            target=target,
            label=label,
            unit=unit,
            color=self.config.color or ctx.theme.get_accent_color(self.config.slot),
            icon=self.icon,
            show_target=self.show_target,
            bar_height_style=self.bar_height_style,
            precision=self.precision,
        )


@dataclass
class MultiProgressDisplay(Component):
    """Multi-progress list display component."""

    items: list[dict] = field(default_factory=list)
    title: str | None = None
    precision: int = 0

    def measure(self, ctx: RenderContext, max_width: int, max_height: int) -> tuple[int, int]:
        return (max_width, max_height)

    def render(self, ctx: RenderContext, x: int, y: int, width: int, height: int) -> None:
        """Render multi-progress list."""
        padding = int(width * 0.05)
        row_count = len(self.items) or 1

        # Calculate sizes
        title_height = int(height * 0.14) if self.title else 0
        available_height = height - title_height - padding * 2
        row_height = min(int(height * 0.35), available_height // row_count)
        bar_height = max(4, int(height * 0.06))
        icon_size = max(8, int(height * 0.09))

        # Build component tree
        children = []

        # Add title if present
        if self.title:
            children.append(
                Row(
                    children=[
                        Text(
                            text=self.title.upper(),
                            font="small",
                            color=THEME_TEXT_SECONDARY,
                            align="start",
                        )
                    ],
                    padding=padding,
                )
            )

        # Build each progress item row
        for i, item in enumerate(self.items):
            label = item.get("label", "Item")
            value = item.get("value", 0)
            target = item.get("target", 100)
            color = item.get("color", ctx.theme.get_accent_color(i))
            icon = item.get("icon")
            unit = item.get("unit", "")
            precision = _coerce_precision(item.get("precision", self.precision), self.precision)

            percent = min(100, (value / target) * 100) if target > 0 else 0
            value_text = f"{_format_fixed(value, precision)}/{_format_fixed(target, precision)}"
            if unit:
                value_text += f" {unit}"

            # Top row: Icon + Label + Spacer + Value
            top_row_children = []
            if icon:
                top_row_children.append(Icon(name=icon, size=icon_size, color=color))
            top_row_children.extend(
                [
                    Text(
                        text=label.upper(), font="tiny", color=THEME_TEXT_SECONDARY, align="start"
                    ),
                    Spacer(),
                    Text(text=value_text, font="tiny", color=THEME_TEXT_PRIMARY, align="end"),
                ]
            )

            # Bottom row: Bar + Percent
            bottom_row_children = [
                Bar(percent=percent, color=color, background=COLOR_DARK_GRAY, height=bar_height),
                Text(text=f"{percent:.0f}%", font="tiny", color=THEME_TEXT_PRIMARY, align="end"),
            ]

            # Combine into a column for this item
            item_column = Column(
                children=[
                    Row(children=top_row_children, gap=4, align="center", padding=padding),
                    Row(children=bottom_row_children, gap=8, align="center", padding=padding),
                ],
                gap=int(row_height * 0.15),
                justify="center",
                align="stretch",  # Stretch rows to full width for Spacer to work
            )
            children.append(item_column)

        # Render the entire column
        Column(
            children=children,
            gap=int(height * 0.02),
            justify="start",
            align="stretch",  # Stretch to full width
            padding=0,
        ).render(ctx, x, y, width, height)


class MultiProgressWidget(Widget):
    """Widget that displays multiple progress items."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the multi-progress widget."""
        super().__init__(config)
        self.items = config.options.get("items", [])
        self.title = config.options.get("title")
        self.precision = _coerce_precision(config.options.get("precision", 0), default=0)

    def get_entities(self) -> list[str]:
        """Return list of entity IDs."""
        entities: list[str] = []
        for item in self.items:
            entity_id = _normalize_entity_id(item.get("entity_id"))
            if entity_id and entity_id not in entities:
                entities.append(entity_id)
            target_entity = _normalize_entity_id(item.get("target_entity"))
            if target_entity and target_entity not in entities:
                entities.append(target_entity)
        return entities

    def _resolve_item_target(
        self,
        state: WidgetState,
        target_entity_id: str | None,
        fallback: float,
        template_value: object | None = None,
    ) -> float:
        """Resolve item target from template/entity/static options."""
        parsed_template = _parse_float(template_value)
        if parsed_template is not None:
            return parsed_template

        if not target_entity_id:
            return fallback
        target_entity = state.get_entity(target_entity_id)
        if target_entity is None:
            return fallback
        parsed = _parse_float(target_entity.state)
        if parsed is None:
            return fallback
        return parsed

    def _get_resolved_item_values(self, state: WidgetState, index: int) -> dict[str, Any]:
        """Get resolved template values for a multi-progress item by index."""
        resolved_items = state.get_resolved_option("items")
        if not isinstance(resolved_items, list):
            return {}
        if index < 0 or index >= len(resolved_items):
            return {}
        resolved_item = resolved_items[index]
        if not isinstance(resolved_item, dict):
            return {}
        return resolved_item

    def render(self, ctx: RenderContext, state: WidgetState) -> Component:
        """Render the multi-progress widget."""
        resolved_title_present = "title" in state.resolved_options
        resolved_title = state.get_resolved_option("title")
        display_title = (
            ("" if resolved_title is None else str(resolved_title))
            if resolved_title_present
            else self.title
        )

        display_items = []
        for i, item in enumerate(self.items):
            resolved_item = self._get_resolved_item_values(state, i)

            entity_id = _normalize_entity_id(item.get("entity_id"))
            entity = state.get_entity(entity_id) if entity_id else None
            value = _extract_numeric(entity)
            static_target = _coerce_float(item.get("target", 100), 100.0)
            target_entity = _normalize_entity_id(item.get("target_entity"))
            target = self._resolve_item_target(
                state,
                target_entity,
                static_target,
                resolved_item.get("target"),
            )

            if "label" in resolved_item:
                resolved_label = resolved_item.get("label")
                label = "" if resolved_label is None else str(resolved_label)
            else:
                label = item.get("label", "")
                if entity and not label:
                    label = entity.friendly_name
                label = label or entity_id or "Item"

            unit = item.get("unit", "")
            if entity and not unit:
                unit = entity.unit or ""

            display_items.append(
                {
                    "label": label,
                    "value": value,
                    "target": target,
                    "color": item.get("color", ctx.theme.get_accent_color(i)),
                    "icon": item.get("icon"),
                    "unit": unit,
                    "precision": self.precision,
                }
            )

        return MultiProgressDisplay(
            items=display_items,
            title=display_title,
            precision=self.precision,
        )
