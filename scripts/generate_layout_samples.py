#!/usr/bin/env python3
"""Generate layout sample images showing each layout type."""

from __future__ import annotations

import random
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from PIL import Image

from custom_components.geekmagic.widgets.state import EntityState, WidgetState

if TYPE_CHECKING:
    from custom_components.geekmagic.layouts.base import Layout
    from scripts.mock_hass import MockHass

from custom_components.geekmagic.const import (
    COLOR_CYAN,
    COLOR_GOLD,
    COLOR_LIME,
    COLOR_ORANGE,
    COLOR_PURPLE,
    COLOR_RED,
    COLOR_TEAL,
    COLOR_WHITE,
)
from custom_components.geekmagic.layouts.grid import Grid2x2, Grid2x3, Grid3x2, Grid3x3
from custom_components.geekmagic.layouts.hero import HeroLayout
from custom_components.geekmagic.layouts.split import (
    SplitHorizontal,
    SplitVertical,
    ThreeColumnLayout,
)
from custom_components.geekmagic.renderer import Renderer
from custom_components.geekmagic.widgets import (
    ChartWidget,
    ClockWidget,
    EntityWidget,
    GaugeWidget,
    ProgressWidget,
    StatusListWidget,
    StatusWidget,
    WeatherWidget,
    WidgetConfig,
)
from custom_components.geekmagic.widgets.theme import THEMES
from scripts.mock_hass import MockHass


def build_widget_states(
    layout: Layout,
    hass: MockHass,
    chart_history: dict[int, list[float]] | None = None,
) -> dict[int, WidgetState]:
    """Build WidgetState dict for all widgets in a layout."""
    widget_states: dict[int, WidgetState] = {}
    chart_history = chart_history or {}

    for slot in layout.slots:
        if slot.widget is None:
            continue

        widget = slot.widget
        entity_id = widget.config.entity_id
        entity: EntityState | None = None
        if entity_id:
            state = hass.states.get(entity_id)
            if state:
                entity = EntityState(
                    entity_id=entity_id,
                    state=state.state,
                    attributes=state.attributes,
                )

        entities: dict[str, EntityState] = {}
        try:
            entity_ids = widget.get_entities()
            for eid in entity_ids:
                if eid and eid != entity_id:
                    state = hass.states.get(eid)
                    if state:
                        entities[eid] = EntityState(
                            entity_id=eid,
                            state=state.state,
                            attributes=state.attributes,
                        )
        except AttributeError:
            pass

        history: list[float] = chart_history.get(slot.index, [])

        widget_states[slot.index] = WidgetState(
            entity=entity,
            entities=entities,
            history=history,
            image=None,
            now=datetime.now(tz=UTC),
        )

    return widget_states


def save_layout(renderer: Renderer, img: Image.Image, name: str, output_dir: Path) -> None:
    """Save layout image."""
    final = renderer.finalize(img)
    output_path = output_dir / f"layout_{name}.png"
    final.save(output_path)
    print(f"Generated: {output_path}")


def create_mock_hass() -> MockHass:
    """Create mock hass with common entities."""
    hass = MockHass()
    # Sensors
    hass.states.set("sensor.temp", "23", {"unit_of_measurement": "°C", "friendly_name": "Temp"})
    hass.states.set(
        "sensor.humidity", "58", {"unit_of_measurement": "%", "friendly_name": "Humidity"}
    )
    hass.states.set("sensor.cpu", "42", {"unit_of_measurement": "%", "friendly_name": "CPU"})
    hass.states.set("sensor.memory", "68", {"unit_of_measurement": "%", "friendly_name": "Memory"})
    hass.states.set("sensor.disk", "55", {"unit_of_measurement": "%", "friendly_name": "Disk"})
    hass.states.set(
        "sensor.network", "85", {"unit_of_measurement": "Mb/s", "friendly_name": "Network"}
    )
    hass.states.set("sensor.power", "2.4", {"unit_of_measurement": "kW", "friendly_name": "Power"})
    hass.states.set("sensor.solar", "3.2", {"unit_of_measurement": "kW", "friendly_name": "Solar"})
    hass.states.set(
        "sensor.battery", "87", {"unit_of_measurement": "%", "friendly_name": "Battery"}
    )
    # Weather
    hass.states.set(
        "weather.home",
        "sunny",
        {
            "temperature": 24,
            "humidity": 45,
            "friendly_name": "Weather",
            "forecast": [
                {"datetime": "Mon", "condition": "sunny", "temperature": 26},
                {"datetime": "Tue", "condition": "cloudy", "temperature": 22},
                {"datetime": "Wed", "condition": "rainy", "temperature": 18},
            ],
        },
    )
    # Devices
    hass.states.set("device_tracker.phone", "home", {"friendly_name": "Phone"})
    hass.states.set("device_tracker.laptop", "home", {"friendly_name": "Laptop"})
    hass.states.set("device_tracker.tablet", "not_home", {"friendly_name": "Tablet"})
    hass.states.set("device_tracker.watch", "home", {"friendly_name": "Watch"})
    return hass


