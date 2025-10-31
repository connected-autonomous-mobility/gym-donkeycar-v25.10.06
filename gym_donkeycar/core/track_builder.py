"""
file: track_builder.py
author: GitHub Copilot
date: 2025-10-28
notes: Programmatic track creation API for gym-donkeycar
"""

import json
from typing import Any, Dict, List, Optional, Tuple, Union


class TrackSegment:
    """
    Base class for track segments.

    Track segments are the building blocks of a custom track.
    """

    def __init__(self, length: float):
        """
        Initialize a track segment.

        :param length: Length of the segment in meters
        """
        self.length = length
        self.segment_type = "base"

    def to_dict(self) -> Dict[str, Any]:
        """Convert segment to dictionary representation."""
        return {
            "type": self.segment_type,
            "length": self.length,
        }


class StraightSegment(TrackSegment):
    """A straight track segment."""

    def __init__(self, length: float):
        """
        Create a straight track segment.

        :param length: Length of the straight in meters
        """
        super().__init__(length)
        self.segment_type = "straight"


class CurveSegment(TrackSegment):
    """A curved track segment."""

    def __init__(self, length: float, radius: float, angle: float, direction: str = "left"):
        """
        Create a curved track segment.

        :param length: Arc length of the curve in meters
        :param radius: Radius of the curve in meters
        :param angle: Angle of the curve in degrees
        :param direction: Direction of the curve ('left' or 'right')
        """
        super().__init__(length)
        self.segment_type = "curve"
        self.radius = radius
        self.angle = angle
        self.direction = direction

    def to_dict(self) -> Dict[str, Any]:
        """Convert segment to dictionary representation."""
        data = super().to_dict()
        data.update(
            {
                "radius": self.radius,
                "angle": self.angle,
                "direction": self.direction,
            }
        )
        return data


class ElevationSegment(TrackSegment):
    """A track segment with elevation change."""

    def __init__(self, length: float, height_change: float, gradient: Optional[float] = None):
        """
        Create a track segment with elevation change.

        :param length: Length of the segment in meters
        :param height_change: Height change in meters (positive for uphill, negative for downhill)
        :param gradient: Optional gradient in degrees
        """
        super().__init__(length)
        self.segment_type = "elevation"
        self.height_change = height_change
        self.gradient = gradient

    def to_dict(self) -> Dict[str, Any]:
        """Convert segment to dictionary representation."""
        data = super().to_dict()
        data.update(
            {
                "height_change": self.height_change,
                "gradient": self.gradient,
            }
        )
        return data


