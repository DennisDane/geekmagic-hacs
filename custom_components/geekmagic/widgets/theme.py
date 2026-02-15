"""Theme system for GeekMagic display.

Themes provide a complete design system affecting colors, typography,
spacing, shapes, borders, and visual effects.

Each theme defines:
- Background style (dark, light, colored)
- Design system colors (primary, secondary, success, warning, error)
- Shape styling (corner radius, borders)
- Typography (weights, emphasis)
- Special effects (glow, scanlines)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

# Type aliases
Color = tuple[int, int, int]
BorderStyle = Literal["none", "solid", "outline", "double"]
FontWeight = Literal["light", "regular"]


@dataclass(frozen=True)
class Theme:
    """Theme configuration affecting all visual aspects.

    Design System Colors:
        primary: Main accent color for key elements, values, highlights
        secondary: Supporting accent for less prominent elements
        success: Positive states (on, connected, complete)
        warning: Caution states (low battery, pending)
        error: Negative states (off, disconnected, failed)
        muted: Subtle elements, disabled states

    Surface Colors:
        background: Screen/canvas background
        surface: Widget/panel background
        surface_variant: Alternate surface (cards, elevated elements)
        border: Border/divider color

    Text Colors:
        text_primary: Main text (values, content)
        text_secondary: Secondary text (labels, descriptions)
        text_on_primary: Text on primary-colored backgrounds
    """

    name: str

    # Design system colors
    primary: Color = (27, 158, 119)
    secondary: Color = (117, 112, 179)
    success: Color = (102, 166, 30)
    warning: Color = (230, 171, 2)
    error: Color = (231, 76, 60)
    muted: Color = (100, 100, 100)

    # Surface colors
    background: Color = (0, 0, 0)
    surface: Color = (18, 18, 18)
    surface_variant: Color = (30, 30, 30)
    border: Color = (60, 60, 60)

    # Text colors
    text_primary: Color = (255, 255, 255)
    text_secondary: Color = (150, 150, 150)
    text_on_primary: Color = (255, 255, 255)

    # Accent color palette for widgets (cycles through for variety)
    accent_colors: tuple[Color, ...] = field(
        default_factory=lambda: (
            (27, 158, 119),  # Teal
            (217, 95, 2),  # Orange
            (117, 112, 179),  # Lavender
            (231, 41, 138),  # Magenta
            (102, 166, 30),  # Lime
            (230, 171, 2),  # Gold
        )
    )

    # Shape styling
    corner_radius: int = 8
    border_width: int = 0
    border_style: BorderStyle = "none"

    # Spacing
    layout_padding: int = 8
    widget_padding: int = 6  # Percentage of width
    gap: int = 6

    # Typography
    value_bold: bool = True
    label_weight: FontWeight = "regular"

    # Visual effects
    glow_effect: bool = False
    scanlines: bool = False
    invert_bars: bool = False

    # Progress/gauge bar styling
    bar_background: Color = (50, 50, 50)

    def get_accent_color(self, index: int) -> Color:
        """Get accent color for a slot index, cycling through available colors."""
        return self.accent_colors[index % len(self.accent_colors)]


# =============================================================================
# Pre-defined Themes - 17 unique themes
# =============================================================================

# 1. Classic - Balanced dark theme (default)
THEME_CLASSIC = Theme(
    name="classic",
    primary=(27, 158, 119),
    secondary=(117, 112, 179),
    success=(102, 166, 30),
    warning=(230, 171, 2),
    error=(231, 76, 60),
    muted=(100, 100, 100),
    background=(0, 0, 0),
    surface=(18, 18, 18),
    surface_variant=(28, 28, 28),
    border=(60, 60, 60),
    text_primary=(255, 255, 255),
    text_secondary=(150, 150, 150),
    text_on_primary=(255, 255, 255),
    accent_colors=(
        (27, 158, 119),  # Teal
        (217, 95, 2),  # Orange
        (117, 112, 179),  # Lavender
        (231, 41, 138),  # Magenta
        (102, 166, 30),  # Lime
        (230, 171, 2),  # Gold
    ),
    corner_radius=8,
    border_width=0,
    border_style="none",
    bar_background=(50, 50, 50),
)

# 2. Minimal - Sharp, clean, monochrome
THEME_MINIMAL = Theme(
    name="minimal",
    primary=(100, 200, 255),
    secondary=(180, 180, 180),
    success=(100, 200, 100),
    warning=(255, 200, 100),
    error=(255, 100, 100),
    muted=(80, 80, 80),
    background=(0, 0, 0),
    surface=(0, 0, 0),
    surface_variant=(15, 15, 15),
    border=(80, 80, 80),
    text_primary=(255, 255, 255),
    text_secondary=(120, 120, 120),
    text_on_primary=(0, 0, 0),
    accent_colors=(
        (100, 200, 255),  # Ice blue (single color for consistency)
    ),
    corner_radius=0,
    border_width=1,
    border_style="solid",
    layout_padding=4,
    widget_padding=4,
    gap=4,
    value_bold=False,
    label_weight="light",
    bar_background=(40, 40, 40),
)

# 3. Neon - Cyberpunk with glow effects
THEME_NEON = Theme(
    name="neon",
    primary=(0, 255, 255),
    secondary=(255, 0, 255),
    success=(0, 255, 128),
    warning=(255, 255, 0),
    error=(255, 50, 50),
    muted=(80, 80, 100),
    background=(5, 5, 15),
    surface=(10, 10, 20),
    surface_variant=(15, 15, 30),
    border=(0, 255, 255),
    text_primary=(255, 255, 255),
    text_secondary=(200, 200, 220),
    text_on_primary=(0, 0, 0),
    accent_colors=(
        (0, 255, 255),  # Cyan
        (255, 0, 255),  # Magenta
        (0, 255, 128),  # Neon green
        (255, 100, 200),  # Pink
        (100, 200, 255),  # Light blue
        (255, 255, 0),  # Yellow
    ),
    corner_radius=4,
    border_width=2,
    border_style="solid",
    glow_effect=True,
    bar_background=(20, 20, 40),
)

# 4. Retro - Terminal/CRT style
THEME_RETRO = Theme(
    name="retro",
    primary=(0, 255, 0),
    secondary=(255, 180, 0),
    success=(0, 255, 0),
    warning=(255, 180, 0),
    error=(255, 50, 0),
    muted=(0, 100, 0),
    background=(0, 8, 0),
    surface=(0, 0, 0),
    surface_variant=(0, 15, 0),
    border=(0, 180, 0),
    text_primary=(0, 255, 0),
    text_secondary=(0, 150, 0),
    text_on_primary=(0, 0, 0),
    accent_colors=(
        (0, 255, 0),  # Green
        (255, 180, 0),  # Amber
    ),
    corner_radius=0,
    border_width=1,
    border_style="outline",
    layout_padding=10,
    widget_padding=8,
    gap=8,
    scanlines=True,
    invert_bars=True,
    bar_background=(0, 40, 0),
)

# 5. Soft - Rounded, muted, cozy
THEME_SOFT = Theme(
    name="soft",
    primary=(120, 180, 220),
    secondary=(180, 140, 200),
    success=(140, 200, 160),
    warning=(220, 180, 140),
    error=(220, 140, 140),
    muted=(100, 100, 115),
    background=(15, 15, 20),
    surface=(30, 30, 40),
    surface_variant=(40, 40, 55),
    border=(50, 50, 65),
    text_primary=(240, 240, 245),
    text_secondary=(140, 140, 155),
    text_on_primary=(20, 20, 30),
    accent_colors=(
        (120, 180, 220),  # Soft blue
        (180, 140, 200),  # Soft purple
        (140, 200, 160),  # Soft green
        (220, 180, 140),  # Soft orange
        (200, 150, 180),  # Soft pink
        (180, 200, 140),  # Soft lime
    ),
    corner_radius=16,
    border_width=1,
    border_style="solid",
    layout_padding=10,
    widget_padding=8,
    gap=8,
    value_bold=False,
    bar_background=(45, 45, 60),
)

# 6. Light - Clean light theme with white backgrounds
THEME_LIGHT = Theme(
    name="light",
    primary=(0, 122, 204),
    secondary=(102, 45, 145),
    success=(40, 167, 69),
    warning=(255, 193, 7),
    error=(220, 53, 69),
    muted=(180, 180, 180),
    background=(255, 255, 255),
    surface=(255, 255, 255),
    surface_variant=(250, 250, 252),
    border=(230, 230, 235),
    text_primary=(30, 30, 35),
    text_secondary=(100, 100, 110),
    text_on_primary=(255, 255, 255),
    accent_colors=(
        (0, 122, 204),  # Blue
        (102, 45, 145),  # Purple
        (40, 167, 69),  # Green
        (255, 140, 0),  # Orange
        (220, 53, 69),  # Red
        (23, 162, 184),  # Teal
    ),
    corner_radius=12,
    border_width=0,  # No borders - clean look
    border_style="none",
    layout_padding=8,
    widget_padding=6,
    gap=6,
    bar_background=(235, 235, 240),
)

# 7. Ocean - Deep blue nautical theme
THEME_OCEAN = Theme(
    name="ocean",
    primary=(0, 180, 216),
    secondary=(72, 202, 228),
    success=(0, 200, 150),
    warning=(255, 200, 87),
    error=(255, 107, 107),
    muted=(70, 100, 120),
    background=(3, 37, 65),
    surface=(10, 50, 80),
    surface_variant=(15, 60, 95),
    border=(30, 90, 130),
    text_primary=(240, 248, 255),
    text_secondary=(150, 190, 210),
    text_on_primary=(0, 30, 50),
    accent_colors=(
        (0, 180, 216),  # Bright cyan
        (72, 202, 228),  # Light cyan
        (144, 224, 239),  # Pale cyan
        (0, 200, 150),  # Aqua
        (255, 200, 87),  # Sand
        (100, 150, 200),  # Steel blue
    ),
    corner_radius=10,
    border_width=1,
    border_style="solid",
    bar_background=(20, 60, 90),
)

# 8. Sunset - Warm gradient-inspired
THEME_SUNSET = Theme(
    name="sunset",
    primary=(255, 107, 107),
    secondary=(255, 159, 67),
    success=(106, 176, 76),
    warning=(255, 200, 87),
    error=(255, 71, 87),
    muted=(130, 100, 100),
    background=(30, 20, 25),
    surface=(45, 30, 35),
    surface_variant=(55, 38, 45),
    border=(80, 55, 60),
    text_primary=(255, 245, 238),
    text_secondary=(180, 150, 150),
    text_on_primary=(40, 20, 25),
    accent_colors=(
        (255, 107, 107),  # Coral
        (255, 159, 67),  # Orange
        (255, 200, 87),  # Gold
        (255, 140, 140),  # Pink
        (200, 120, 180),  # Mauve
        (255, 180, 120),  # Peach
    ),
    corner_radius=14,
    border_width=0,
    border_style="none",
    bar_background=(60, 45, 50),
)

# 9. Forest - Natural earth tones
THEME_FOREST = Theme(
    name="forest",
    primary=(76, 175, 80),
    secondary=(139, 195, 74),
    success=(76, 175, 80),
    warning=(205, 175, 60),
    error=(192, 86, 64),
    muted=(90, 100, 85),
    background=(20, 28, 20),
    surface=(30, 42, 30),
    surface_variant=(38, 52, 38),
    border=(60, 80, 60),
    text_primary=(240, 245, 235),
    text_secondary=(160, 175, 155),
    text_on_primary=(20, 30, 20),
    accent_colors=(
        (76, 175, 80),  # Green
        (139, 195, 74),  # Light green
        (205, 175, 60),  # Olive gold
        (165, 130, 95),  # Brown
        (100, 160, 130),  # Sage
        (180, 200, 100),  # Lime
    ),
    corner_radius=6,
    border_width=1,
    border_style="solid",
    bar_background=(40, 55, 40),
)

# 10. Candy - Playful pastel
THEME_CANDY = Theme(
    name="candy",
    primary=(255, 105, 180),
    secondary=(138, 207, 255),
    success=(144, 238, 144),
    warning=(255, 218, 121),
    error=(255, 150, 150),
    muted=(200, 180, 200),
    background=(255, 240, 245),
    surface=(255, 250, 252),
    surface_variant=(255, 235, 242),
    border=(255, 200, 220),
    text_primary=(80, 60, 80),
    text_secondary=(140, 120, 140),
    text_on_primary=(255, 255, 255),
    accent_colors=(
        (255, 105, 180),  # Hot pink
        (138, 207, 255),  # Sky blue
        (255, 182, 193),  # Light pink
        (152, 251, 152),  # Pale green
        (255, 218, 121),  # Light gold
        (221, 160, 221),  # Plum
    ),
    corner_radius=20,
    border_width=2,
    border_style="solid",
    layout_padding=10,
    widget_padding=8,
    gap=8,
    bar_background=(255, 220, 235),
)

# 11. Oak Yellow - Black cards with warm oak-yellow borders
THEME_OAK_YELLOW = Theme(
    name="oak_yellow",
    primary=(214, 170, 88),
    secondary=(186, 150, 74),
    success=(173, 199, 85),
    warning=(232, 183, 72),
    error=(210, 94, 70),
    muted=(120, 110, 90),
    background=(44, 34, 10),
    surface=(0, 0, 0),
    surface_variant=(10, 10, 10),
    border=(184, 142, 72),
    text_primary=(245, 235, 210),
    text_secondary=(170, 155, 120),
    text_on_primary=(15, 12, 8),
    accent_colors=(
        (214, 170, 88),  # Oak yellow
        (232, 183, 72),  # Warm gold
        (196, 154, 76),  # Antique brass
        (173, 199, 85),  # Olive-lime
        (145, 180, 205),  # Muted sky
        (210, 94, 70),  # Terracotta
    ),
    corner_radius=8,
    border_width=2,
    border_style="solid",
    bar_background=(40, 34, 24),
)

# 12. Amber Yellow - Brighter yellow variant on dark cards
THEME_AMBER_YELLOW = Theme(
    name="amber_yellow",
    primary=(242, 188, 56),
    secondary=(255, 214, 92),
    success=(170, 205, 95),
    warning=(255, 205, 70),
    error=(225, 98, 72),
    muted=(130, 120, 95),
    background=(56, 42, 10),
    surface=(0, 0, 0),
    surface_variant=(12, 12, 12),
    border=(242, 188, 56),
    text_primary=(255, 246, 218),
    text_secondary=(190, 170, 120),
    text_on_primary=(20, 14, 4),
    accent_colors=(
        (242, 188, 56),  # Amber
        (255, 214, 92),  # Light amber
        (224, 170, 52),  # Deep amber
        (170, 205, 95),  # Olive highlight
        (110, 170, 210),  # Blue contrast
        (225, 98, 72),  # Alert red
    ),
    corner_radius=8,
    border_width=2,
    border_style="solid",
    bar_background=(46, 36, 20),
)

# 13. Slate Mint - Matte charcoal with cool mint accents
THEME_SLATE_MINT = Theme(
    name="slate_mint",
    primary=(122, 196, 173),
    secondary=(109, 146, 166),
    success=(140, 181, 124),
    warning=(206, 172, 104),
    error=(188, 102, 98),
    muted=(108, 120, 122),
    background=(22, 27, 30),
    surface=(34, 40, 43),
    surface_variant=(43, 50, 54),
    border=(92, 154, 138),
    text_primary=(234, 239, 236),
    text_secondary=(159, 171, 167),
    text_on_primary=(16, 27, 24),
    accent_colors=(
        (122, 196, 173),  # Mint
        (109, 146, 166),  # Slate blue
        (206, 172, 104),  # Matte amber
        (188, 102, 98),  # Soft coral
        (140, 181, 124),  # Sage
        (165, 189, 194),  # Silver mist
    ),
    corner_radius=10,
    border_width=1,
    border_style="solid",
    bar_background=(57, 64, 67),
)

# 14. Terracotta Dusk - Warm earthy matte palette
THEME_TERRACOTTA_DUSK = Theme(
    name="terracotta_dusk",
    primary=(206, 135, 103),
    secondary=(189, 157, 117),
    success=(149, 175, 119),
    warning=(214, 173, 105),
    error=(182, 91, 79),
    muted=(134, 113, 97),
    background=(50, 37, 32),
    surface=(71, 53, 45),
    surface_variant=(82, 62, 52),
    border=(176, 118, 92),
    text_primary=(246, 236, 224),
    text_secondary=(188, 162, 141),
    text_on_primary=(38, 25, 20),
    accent_colors=(
        (206, 135, 103),  # Terracotta
        (176, 118, 92),  # Clay
        (189, 157, 117),  # Sandstone
        (149, 175, 119),  # Olive
        (128, 150, 166),  # Dusty sky
        (182, 91, 79),  # Brick red
    ),
    corner_radius=10,
    border_width=1,
    border_style="solid",
    bar_background=(95, 74, 61),
)

# 15. Nordic Fog - Light matte Scandinavian look
THEME_NORDIC_FOG = Theme(
    name="nordic_fog",
    primary=(92, 124, 139),
    secondary=(120, 145, 156),
    success=(111, 148, 124),
    warning=(186, 154, 101),
    error=(176, 103, 103),
    muted=(169, 178, 181),
    background=(223, 229, 231),
    surface=(245, 247, 247),
    surface_variant=(234, 238, 239),
    border=(171, 184, 188),
    text_primary=(42, 50, 55),
    text_secondary=(99, 112, 118),
    text_on_primary=(246, 248, 248),
    accent_colors=(
        (92, 124, 139),  # Storm blue
        (120, 145, 156),  # Steel
        (111, 148, 124),  # Pine
        (186, 154, 101),  # Wheat
        (176, 103, 103),  # Dusty red
        (132, 160, 171),  # Mist teal
    ),
    corner_radius=14,
    border_width=1,
    border_style="solid",
    value_bold=False,
    bar_background=(212, 219, 222),
)

# 16. Graphite Copper - Industrial dark with warm metal accents
THEME_GRAPHITE_COPPER = Theme(
    name="graphite_copper",
    primary=(181, 126, 96),
    secondary=(132, 149, 160),
    success=(131, 164, 122),
    warning=(197, 158, 101),
    error=(185, 95, 84),
    muted=(116, 108, 104),
    background=(20, 18, 18),
    surface=(34, 30, 30),
    surface_variant=(44, 39, 37),
    border=(154, 108, 82),
    text_primary=(239, 230, 222),
    text_secondary=(167, 151, 140),
    text_on_primary=(24, 18, 15),
    accent_colors=(
        (181, 126, 96),  # Copper
        (154, 108, 82),  # Burnt bronze
        (132, 149, 160),  # Gunmetal blue
        (131, 164, 122),  # Oxide green
        (197, 158, 101),  # Brass
        (185, 95, 84),  # Rust red
    ),
    corner_radius=8,
    border_width=2,
    border_style="solid",
    bar_background=(61, 53, 48),
)

# 17. Petrol Bloom - Deep teal matte with rose contrast
THEME_PETROL_BLOOM = Theme(
    name="petrol_bloom",
    primary=(105, 173, 182),
    secondary=(182, 129, 156),
    success=(126, 176, 142),
    warning=(207, 176, 109),
    error=(196, 107, 110),
    muted=(97, 123, 129),
    background=(16, 31, 36),
    surface=(23, 43, 49),
    surface_variant=(31, 55, 61),
    border=(76, 130, 139),
    text_primary=(226, 238, 239),
    text_secondary=(150, 174, 179),
    text_on_primary=(13, 27, 30),
    accent_colors=(
        (105, 173, 182),  # Petrol teal
        (182, 129, 156),  # Dusty rose
        (126, 176, 142),  # Seafoam
        (207, 176, 109),  # Matte gold
        (196, 107, 110),  # Berry red
        (132, 162, 184),  # Cloud blue
    ),
    corner_radius=12,
    border_width=1,
    border_style="solid",
    bar_background=(45, 69, 75),
)


# =============================================================================
# Theme Registry
# =============================================================================

THEMES: dict[str, Theme] = {
    "classic": THEME_CLASSIC,
    "minimal": THEME_MINIMAL,
    "neon": THEME_NEON,
    "retro": THEME_RETRO,
    "soft": THEME_SOFT,
    "light": THEME_LIGHT,
    "ocean": THEME_OCEAN,
    "sunset": THEME_SUNSET,
    "forest": THEME_FOREST,
    "candy": THEME_CANDY,
    "oak_yellow": THEME_OAK_YELLOW,
    "amber_yellow": THEME_AMBER_YELLOW,
    "slate_mint": THEME_SLATE_MINT,
    "terracotta_dusk": THEME_TERRACOTTA_DUSK,
    "nordic_fog": THEME_NORDIC_FOG,
    "graphite_copper": THEME_GRAPHITE_COPPER,
    "petrol_bloom": THEME_PETROL_BLOOM,
}

DEFAULT_THEME = THEME_CLASSIC


def get_theme(name: str) -> Theme:
    """Get a theme by name.

    Args:
        name: Theme name

    Returns:
        Theme instance, defaults to classic if name not found
    """
    return THEMES.get(name, DEFAULT_THEME)


__all__ = [
    "DEFAULT_THEME",
    "THEMES",
    "THEME_AMBER_YELLOW",
    "THEME_CANDY",
    "THEME_CLASSIC",
    "THEME_FOREST",
    "THEME_GRAPHITE_COPPER",
    "THEME_LIGHT",
    "THEME_MINIMAL",
    "THEME_NEON",
    "THEME_NORDIC_FOG",
    "THEME_OAK_YELLOW",
    "THEME_OCEAN",
    "THEME_PETROL_BLOOM",
    "THEME_RETRO",
    "THEME_SLATE_MINT",
    "THEME_SOFT",
    "THEME_SUNSET",
    "THEME_TERRACOTTA_DUSK",
    "BorderStyle",
    "Color",
    "FontWeight",
    "Theme",
    "get_theme",
]
