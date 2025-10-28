"""
file: test_track_builder.py
author: GitHub Copilot
date: 2025-10-28
notes: Tests for the track builder functionality
"""

import json
import os
import tempfile

import pytest

from gym_donkeycar.core.track_builder import (
    CurveSegment,
    ElevationSegment,
    StraightSegment,
    TrackBuilder,
    TrackSegment,
    create_figure_eight,
    create_s_curve,
    create_simple_oval,
)


class TestTrackSegment:
    """Tests for TrackSegment base class."""

    def test_create_base_segment(self):
        segment = TrackSegment(length=50.0)
        assert segment.length == 50.0
        assert segment.segment_type == "base"

    def test_to_dict(self):
        segment = TrackSegment(length=50.0)
        data = segment.to_dict()
        assert data["type"] == "base"
        assert data["length"] == 50.0


class TestStraightSegment:
    """Tests for StraightSegment class."""

    def test_create_straight_segment(self):
        segment = StraightSegment(length=100.0)
        assert segment.length == 100.0
        assert segment.segment_type == "straight"

    def test_to_dict(self):
        segment = StraightSegment(length=100.0)
        data = segment.to_dict()
        assert data["type"] == "straight"
        assert data["length"] == 100.0


class TestCurveSegment:
    """Tests for CurveSegment class."""

    def test_create_curve_segment(self):
        segment = CurveSegment(length=31.4, radius=20.0, angle=90.0, direction="left")
        assert segment.length == 31.4
        assert segment.radius == 20.0
        assert segment.angle == 90.0
        assert segment.direction == "left"
        assert segment.segment_type == "curve"

    def test_to_dict(self):
        segment = CurveSegment(length=31.4, radius=20.0, angle=90.0, direction="right")
        data = segment.to_dict()
        assert data["type"] == "curve"
        assert data["length"] == 31.4
        assert data["radius"] == 20.0
        assert data["angle"] == 90.0
        assert data["direction"] == "right"


class TestElevationSegment:
    """Tests for ElevationSegment class."""

    def test_create_elevation_segment(self):
        segment = ElevationSegment(length=50.0, height_change=10.0, gradient=15.0)
        assert segment.length == 50.0
        assert segment.height_change == 10.0
        assert segment.gradient == 15.0
        assert segment.segment_type == "elevation"

    def test_create_elevation_segment_without_gradient(self):
        segment = ElevationSegment(length=50.0, height_change=10.0)
        assert segment.length == 50.0
        assert segment.height_change == 10.0
        assert segment.gradient is None

    def test_to_dict(self):
        segment = ElevationSegment(length=50.0, height_change=10.0, gradient=15.0)
        data = segment.to_dict()
        assert data["type"] == "elevation"
        assert data["length"] == 50.0
        assert data["height_change"] == 10.0
        assert data["gradient"] == 15.0


