# Track Builder Quick Start Guide

This guide will help you get started with creating custom tracks programmatically using the Track Builder API.

## Installation

The Track Builder is included with gym-donkeycar. No additional installation is required.

```bash
pip install gym-donkeycar
```

## Basic Usage

### 1. Import the Track Builder

```python
from gym_donkeycar.core import TrackBuilder
```

### 2. Create a Simple Track

```python
# Create a track builder instance
builder = TrackBuilder(name="my_first_track", width=4.0)

# Add some segments
builder.add_straight(100.0)  # 100 meter straight
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")  # 90° left turn
builder.add_straight(50.0)   # 50 meter straight

# Build the track configuration
track_config = builder.build()

print(f"Track length: {track_config['total_length']} meters")
print(f"Number of segments: {track_config['num_segments']}")
```

### 3. Save Your Track

```python
# Save to JSON file
builder.save("my_track.json")

# Or get JSON string
json_string = builder.to_json()
print(json_string)
```

### 4. Load a Saved Track

```python
# Load from file
builder = TrackBuilder.load("my_track.json")
track_config = builder.build()
```

## Track Segments

### Straight Segments

Add straight sections to your track:

```python
builder.add_straight(length=100.0)  # length in meters
```

### Curve Segments

Add curved sections:

```python
builder.add_curve(
    length=31.4,        # arc length in meters
    radius=20.0,        # radius of curvature in meters
    angle=90.0,         # angle in degrees
    direction="left"    # "left" or "right"
)
```

**Calculating arc length:** For a circular arc, use: `length = (π × radius × angle) / 180`

### Elevation Segments

Add hills and valleys:

```python
builder.add_elevation(
    length=50.0,           # length in meters
    height_change=10.0,    # height change in meters (positive = uphill)
    gradient=15.0          # optional: gradient angle in degrees
)
```

## Method Chaining

Create tracks concisely using method chaining:

```python
track = (TrackBuilder(name="oval")
    .add_straight(100.0)
    .add_curve(31.4, 20.0, 90.0, "left")
    .add_straight(100.0)
    .add_curve(31.4, 20.0, 90.0, "left")
    .build())
```

## Predefined Templates

Use built-in track templates:

```python
from gym_donkeycar.core import (
    create_simple_oval,
    create_figure_eight,
    create_s_curve
)

# Simple oval track
oval = create_simple_oval(length=100.0, width=60.0, track_width=4.0)

# Figure-eight track
figure_eight = create_figure_eight(size=50.0, track_width=4.0)

# S-curve track
s_curve = create_s_curve(straight_length=50.0, curve_radius=25.0, track_width=4.0)
```

## Complete Example

Here's a complete example creating a racing circuit:

```python
from gym_donkeycar.core import TrackBuilder

# Create a complex racing circuit
circuit = (TrackBuilder(name="racing_circuit", width=6.0)
    # Main straight
    .add_straight(150.0)
    
    # Chicane
    .add_curve(15.7, radius=10.0, angle=45.0, direction="right")
    .add_straight(20.0)
    .add_curve(15.7, radius=10.0, angle=45.0, direction="left")
    
    # Long straight
    .add_straight(120.0)
    
    # Hairpin turn
    .add_curve(47.1, radius=15.0, angle=180.0, direction="left")
    
    # Back straight with hill
    .add_elevation(80.0, height_change=10.0, gradient=12.0)
    .add_straight(50.0)
    .add_elevation(80.0, height_change=-10.0, gradient=-12.0)
    
    # Final corners
    .add_curve(31.4, radius=20.0, angle=90.0, direction="right")
    .add_straight(60.0)
    .add_curve(31.4, radius=20.0, angle=90.0, direction="right")
    .build())

print(f"Circuit length: {circuit['total_length']:.2f} meters")
print(f"Number of segments: {circuit['num_segments']}")

# Save the track
import json
builder = TrackBuilder.from_json(json.dumps(circuit))
builder.save("racing_circuit.json")
```

## Track Configuration Format

The `build()` method returns a dictionary with this structure:

```python
{
    "name": "my_track",
    "width": 4.0,
    "start_position": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
    },
    "segments": [
        {
            "type": "straight",
            "length": 100.0
        },
        {
            "type": "curve",
            "length": 31.4,
            "radius": 20.0,
            "angle": 90.0,
            "direction": "left"
        }
    ],
    "total_length": 131.4,
    "num_segments": 2
}
```

## Next Steps

- See [complete examples](create_custom_track.py) for more detailed code
- Read the [full documentation](../docs/TRACK_BUILDER.md) for advanced features
- Experiment with procedural generation using random parameters
- Create your own custom segment types by extending `TrackSegment`

## Tips

1. **Calculate arc lengths accurately:** Use the formula `(π × radius × angle) / 180` for curves
2. **Use consistent units:** All lengths are in meters, angles in degrees
3. **Chain methods for readability:** Method chaining makes track definitions easier to read
4. **Save your work:** Always save complex tracks to JSON files for reuse
5. **Start simple:** Begin with basic shapes and gradually add complexity

## Getting Help

- Check the [main documentation](../docs/TRACK_BUILDER.md)
- Look at the [example scripts](create_custom_track.py)
- Review the [test cases](../tests/test_track_builder.py) for more usage patterns

Happy track building! 🏁