class TrackBuilder:
    """
    Builder class for creating custom tracks programmatically.

    Example:
        >>> from gym_donkeycar.core.track_builder import TrackBuilder
        >>> builder = TrackBuilder(name="my_custom_track", width=4.0)
        >>> builder.add_straight(50.0)
        >>> builder.add_curve(30.0, radius=20.0, angle=90.0, direction="left")
        >>> builder.add_straight(30.0)
        >>> builder.add_curve(30.0, radius=20.0, angle=90.0, direction="left")
        >>> track_config = builder.build()
    """

    def __init__(
        self, name: str = "custom_track", width: float = 4.0, start_position: Optional[Tuple[float, float, float]] = None
    ):
        """
        Initialize the track builder.

        :param name: Name of the track
        :param width: Width of the track in meters
        :param start_position: Starting position as (x, y, z) tuple
        """
        self.name = name
        self.width = width
        self.start_position = start_position or (0.0, 0.0, 0.0)
        self.segments: List[TrackSegment] = []

    def add_straight(self, length: float) -> "TrackBuilder":
        """
        Add a straight segment to the track.

        :param length: Length of the straight in meters
        :return: Self for method chaining
        """
        self.segments.append(StraightSegment(length))
        return self

    def add_curve(self, length: float, radius: float, angle: float, direction: str = "left") -> "TrackBuilder":
        """
        Add a curved segment to the track.

        :param length: Arc length of the curve in meters
        :param radius: Radius of the curve in meters
        :param angle: Angle of the curve in degrees
        :param direction: Direction of the curve ('left' or 'right')
        :return: Self for method chaining
        """
        if direction not in ["left", "right"]:
            raise ValueError(f"Direction must be 'left' or 'right', got '{direction}'")
        self.segments.append(CurveSegment(length, radius, angle, direction))
        return self

    def add_elevation(self, length: float, height_change: float, gradient: Optional[float] = None) -> "TrackBuilder":
        """
        Add a segment with elevation change.

        :param length: Length of the segment in meters
        :param height_change: Height change in meters
        :param gradient: Optional gradient in degrees
        :return: Self for method chaining
        """
        self.segments.append(ElevationSegment(length, height_change, gradient))
        return self

    def add_segment(self, segment: TrackSegment) -> "TrackBuilder":
        """
        Add a custom segment to the track.

        :param segment: TrackSegment instance
        :return: Self for method chaining
        """
        self.segments.append(segment)
        return self

    def clear(self) -> "TrackBuilder":
        """
        Clear all segments from the track.

        :return: Self for method chaining
        """
        self.segments = []
        return self

    def build(self) -> Dict[str, Any]:
        """
        Build and return the track configuration.

        :return: Dictionary containing the track configuration
        """
        return {
            "name": self.name,
            "width": self.width,
            "start_position": {
                "x": self.start_position[0],
                "y": self.start_position[1],
                "z": self.start_position[2],
            },
            "segments": [segment.to_dict() for segment in self.segments],
            "total_length": sum(segment.length for segment in self.segments),
            "num_segments": len(self.segments),
        }

    def to_json(self, indent: Optional[int] = 2) -> str:
        """
        Build and return the track configuration as JSON.

        :param indent: JSON indentation level (None for compact)
        :return: JSON string of the track configuration
        """
        return json.dumps(self.build(), indent=indent)

    def save(self, filepath: str) -> None:
        """
        Save the track configuration to a JSON file.

        :param filepath: Path to the output JSON file
        """
        with open(filepath, "w") as f:
            f.write(self.to_json())

    @staticmethod
    def from_json(json_str: str) -> "TrackBuilder":
        """
        Create a TrackBuilder from a JSON string.

        :param json_str: JSON string containing track configuration
        :return: TrackBuilder instance
        """
        config = json.loads(json_str)
        builder = TrackBuilder(
            name=config.get("name", "custom_track"),
            width=config.get("width", 4.0),
            start_position=(
                config.get("start_position", {}).get("x", 0.0),
                config.get("start_position", {}).get("y", 0.0),
                config.get("start_position", {}).get("z", 0.0),
            ),
        )

        for seg_data in config.get("segments", []):
            seg_type = seg_data.get("type")
            if seg_type == "straight":
                builder.add_straight(seg_data["length"])
            elif seg_type == "curve":
                builder.add_curve(
                    seg_data["length"],
                    seg_data["radius"],
                    seg_data["angle"],
                    seg_data.get("direction", "left"),
                )
            elif seg_type == "elevation":
                builder.add_elevation(
                    seg_data["length"],
                    seg_data["height_change"],
                    seg_data.get("gradient"),
                )

        return builder

    @staticmethod
    def load(filepath: str) -> "TrackBuilder":
        """
        Load a track configuration from a JSON file.

        :param filepath: Path to the input JSON file
        :return: TrackBuilder instance
        """
        with open(filepath, "r") as f:
            return TrackBuilder.from_json(f.read())


def create_simple_oval(length: float = 100.0, width: float = 50.0, track_width: float = 4.0) -> Dict[str, Any]:
    """
    Create a simple oval track configuration.

    :param length: Length of the straight sections in meters
    :param width: Width of the track (determines curve radius) in meters
    :param track_width: Width of the racing surface in meters
    :return: Track configuration dictionary
    """
    import math

    # Calculate curve parameters
    radius = width / 2.0
    angle = 180.0  # Half circle
    arc_length = math.pi * radius  # Half circumference

    builder = TrackBuilder(name="simple_oval", width=track_width)
    builder.add_straight(length)
    builder.add_curve(arc_length, radius, angle, "left")
    builder.add_straight(length)
    builder.add_curve(arc_length, radius, angle, "left")

    return builder.build()


def create_figure_eight(size: float = 50.0, track_width: float = 4.0) -> Dict[str, Any]:
    """
    Create a figure-eight track configuration.

    :param size: Size parameter for the track in meters
    :param track_width: Width of the racing surface in meters
    :return: Track configuration dictionary
    """
    import math

    radius = size / 2.0
    angle = 180.0
    arc_length = math.pi * radius

    builder = TrackBuilder(name="figure_eight", width=track_width)
    # First loop
    builder.add_curve(arc_length, radius, angle, "left")
    builder.add_curve(arc_length, radius, angle, "left")
    # Second loop (opposite direction)
    builder.add_curve(arc_length, radius, angle, "right")
    builder.add_curve(arc_length, radius, angle, "right")

    return builder.build()


def create_s_curve(straight_length: float = 40.0, curve_radius: float = 20.0, track_width: float = 4.0) -> Dict[str, Any]:
    """
    Create an S-curve track configuration.

    :param straight_length: Length of straight sections in meters
    :param curve_radius: Radius of curves in meters
    :param track_width: Width of the racing surface in meters
    :return: Track configuration dictionary
    """
    import math

    angle = 90.0
    arc_length = (math.pi * curve_radius * angle) / 180.0

    builder = TrackBuilder(name="s_curve", width=track_width)
    builder.add_straight(straight_length)
    builder.add_curve(arc_length, curve_radius, angle, "left")
    builder.add_straight(straight_length / 2.0)
    builder.add_curve(arc_length, curve_radius, angle, "right")
    builder.add_straight(straight_length)

    return builder.build()