class TestTrackBuilder:
    """Tests for TrackBuilder class."""

    def test_create_empty_builder(self):
        builder = TrackBuilder()
        assert builder.name == "custom_track"
        assert builder.width == 4.0
        assert builder.start_position == (0.0, 0.0, 0.0)
        assert len(builder.segments) == 0

    def test_create_builder_with_params(self):
        builder = TrackBuilder(name="test_track", width=5.0, start_position=(1.0, 2.0, 3.0))
        assert builder.name == "test_track"
        assert builder.width == 5.0
        assert builder.start_position == (1.0, 2.0, 3.0)

    def test_add_straight(self):
        builder = TrackBuilder()
        builder.add_straight(100.0)
        assert len(builder.segments) == 1
        assert isinstance(builder.segments[0], StraightSegment)
        assert builder.segments[0].length == 100.0

    def test_add_curve(self):
        builder = TrackBuilder()
        builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")
        assert len(builder.segments) == 1
        assert isinstance(builder.segments[0], CurveSegment)
        assert builder.segments[0].length == 31.4
        assert builder.segments[0].radius == 20.0
        assert builder.segments[0].angle == 90.0
        assert builder.segments[0].direction == "left"

    def test_add_curve_invalid_direction(self):
        builder = TrackBuilder()
        with pytest.raises(ValueError, match="Direction must be"):
            builder.add_curve(31.4, radius=20.0, angle=90.0, direction="up")

    def test_add_elevation(self):
        builder = TrackBuilder()
        builder.add_elevation(50.0, height_change=10.0, gradient=15.0)
        assert len(builder.segments) == 1
        assert isinstance(builder.segments[0], ElevationSegment)
        assert builder.segments[0].length == 50.0
        assert builder.segments[0].height_change == 10.0
        assert builder.segments[0].gradient == 15.0

    def test_add_segment(self):
        builder = TrackBuilder()
        custom_segment = StraightSegment(75.0)
        builder.add_segment(custom_segment)
        assert len(builder.segments) == 1
        assert builder.segments[0] is custom_segment

    def test_clear(self):
        builder = TrackBuilder()
        builder.add_straight(100.0)
        builder.add_straight(50.0)
        assert len(builder.segments) == 2
        builder.clear()
        assert len(builder.segments) == 0

    def test_method_chaining(self):
        builder = TrackBuilder()
        result = builder.add_straight(100.0).add_curve(31.4, 20.0, 90.0, "left").add_straight(50.0)
        assert result is builder
        assert len(builder.segments) == 3

    def test_build(self):
        builder = TrackBuilder(name="test_track", width=5.0)
        builder.add_straight(100.0)
        builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")

        config = builder.build()
        assert config["name"] == "test_track"
        assert config["width"] == 5.0
        assert config["start_position"]["x"] == 0.0
        assert config["start_position"]["y"] == 0.0
        assert config["start_position"]["z"] == 0.0
        assert len(config["segments"]) == 2
        assert config["total_length"] == 131.4
        assert config["num_segments"] == 2

        # Check segment data
        assert config["segments"][0]["type"] == "straight"
        assert config["segments"][0]["length"] == 100.0
        assert config["segments"][1]["type"] == "curve"
        assert config["segments"][1]["length"] == 31.4

    def test_to_json(self):
        builder = TrackBuilder()
        builder.add_straight(100.0)
        json_str = builder.to_json()

        # Verify it's valid JSON
        config = json.loads(json_str)
        assert config["name"] == "custom_track"
        assert len(config["segments"]) == 1

    def test_save_and_load(self):
        # Create a track
        builder = TrackBuilder(name="save_test", width=4.5)
        builder.add_straight(100.0)
        builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")
        builder.add_elevation(50.0, height_change=10.0)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            filepath = f.name

        try:
            builder.save(filepath)

            # Load the track
            loaded_builder = TrackBuilder.load(filepath)
            loaded_config = loaded_builder.build()

            # Verify loaded data matches original
            original_config = builder.build()
            assert loaded_config["name"] == original_config["name"]
            assert loaded_config["width"] == original_config["width"]
            assert loaded_config["num_segments"] == original_config["num_segments"]
            assert loaded_config["total_length"] == original_config["total_length"]

            # Verify segments
            for i, segment in enumerate(loaded_config["segments"]):
                orig_segment = original_config["segments"][i]
                assert segment["type"] == orig_segment["type"]
                assert segment["length"] == orig_segment["length"]

        finally:
            # Clean up
            if os.path.exists(filepath):
                os.remove(filepath)

    def test_from_json(self):
        json_str = """
        {
            "name": "test_track",
            "width": 5.0,
            "start_position": {"x": 1.0, "y": 2.0, "z": 3.0},
            "segments": [
                {"type": "straight", "length": 100.0},
                {"type": "curve", "length": 31.4, "radius": 20.0, "angle": 90.0, "direction": "left"},
                {"type": "elevation", "length": 50.0, "height_change": 10.0, "gradient": 15.0}
            ]
        }
        """

        builder = TrackBuilder.from_json(json_str)
        config = builder.build()

        assert config["name"] == "test_track"
        assert config["width"] == 5.0
        assert config["start_position"]["x"] == 1.0
        assert config["start_position"]["y"] == 2.0
        assert config["start_position"]["z"] == 3.0
        assert len(config["segments"]) == 3


class TestPredefinedTracks:
    """Tests for predefined track templates."""

    def test_create_simple_oval(self):
        track = create_simple_oval(length=100.0, width=60.0, track_width=4.0)
        assert track["name"] == "simple_oval"
        assert track["width"] == 4.0
        assert len(track["segments"]) == 4  # 2 straights + 2 curves
        assert track["total_length"] > 0

    def test_create_figure_eight(self):
        track = create_figure_eight(size=50.0, track_width=4.0)
        assert track["name"] == "figure_eight"
        assert track["width"] == 4.0
        assert len(track["segments"]) == 4  # 4 curves
        assert track["total_length"] > 0

    def test_create_s_curve(self):
        track = create_s_curve(straight_length=50.0, curve_radius=25.0, track_width=4.0)
        assert track["name"] == "s_curve"
        assert track["width"] == 4.0
        assert len(track["segments"]) > 0
        assert track["total_length"] > 0


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_empty_track(self):
        builder = TrackBuilder()
        config = builder.build()
        assert config["total_length"] == 0
        assert config["num_segments"] == 0
        assert len(config["segments"]) == 0

    def test_single_segment(self):
        builder = TrackBuilder()
        builder.add_straight(100.0)
        config = builder.build()
        assert config["total_length"] == 100.0
        assert config["num_segments"] == 1

    def test_large_track(self):
        builder = TrackBuilder()
        for _ in range(100):
            builder.add_straight(10.0)
        config = builder.build()
        assert config["num_segments"] == 100
        assert config["total_length"] == 1000.0

    def test_negative_height_change(self):
        builder = TrackBuilder()
        builder.add_elevation(50.0, height_change=-10.0)
        config = builder.build()
        segment = config["segments"][0]
        assert segment["height_change"] == -10.0