def generate_grid_2x2(renderer: Renderer, output_dir: Path) -> None:
    """Generate Grid 2x2 layout sample - Home Overview."""
    hass = create_mock_hass()
    # Add more states for this sample
    hass.states.set(
        "climate.living_room",
        "heat",
        {"temperature": 22, "current_temperature": 21, "friendly_name": "Living Room"},
    )
    hass.states.set("light.living_room", "on", {"brightness": 200, "friendly_name": "Lights"})

    layout = Grid2x2(padding=8, gap=8)
    img, draw = renderer.create_canvas()

    # Mixed widgets: Clock, Temperature, Weather, Lights
    widgets = [
        ClockWidget(
            WidgetConfig(
                widget_type="clock",
                slot=0,
                color=COLOR_WHITE,
                options={"show_date": True},
            )
        ),
        GaugeWidget(
            WidgetConfig(
                widget_type="gauge",
                slot=1,
                entity_id="sensor.temp",
                label="Inside",
                color=COLOR_ORANGE,
                options={"style": "arc", "min": 15, "max": 30},
            )
        ),
        WeatherWidget(
            WidgetConfig(
                widget_type="weather",
                slot=2,
                entity_id="weather.home",
                options={"show_forecast": False},
            )
        ),
        EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=3,
                entity_id="light.living_room",
                label="Lights",
                color=COLOR_GOLD,
                options={"icon": "lightbulb", "show_panel": True},
            )
        ),
    ]
    for i, w in enumerate(widgets):
        layout.set_widget(i, w)

    layout.render(renderer, draw, build_widget_states(layout, hass))
    save_layout(renderer, img, "grid_2x2", output_dir)


def generate_grid_2x3(renderer: Renderer, output_dir: Path) -> None:
    """Generate Grid 2x3 layout sample - Smart Home Dashboard."""
    hass = create_mock_hass()
    # Add smart home entities
    hass.states.set("light.bedroom", "off", {"friendly_name": "Bedroom"})
    hass.states.set("light.kitchen", "on", {"brightness": 255, "friendly_name": "Kitchen"})
    hass.states.set("lock.front_door", "locked", {"friendly_name": "Front Door"})
    hass.states.set(
        "binary_sensor.motion", "off", {"friendly_name": "Motion", "device_class": "motion"}
    )

    layout = Grid2x3(padding=8, gap=8)
    img, draw = renderer.create_canvas()

    # Smart home mix: Lights, Climate, Security
    widgets = [
        EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=0,
                entity_id="light.kitchen",
                label="Kitchen",
                color=COLOR_GOLD,
                options={"icon": "lightbulb", "show_panel": True},
            )
        ),
        EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=1,
                entity_id="light.bedroom",
                label="Bedroom",
                color=COLOR_PURPLE,
                options={"icon": "lightbulb-outline", "show_panel": True},
            )
        ),
        EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=2,
                entity_id="sensor.temp",
                label="Temp",
                color=COLOR_ORANGE,
                options={"icon": "thermometer", "show_panel": True},
            )
        ),
        EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=3,
                entity_id="sensor.humidity",
                label="Humidity",
                color=COLOR_CYAN,
                options={"icon": "water-percent", "show_panel": True},
            )
        ),
        EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=4,
                entity_id="lock.front_door",
                label="Door",
                color=COLOR_LIME,
                options={"icon": "lock", "show_panel": True},
            )
        ),
        StatusWidget(
            WidgetConfig(
                widget_type="status",
                slot=5,
                entity_id="binary_sensor.motion",
                label="Motion",
                options={"icon": "motion-sensor"},
            )
        ),
    ]
    for i, w in enumerate(widgets):
        layout.set_widget(i, w)

    layout.render(renderer, draw, build_widget_states(layout, hass))
    save_layout(renderer, img, "grid_2x3", output_dir)


