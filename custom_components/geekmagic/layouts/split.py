"""Split layout for GeekMagic displays."""

from __future__ import annotations

from .base import Layout, Slot


class SplitHorizontal(Layout):
    """Horizontal split layout - side by side (left/right).

    +----------+----------+
    |          |          |
    |  LEFT    |  RIGHT   |
    | (slot 0) | (slot 1) |
    |          |          |
    +----------+----------+
    """

    def __init__(
        self,
        ratio: float = 0.5,
        padding: int = 8,
        gap: int = 8,
    ) -> None:
        """Initialize horizontal split layout.

        Args:
            ratio: Ratio of left panel width (0.0-1.0)
            padding: Padding around edges
            gap: Gap between panels
        """
        self.ratio = max(0.2, min(0.8, ratio))
        super().__init__(padding=padding, gap=gap)

    def _calculate_slots(self) -> None:
        """Calculate left/right panel rectangles."""
        self.slots = []

        available_width, _ = self._available_space()
        content_width = available_width - self.gap
        left_width = int(content_width * self.ratio)

        # Left slot
        self.slots.append(
            Slot(
                index=0,
                rect=(
                    self.padding,
                    self.padding,
                    self.padding + left_width,
                    self.height - self.padding,
                ),
            )
        )

        # Right slot
        self.slots.append(
            Slot(
                index=1,
                rect=(
                    self.padding + left_width + self.gap,
                    self.padding,
                    self.width - self.padding,
                    self.height - self.padding,
                ),
            )
        )


class SplitVertical(Layout):
    """Vertical split layout - stacked (top/bottom).

    +---------------------+
    |        TOP          |
    |      (slot 0)       |
    +---------------------+
    |       BOTTOM        |
    |      (slot 1)       |
    +---------------------+
    """

    def __init__(
        self,
        ratio: float = 0.5,
        padding: int = 8,
        gap: int = 8,
    ) -> None:
        """Initialize vertical split layout.

        Args:
            ratio: Ratio of top panel height (0.0-1.0)
            padding: Padding around edges
            gap: Gap between panels
        """
        self.ratio = max(0.2, min(0.8, ratio))
        super().__init__(padding=padding, gap=gap)

    def _calculate_slots(self) -> None:
        """Calculate top/bottom panel rectangles."""
        self.slots = []

        _, available_height = self._available_space()
        content_height = available_height - self.gap
        top_height = int(content_height * self.ratio)

        # Top slot
        self.slots.append(
            Slot(
                index=0,
                rect=(
                    self.padding,
                    self.padding,
                    self.width - self.padding,
                    self.padding + top_height,
                ),
            )
        )

        # Bottom slot
        self.slots.append(
            Slot(
                index=1,
                rect=(
                    self.padding,
                    self.padding + top_height + self.gap,
                    self.width - self.padding,
                    self.height - self.padding,
                ),
            )
        )


# Keep for backwards compatibility
SplitLayout = SplitHorizontal


class ThreeColumnLayout(Layout):
    """Three column layout.

    +-------+-------+-------+
    |       |       |       |
    |  L    |   M   |   R   |
    |       |       |       |
    +-------+-------+-------+
    """

    def __init__(
        self,
        ratios: tuple[float, float, float] = (0.33, 0.34, 0.33),
        padding: int = 8,
        gap: int = 8,
    ) -> None:
        """Initialize three-column layout.

        Args:
            ratios: Width ratios for each column (should sum to ~1.0)
            padding: Padding around edges
            gap: Gap between columns
        """
        self.ratios = ratios
        super().__init__(padding=padding, gap=gap)

    def _calculate_slots(self) -> None:
        """Calculate column rectangles."""
        self.slots = []

        available_width = self.width - (2 * self.padding) - (2 * self.gap)
        total_ratio = sum(self.ratios)

        x = self.padding
        for i, ratio in enumerate(self.ratios):
            col_width = int(available_width * (ratio / total_ratio))

            self.slots.append(
                Slot(
                    index=i,
                    rect=(
                        x,
                        self.padding,
                        x + col_width,
                        self.height - self.padding,
                    ),
                )
            )

            x += col_width + self.gap
