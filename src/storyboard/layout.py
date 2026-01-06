"""Storyboard layout templates"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class StoryboardLayout:
    """Layout configuration for storyboard"""
    columns: int = 3
    image_width: int = 400
    image_height: int = 225  # 16:9 aspect ratio
    padding: int = 20
    caption_height: int = 60
    title_height: int = 80
    font_size_title: int = 24
    font_size_caption: int = 12
    font_size_metadata: int = 10
    background_color: Tuple[int, int, int] = (255, 255, 255)
    text_color: Tuple[int, int, int] = (0, 0, 0)
    border_color: Tuple[int, int, int] = (200, 200, 200)
    border_width: int = 2

    def calculate_dimensions(self, num_frames: int) -> Tuple[int, int]:
        """
        Calculate total storyboard dimensions

        Args:
            num_frames: Number of frames in storyboard

        Returns:
            Tuple of (width, height)
        """
        rows = (num_frames + self.columns - 1) // self.columns

        width = (
            self.padding +
            (self.image_width + self.padding) * self.columns
        )

        height = (
            self.title_height +
            self.padding +
            (self.image_height + self.caption_height + self.padding) * rows +
            self.padding
        )

        return width, height

    def get_frame_position(self, index: int) -> Tuple[int, int]:
        """
        Get position for frame at index

        Args:
            index: Frame index

        Returns:
            Tuple of (x, y) position
        """
        row = index // self.columns
        col = index % self.columns

        x = self.padding + col * (self.image_width + self.padding)
        y = (
            self.title_height +
            self.padding +
            row * (self.image_height + self.caption_height + self.padding)
        )

        return x, y


class TimelineLayout(StoryboardLayout):
    """Timeline-style layout (single column)"""

    def __init__(self):
        super().__init__(
            columns=1,
            image_width=800,
            image_height=450,
            padding=30,
            caption_height=80
        )


class GridLayout(StoryboardLayout):
    """Grid layout (3x3 or custom)"""

    def __init__(self, columns: int = 3):
        super().__init__(
            columns=columns,
            image_width=300,
            image_height=169,
            padding=15,
            caption_height=50
        )


class CompactLayout(StoryboardLayout):
    """Compact layout for many frames"""

    def __init__(self):
        super().__init__(
            columns=4,
            image_width=250,
            image_height=141,
            padding=10,
            caption_height=40,
            font_size_caption=10
        )