def generate_grid_3x2(renderer: Renderer, output_dir: Path) -> None:
    """Generate Grid 3x2 layout sample - Energy Monitor."""
    hass = create_mock_hass()
    # Add energy entities
    hass.states.set(
        "sensor.grid_import",
        "1.2",
        {"unit_of_measurement": "kW", "friendly_name": "Grid Import"},
    )
    hass.states.set(
        "sensor.grid_export",
        "0.5",
        {"unit_of_measurement": "kW", "friendly_name": "Grid Export"},
    )
    hass.states.set(
        "sensor.home_battery",
        "75",
        {"unit_of_measurement": "%", "friendly_name": "Home Battery"},
    )

    layout = Grid3x2(padding=8, gap=8)
    img, draw = renderer.create_canvas()

    # Energy monitoring: Solar, Battery, Grid, Power usage
    widgets = [
        GaugeWidget(
            WidgetConfig(
                widget_type="gauge",
                slot=0,
                entity_id="sensor.solar",
                label="Solar",
                color=COLOR_GOLD,
                options={"style": "arc", "icon": "solar-power", "max": 5},
            )
        ),
        GaugeWidget(
            WidgetConfig(
                widget_type="gauge",
                slot=1,
                entity_id="sensor.home_battery",
                label="Battery",
                color=COLOR_LIME,
                options={"style": "ring", "icon": "battery-high"},
            )
        ),
        EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=2,
                entity_id="sensor.power",
                label="Using",
                color=COLOR_ORANGE,
                options={"icon": "flash", "show_panel": True},
            )
        ),
        EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=3,
                entity_id="sensor.grid_import",
                label="Import",
                color=COLOR_RED,
                options={"icon": "transmission-tower-import", "show_panel": True},
            )
        ),
        EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=4,
                entity_id="sensor.grid_export",
                label="Export",
                color=COLOR_TEAL,
                options={"icon": "transmission-tower-export", "show_panel": True},
            )
        ),
    ]
    # Add chart for slot 5
    chart = ChartWidget(
        WidgetConfig(
            widget_type="chart",
            slot=5,
            entity_id="sensor.power",
            label="History",
            color=COLOR_CYAN,
        )
    )
    rng = random.Random(100)  # noqa: S311
    chart_history: dict[int, list[float]] = {
        5: [1.5 + rng.uniform(-0.5, 1.5) for _ in range(24)],
    }
    widgets.append(chart)

    for i, w in enumerate(widgets):
        layout.set_widget(i, w)

    layout.render(renderer, draw, build_widget_states(layout, hass, chart_history))
    save_layout(renderer, img, "grid_3x2", output_dir)


def generate_grid_3x3(renderer: Renderer, output_dir: Path) -> None:
    """Generate Grid 3x3 layout sample."""
    hass = create_mock_hass()
    # Add more sensors for 9 slots
    hass.states.set("sensor.s1", "21", {"unit_of_measurement": "°C", "friendly_name": "Living"})
    hass.states.set("sensor.s2", "19", {"unit_of_measurement": "°C", "friendly_name": "Bedroom"})
    hass.states.set("sensor.s3", "23", {"unit_of_measurement": "°C", "friendly_name": "Kitchen"})
    hass.states.set("sensor.s4", "22", {"unit_of_measurement": "°C", "friendly_name": "Office"})
    hass.states.set("sensor.s5", "20", {"unit_of_measurement": "°C", "friendly_name": "Bath"})
    hass.states.set("sensor.s6", "18", {"unit_of_measurement": "°C", "friendly_name": "Garage"})
    hass.states.set("sensor.s7", "24", {"unit_of_measurement": "°C", "friendly_name": "Attic"})
    hass.states.set("sensor.s8", "17", {"unit_of_measurement": "°C", "friendly_name": "Basement"})
    hass.states.set("sensor.s9", "22", {"unit_of_measurement": "°C", "friendly_name": "Patio"})

    layout = Grid3x3(padding=6, gap=6)
    img, draw = renderer.create_canvas()

    colors = [
        COLOR_ORANGE,
        COLOR_CYAN,
        COLOR_TEAL,
        COLOR_PURPLE,
        COLOR_GOLD,
        COLOR_LIME,
        COLOR_RED,
        COLOR_WHITE,
        COLOR_ORANGE,
    ]
    for i in range(9):
        widget = EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=i,
                entity_id=f"sensor.s{i + 1}",
                color=colors[i],
                options={"show_name": True},
            )
        )
        layout.set_widget(i, widget)

    layout.render(renderer, draw, build_widget_states(layout, hass))
    save_layout(renderer, img, "grid_3x3", output_dir)


