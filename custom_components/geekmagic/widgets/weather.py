"""Weather widget for GeekMagic displays."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from ..const import (
    COLOR_CYAN,
    COLOR_GOLD,
    COLOR_GRAY,
    COLOR_WHITE,
)
from .base import Widget, WidgetConfig
from .components import Component

if TYPE_CHECKING:
    from ..render_context import RenderContext
    from .state import WidgetState


WEATHER_ICONS = {
    "sunny": "weather-sunny",
    "clear-night": "weather-night",
    "partlycloudy": "weather-partly-cloudy",
    "cloudy": "weather-cloudy",
    "rainy": "weather-rainy",
    "pouring": "weather-pouring",
    "snowy": "weather-snowy",
    "snowy-rainy": "weather-snowy-rainy",
    "fog": "weather-fog",
    "hail": "weather-hail",
    "windy": "weather-windy",
    "windy-variant": "weather-windy-variant",
    "lightning": "weather-lightning",
    "lightning-rainy": "weather-lightning-rainy",
    "exceptional": "alert-circle",
}


@dataclass
class WeatherDisplay(Component):
    """Weather display component."""

    temperature: Any = "--"
    humidity: Any = "--"
    condition: str = "sunny"
    forecast: list[dict] = field(default_factory=list)
    show_forecast: bool = True
    show_humidity: bool = True
    show_high_low: bool = True
    forecast_days: int = 3

    def measure(self, ctx: RenderContext, max_width: int, max_height: int) -> tuple[int, int]:
        return (max_width, max_height)

    def render(self, ctx: RenderContext, x: int, y: int, width: int, height: int) -> None:
        """Render weather."""
        padding = int(width * 0.04)
        icon_name = WEATHER_ICONS.get(self.condition, "weather-sunny")

        if height > 120 and self.show_forecast:
            self._render_full(ctx, x, y, width, height, icon_name, padding)
        else:
            self._render_compact(ctx, x, y, width, height, icon_name, padding)

    def _render_full(
        self,
        ctx: RenderContext,
        x: int,
        y: int,
        width: int,
        height: int,
        icon_name: str,
        padding: int,
    ) -> None:
        """Render full weather with forecast."""
        center_x = x + width // 2
        font_temp = ctx.get_font("xlarge")
        font_condition = ctx.get_font("small")
        font_tiny = ctx.get_font("tiny")

        current_y = y + padding

        icon_size = max(24, int(height * 0.25))
        ctx.draw_icon(
            icon_name, (center_x - icon_size // 2, current_y), size=icon_size, color=COLOR_GOLD
        )

        temp_str = f"{self.temperature}°" if self.temperature != "--" else "--"
        ctx.draw_text(
            temp_str,
            (center_x, current_y + icon_size + int(height * 0.08)),
            font=font_temp,
            color=COLOR_WHITE,
            anchor="mm",
        )

        ctx.draw_text(
            self.condition.replace("-", " ").title(),
            (center_x, current_y + icon_size + int(height * 0.22)),
            font=font_condition,
            color=COLOR_GRAY,
            anchor="mm",
        )

        if self.show_humidity:
            humidity_icon_size = max(8, int(height * 0.07))
            humidity_y = current_y + icon_size + int(height * 0.30)
            ctx.draw_icon(
                "water-percent",
                (x + padding, humidity_y),
                size=humidity_icon_size,
                color=COLOR_CYAN,
            )
            ctx.draw_text(
                f"{self.humidity}%",
                (x + padding + humidity_icon_size + 4, humidity_y + humidity_icon_size // 2),
                font=font_tiny,
                color=COLOR_CYAN,
                anchor="lm",
            )

        if self.forecast and self.show_forecast:
            forecast_y = y + height - int(height * 0.28)
            forecast_items = self.forecast[: self.forecast_days]
            if forecast_items:
                item_width = (width - padding * 2) // len(forecast_items)
                forecast_icon_size = max(10, int(height * 0.10))

                for i, day in enumerate(forecast_items):
                    fx = x + padding + i * item_width + item_width // 2
                    day_condition = day.get("condition", "sunny")
                    day_temp = day.get("temperature", "--")
                    day_temp_low = day.get("templow")
                    day_name = day.get("datetime", "")[:3] if day.get("datetime") else f"D{i + 1}"

                    ctx.draw_text(
                        day_name.upper(),
                        (fx, forecast_y),
                        font=font_tiny,
                        color=COLOR_GRAY,
                        anchor="mm",
                    )

                    day_icon = WEATHER_ICONS.get(day_condition, "weather-sunny")
                    ctx.draw_icon(
                        day_icon,
                        (fx - forecast_icon_size // 2, forecast_y + int(height * 0.05)),
                        size=forecast_icon_size,
                        color=COLOR_GRAY,
                    )

                    if self.show_high_low and day_temp_low is not None:
                        temp_str = f"{day_temp}°/{day_temp_low}°"
                    else:
                        temp_str = f"{day_temp}°"
                    ctx.draw_text(
                        temp_str,
                        (fx, forecast_y + int(height * 0.20)),
                        font=font_tiny,
                        color=COLOR_WHITE,
                        anchor="mm",
                    )

    def _render_compact(
        self,
        ctx: RenderContext,
        x: int,
        y: int,
        width: int,
        height: int,
        icon_name: str,
        padding: int,
    ) -> None:
        """Render compact weather."""
        center_y = y + height // 2
        font_temp = ctx.get_font("large")
        font_tiny = ctx.get_font("tiny")

        icon_size = max(16, min(32, int(height * 0.40)))
        ctx.draw_icon(
            icon_name, (x + padding, center_y - icon_size // 2), size=icon_size, color=COLOR_GOLD
        )

        temp_str = f"{self.temperature}°" if self.temperature != "--" else "--"
        ctx.draw_text(
            temp_str,
            (x + width - padding, center_y - int(height * 0.04)),
            font=font_temp,
            color=COLOR_WHITE,
            anchor="rm",
        )

        if self.show_humidity:
            ctx.draw_text(
                f"{self.humidity}%",
                (x + width - padding, center_y + int(height * 0.15)),
                font=font_tiny,
                color=COLOR_CYAN,
                anchor="rm",
            )


def WeatherPlaceholder() -> Component:
    """Create placeholder component when no weather data."""
    from .components import Column, Icon, Text

    return Column(
        children=[
            Icon("weather-cloudy", color=COLOR_GRAY, max_size=48),
            Text("No Weather Data", font="small", color=COLOR_GRAY),
        ],
        gap=8,
        align="center",
        justify="center",
    )


class WeatherWidget(Widget):
    """Widget that displays weather information."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the weather widget."""
        super().__init__(config)
        self.show_forecast = config.options.get("show_forecast", True)
        self.forecast_days = config.options.get("forecast_days", 3)
        self.show_humidity = config.options.get("show_humidity", True)
        self.show_wind = config.options.get("show_wind", False)
        self.show_high_low = config.options.get("show_high_low", True)

    def render(self, ctx: RenderContext, state: WidgetState) -> Component:
        """Render the weather widget."""
        entity = state.entity

        if entity is None:
            return WeatherPlaceholder()

        return WeatherDisplay(
            temperature=entity.get("temperature", "--"),
            humidity=entity.get("humidity", "--"),
            condition=entity.state,
            forecast=entity.get("forecast", []),
            show_forecast=self.show_forecast,
            show_humidity=self.show_humidity,
            show_high_low=self.show_high_low,
            forecast_days=self.forecast_days,
        )
