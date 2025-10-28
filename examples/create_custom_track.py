"""
file: create_custom_track.py
author: GitHub Copilot
date: 2025-10-28
notes: Example showing how to create custom tracks programmatically using the TrackBuilder API
"""
import json

from gym_donkeycar.core import TrackBuilder, create_figure_eight, create_s_curve, create_simple_oval


def example_simple_track():
    """Create a simple rectangular track."""
    print("=" * 60)
    print("Example 1: Simple Rectangular Track")
    print("=" * 60)

    builder = TrackBuilder(name="my_rectangular_track", width=4.0)

    # Add track segments
    builder.add_straight(100.0)  # 100m straight
    builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")  # 90-degree left turn
    builder.add_straight(60.0)  # 60m straight
    builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")  # 90-degree left turn
    builder.add_straight(100.0)  # 100m straight
    builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")  # 90-degree left turn
    builder.add_straight(60.0)  # 60m straight
    builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")  # 90-degree left turn

    # Build the track configuration
    track_config = builder.build()
    print(json.dumps(track_config, indent=2))
    print()

    # Save to file
    builder.save("/tmp/rectangular_track.json")
    print(f"Track saved to: /tmp/rectangular_track.json")
    print(f"Total track length: {track_config['total_length']:.2f} meters")
    print()


def example_chained_building():
    """Create a track using method chaining."""
    print("=" * 60)
    print("Example 2: Track with Method Chaining")
    print("=" * 60)

    track_config = (
        TrackBuilder(name="chained_track", width=5.0)
        .add_straight(50.0)
        .add_curve(47.1, radius=30.0, angle=90.0, direction="right")
        .add_straight(80.0)
        .add_curve(47.1, radius=30.0, angle=90.0, direction="right")
        .add_straight(50.0)
        .add_curve(47.1, radius=30.0, angle=90.0, direction="right")
        .add_straight(80.0)
        .add_curve(47.1, radius=30.0, angle=90.0, direction="right")
        .build()
    )

    print(json.dumps(track_config, indent=2))
    print()


def example_with_elevation():
    """Create a track with elevation changes."""
    print("=" * 60)
    print("Example 3: Track with Elevation Changes")
    print("=" * 60)

    builder = TrackBuilder(name="hilly_track", width=4.0)

    # Flat start
    builder.add_straight(50.0)
    # Uphill section
    builder.add_elevation(40.0, height_change=10.0, gradient=15.0)
    # Flat section at the top
    builder.add_straight(30.0)
    # Downhill section
    builder.add_elevation(40.0, height_change=-10.0, gradient=-15.0)
    # Curve
    builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")
    # Back to start
    builder.add_straight(50.0)

    track_config = builder.build()
    print(json.dumps(track_config, indent=2))
    print()


def example_predefined_tracks():
    """Use predefined track templates."""
    print("=" * 60)
    print("Example 4: Predefined Track Templates")
    print("=" * 60)

    # Simple oval
    print("Simple Oval Track:")
    oval = create_simple_oval(length=100.0, width=60.0, track_width=4.0)
    print(json.dumps(oval, indent=2))
    print()

    # Figure eight
    print("Figure Eight Track:")
    fig8 = create_figure_eight(size=50.0, track_width=4.0)
    print(json.dumps(fig8, indent=2))
    print()

    # S-curve
    print("S-Curve Track:")
    s_curve = create_s_curve(straight_length=50.0, curve_radius=25.0, track_width=4.0)
    print(json.dumps(s_curve, indent=2))
    print()


def example_save_and_load():
    """Save and load track configurations."""
    print("=" * 60)
    print("Example 5: Save and Load Track Configurations")
    print("=" * 60)

    # Create and save a track
    builder = TrackBuilder(name="saved_track", width=4.5)
    builder.add_straight(60.0).add_curve(31.4, radius=20.0, angle=90.0, direction="left").add_straight(60.0)

    filepath = "/tmp/my_track.json"
    builder.save(filepath)
    print(f"Saved track to: {filepath}")

    # Load the track
    loaded_builder = TrackBuilder.load(filepath)
    loaded_config = loaded_builder.build()
    print("Loaded track configuration:")
    print(json.dumps(loaded_config, indent=2))
    print()


def example_complex_track():
    """Create a more complex racing track."""
    print("=" * 60)
    print("Example 6: Complex Racing Track")
    print("=" * 60)

    builder = TrackBuilder(name="racing_circuit", width=6.0, start_position=(0.0, 0.0, 0.0))

    # Start straight
    builder.add_straight(120.0)

    # First corner complex (chicane)
    builder.add_curve(15.7, radius=10.0, angle=45.0, direction="right")
    builder.add_straight(20.0)
    builder.add_curve(15.7, radius=10.0, angle=45.0, direction="left")
    builder.add_straight(20.0)
    builder.add_curve(15.7, radius=10.0, angle=45.0, direction="right")

    # Long straight
    builder.add_straight(150.0)

    # Hairpin turn
    builder.add_curve(47.1, radius=15.0, angle=180.0, direction="left")

    # Back straight with elevation
    builder.add_elevation(80.0, height_change=8.0, gradient=10.0)
    builder.add_straight(50.0)
    builder.add_elevation(80.0, height_change=-8.0, gradient=-10.0)

    # Final corners to complete the loop
    builder.add_curve(23.6, radius=15.0, angle=90.0, direction="right")
    builder.add_straight(60.0)
    builder.add_curve(23.6, radius=15.0, angle=90.0, direction="right")

    track_config = builder.build()
    print(json.dumps(track_config, indent=2))
    print(f"\nTotal track length: {track_config['total_length']:.2f} meters")
    print(f"Number of segments: {track_config['num_segments']}")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Track Builder Examples - Create Tracks Programmatically  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\n")

    # Run all examples
    example_simple_track()
    example_chained_building()
    example_with_elevation()
    example_predefined_tracks()
    example_save_and_load()
    example_complex_track()

    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print("\nNOTE: These track configurations define the track geometry.")
    print("To use them with the simulator, you would need to:")
    print("1. Load them into the Unity simulator")
    print("2. Or use them with a track generation system")
    print("3. The JSON format can be extended for your specific needs")