def generate_hero(renderer: Renderer, output_dir: Path) -> None:
    """Generate Hero layout sample."""
    hass = create_mock_hass()
    layout = HeroLayout(footer_slots=3, hero_ratio=0.7, padding=8, gap=8)
    img, draw = renderer.create_canvas()

    # Weather as hero
    weather = WeatherWidget(
        WidgetConfig(
            widget_type="weather",
            slot=0,
            entity_id="weather.home",
            options={"show_forecast": True, "forecast_days": 3},
        )
    )
    layout.set_widget(0, weather)

    # Footer entities
    footer_configs = [
        ("sensor.temp", "Inside", COLOR_ORANGE),
        ("sensor.humidity", "Humidity", COLOR_CYAN),
        ("sensor.power", "Power", COLOR_GOLD),
    ]
    for i, (entity_id, label, color) in enumerate(footer_configs):
        widget = EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=i + 1,
                entity_id=entity_id,
                label=label,
                color=color,
                options={"show_unit": False},
            )
        )
        layout.set_widget(i + 1, widget)

    layout.render(renderer, draw, build_widget_states(layout, hass))
    save_layout(renderer, img, "hero", output_dir)


def generate_split_horizontal(renderer: Renderer, output_dir: Path) -> None:
    """Generate Split Horizontal layout sample (side by side)."""
    hass = create_mock_hass()
    layout = SplitHorizontal(ratio=0.5, padding=8, gap=8)
    img, draw = renderer.create_canvas()

    # Clock on left
    clock = ClockWidget(
        WidgetConfig(widget_type="clock", slot=0, color=COLOR_WHITE, options={"show_date": True})
    )
    layout.set_widget(0, clock)

    # Gauge on right
    gauge = GaugeWidget(
        WidgetConfig(
            widget_type="gauge",
            slot=1,
            entity_id="sensor.cpu",
            label="CPU",
            color=COLOR_TEAL,
            options={"style": "ring"},
        )
    )
    layout.set_widget(1, gauge)

    layout.render(renderer, draw, build_widget_states(layout, hass))
    save_layout(renderer, img, "split_horizontal", output_dir)


def generate_split_vertical(renderer: Renderer, output_dir: Path) -> None:
    """Generate Split Vertical layout sample (stacked)."""
    hass = create_mock_hass()
    layout = SplitVertical(ratio=0.5, padding=8, gap=8)
    img, draw = renderer.create_canvas()

    # Clock on top
    clock = ClockWidget(
        WidgetConfig(widget_type="clock", slot=0, color=COLOR_WHITE, options={"show_date": True})
    )
    layout.set_widget(0, clock)

    # Status list on bottom
    status = StatusListWidget(
        WidgetConfig(
            widget_type="status_list",
            slot=1,
            options={
                "title": "Devices",
                "entities": [
                    ("device_tracker.phone", "Phone"),
                    ("device_tracker.laptop", "Laptop"),
                    ("device_tracker.tablet", "Tablet"),
                    ("device_tracker.watch", "Watch"),
                ],
                "on_color": COLOR_LIME,
                "off_color": COLOR_RED,
            },
        )
    )
    layout.set_widget(1, status)

    layout.render(renderer, draw, build_widget_states(layout, hass))
    save_layout(renderer, img, "split_vertical", output_dir)


def generate_three_column(renderer: Renderer, output_dir: Path) -> None:
    """Generate Three Column layout sample - Fitness Tracker."""
    hass = create_mock_hass()
    # Add fitness entities
    hass.states.set(
        "sensor.steps", "8542", {"unit_of_measurement": "steps", "friendly_name": "Steps"}
    )
    hass.states.set(
        "sensor.calories", "420", {"unit_of_measurement": "kcal", "friendly_name": "Calories"}
    )
    hass.states.set(
        "sensor.heart_rate", "72", {"unit_of_measurement": "bpm", "friendly_name": "Heart Rate"}
    )

    layout = ThreeColumnLayout(ratios=(0.33, 0.34, 0.33), padding=8, gap=8)
    img, draw = renderer.create_canvas()

    # Fitness: Steps, Calories, Heart Rate
    widgets = [
        ProgressWidget(
            WidgetConfig(
                widget_type="progress",
                slot=0,
                entity_id="sensor.steps",
                label="Steps",
                color=COLOR_LIME,
                options={"target": 10000, "icon": "walk"},
            )
        ),
        ProgressWidget(
            WidgetConfig(
                widget_type="progress",
                slot=1,
                entity_id="sensor.calories",
                label="Cals",
                color=COLOR_ORANGE,
                options={"target": 600, "icon": "fire"},
            )
        ),
        EntityWidget(
            WidgetConfig(
                widget_type="entity",
                slot=2,
                entity_id="sensor.heart_rate",
                label="BPM",
                color=COLOR_RED,
                options={"icon": "heart-pulse", "show_panel": True},
            )
        ),
    ]
    for i, w in enumerate(widgets):
        layout.set_widget(i, w)

    layout.render(renderer, draw, build_widget_states(layout, hass))
    save_layout(renderer, img, "three_column", output_dir)


def generate_theme_samples(renderer: Renderer, output_dir: Path) -> None:
    """Generate sample images for each theme with varied widgets."""
    hass = create_mock_hass()

    # Add chart data for chart widgets
    hass.states.set(
        "sensor.temperature",
        "23",
        {"unit_of_measurement": "°C", "friendly_name": "Temperature"},
    )

    # Define unique widget configurations for each theme
    theme_configs: dict[str, list] = {
        # Classic: Gauge rings + chart (system monitoring feel)
        "classic": [
            ("gauge", "sensor.cpu", "CPU", {"style": "ring"}),
            ("gauge", "sensor.memory", "Memory", {"style": "ring"}),
            ("chart", "sensor.temperature", "Temp", {"hours": 24}),
            ("gauge", "sensor.disk", "Disk", {"style": "bar"}),
        ],
        # Minimal: Clean entities + status
        "minimal": [
            ("entity", "sensor.temp", "Temp", {}),
            ("entity", "sensor.humidity", "Humidity", {}),
            ("status", "device_tracker.phone", "Phone", {}),
            ("entity", "sensor.power", "Power", {}),
        ],
        # Neon: Gauges with glow effect
        "neon": [
            ("gauge", "sensor.cpu", "CPU", {"style": "arc"}),
            ("gauge", "sensor.memory", "MEM", {"style": "arc"}),
            ("chart", "sensor.temperature", "Temp", {"hours": 12}),
            ("gauge", "sensor.battery", "BAT", {"style": "ring"}),
        ],
        # Retro: Terminal-style with bars
        "retro": [
            ("gauge", "sensor.cpu", "CPU", {"style": "bar"}),
            ("gauge", "sensor.memory", "MEM", {"style": "bar"}),
            ("gauge", "sensor.disk", "DSK", {"style": "bar"}),
            ("gauge", "sensor.network", "NET", {"style": "bar"}),
        ],
        # Soft: Gentle progress + entities
        "soft": [
            ("entity", "sensor.temp", "Inside", {}),
            ("progress", "sensor.battery", "Battery", {"goal": 100}),
            ("chart", "sensor.temperature", "Trend", {"hours": 24}),
            ("entity", "sensor.humidity", "Humidity", {}),
        ],
        # Light: Clean gauges for daytime use
        "light": [
            ("gauge", "sensor.cpu", "CPU", {"style": "ring"}),
            ("gauge", "sensor.memory", "Memory", {"style": "ring"}),
            ("entity", "sensor.temp", "Temp", {}),
            ("progress", "sensor.disk", "Disk", {"goal": 100}),
        ],
        # Ocean: Water/nautical themed
        "ocean": [
            ("gauge", "sensor.humidity", "Humidity", {"style": "arc"}),
            ("chart", "sensor.temperature", "Temp", {"hours": 24}),
            ("entity", "sensor.temp", "Inside", {}),
            ("gauge", "sensor.battery", "Battery", {"style": "ring"}),
        ],
        # Sunset: Warm energy monitoring
        "sunset": [
            ("gauge", "sensor.power", "Power", {"style": "arc"}),
            ("gauge", "sensor.solar", "Solar", {"style": "arc"}),
            ("chart", "sensor.temperature", "Temp", {"hours": 12}),
            ("entity", "sensor.battery", "Battery", {}),
        ],
        # Forest: Nature/eco themed
        "forest": [
            ("entity", "sensor.temp", "Outdoor", {}),
            ("gauge", "sensor.humidity", "Humidity", {"style": "bar"}),
            ("chart", "sensor.temperature", "Climate", {"hours": 24}),
            ("progress", "sensor.solar", "Solar", {"goal": 5}),
        ],
        # Candy: Playful and fun
        "candy": [
            ("gauge", "sensor.battery", "Battery", {"style": "ring"}),
            ("entity", "sensor.temp", "Temp", {}),
            ("progress", "sensor.cpu", "CPU", {"goal": 100}),
            ("chart", "sensor.temperature", "Trend", {"hours": 12}),
        ],
    }

    for theme_name, theme in THEMES.items():
        layout = Grid2x2(padding=8, gap=8)
        layout.theme = theme

        accent_colors = theme.accent_colors
        configs = theme_configs.get(theme_name, theme_configs["classic"])

        chart_history: dict[int, list[float]] = {}

        for i, (widget_type, entity_id, label, options) in enumerate(configs):
            color = accent_colors[i % len(accent_colors)]

            if widget_type == "gauge":
                widget = GaugeWidget(
                    WidgetConfig(
                        widget_type="gauge",
                        slot=i,
                        entity_id=entity_id,
                        label=label,
                        color=color,
                        options=options,
                    )
                )
            elif widget_type == "entity":
                widget = EntityWidget(
                    WidgetConfig(
                        widget_type="entity",
                        slot=i,
                        entity_id=entity_id,
                        label=label,
                        color=color,
                        options={"show_panel": True, **options},
                    )
                )
            elif widget_type == "chart":
                widget = ChartWidget(
                    WidgetConfig(
                        widget_type="chart",
                        slot=i,
                        entity_id=entity_id,
                        label=label,
                        color=color,
                        options=options,
                    )
                )
                # Store chart history for later use
                rng = random.Random(42 + i)  # noqa: S311
                base_temp = 20
                chart_history[i] = [base_temp + rng.uniform(-3, 5) for _ in range(48)]
            elif widget_type == "progress":
                widget = ProgressWidget(
                    WidgetConfig(
                        widget_type="progress",
                        slot=i,
                        entity_id=entity_id,
                        label=label,
                        color=color,
                        options=options,
                    )
                )
            elif widget_type == "status":
                widget = StatusWidget(
                    WidgetConfig(
                        widget_type="status",
                        slot=i,
                        entity_id=entity_id,
                        label=label,
                        color=color,
                        options={"on_color": theme.success, "off_color": theme.error},
                    )
                )
            else:
                continue

            layout.set_widget(i, widget)

        img, draw = renderer.create_canvas(background=theme.background)
        layout.render(renderer, draw, build_widget_states(layout, hass, chart_history))
        save_layout(renderer, img, f"theme_{theme_name}", output_dir)


def main() -> None:
    """Generate all layout sample images."""
    output_dir = Path(__file__).parent.parent / "samples" / "layouts"
    output_dir.mkdir(parents=True, exist_ok=True)

    renderer = Renderer()

    print("Generating layout samples...")
    print()

    generate_grid_2x2(renderer, output_dir)
    generate_grid_2x3(renderer, output_dir)
    generate_grid_3x2(renderer, output_dir)
    generate_grid_3x3(renderer, output_dir)
    generate_hero(renderer, output_dir)
    generate_split_vertical(renderer, output_dir)
    generate_split_horizontal(renderer, output_dir)
    generate_three_column(renderer, output_dir)

    print()
    print("Generating theme samples...")
    print()
    generate_theme_samples(renderer, output_dir)

    print()
    print(f"Done! Generated 8 layout samples + {len(THEMES)} theme samples in {output_dir}")


if __name__ == "__main__":
    main()
