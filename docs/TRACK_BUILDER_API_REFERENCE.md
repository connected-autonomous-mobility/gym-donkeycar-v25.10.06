# Creating Custom Tracks Programmatically

This guide explains how to create custom tracks for gym-donkeycar using Python code.

## Overview

The Track Builder API allows you to programmatically define track layouts using Python code instead of manually designing them in a graphical editor. This is useful for:

- **Procedural generation**: Create random or parameterized tracks
- **Research and experimentation**: Easily test different track configurations
- **Reproducibility**: Share track designs as code
- **Automation**: Generate tracks based on specific criteria or algorithms

## Quick Start

```python
from gym_donkeycar.core import TrackBuilder

# Create a simple track
builder = TrackBuilder(name="my_track", width=4.0)
builder.add_straight(100.0)  # 100m straight
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")  # 90° left turn
builder.add_straight(50.0)   # 50m straight

# Get the track configuration
track_config = builder.build()
print(track_config)

# Save to file
builder.save("my_track.json")
```

## Track Segments

### Straight Segment

A straight section of track.

```python
builder.add_straight(length=100.0)
```

**Parameters:**
- `length`: Length of the straight section in meters

### Curve Segment

A curved section of track.

```python
builder.add_curve(length=31.4, radius=20.0, angle=90.0, direction="left")
```

**Parameters:**
- `length`: Arc length of the curve in meters
- `radius`: Radius of the curve in meters
- `angle`: Angle of the curve in degrees
- `direction`: Direction of the curve ('left' or 'right')

**Note:** For a circular arc, length = (π × radius × angle) / 180

### Elevation Segment

A section with elevation change (uphill or downhill).

```python
builder.add_elevation(length=50.0, height_change=10.0, gradient=15.0)
```

**Parameters:**
- `length`: Length of the segment in meters
- `height_change`: Height change in meters (positive for uphill, negative for downhill)
- `gradient`: Optional gradient angle in degrees

## Method Chaining

The TrackBuilder supports method chaining for concise track definitions:

```python
track = (TrackBuilder(name="oval", width=4.0)
    .add_straight(100.0)
    .add_curve(47.1, radius=30.0, angle=90.0, direction="left")
    .add_straight(100.0)
    .add_curve(47.1, radius=30.0, angle=90.0, direction="left")
    .build())
```

## Predefined Track Templates

The module includes several predefined track templates:

### Simple Oval

```python
from gym_donkeycar.core import create_simple_oval

track = create_simple_oval(length=100.0, width=60.0, track_width=4.0)
```

### Figure Eight

```python
from gym_donkeycar.core import create_figure_eight

track = create_figure_eight(size=50.0, track_width=4.0)
```

### S-Curve

```python
from gym_donkeycar.core import create_s_curve

track = create_s_curve(straight_length=50.0, curve_radius=25.0, track_width=4.0)
```

## Saving and Loading Tracks

### Save to JSON

```python
builder = TrackBuilder(name="my_track")
builder.add_straight(100.0)
builder.save("my_track.json")
```

### Load from JSON

```python
builder = TrackBuilder.load("my_track.json")
track_config = builder.build()
```

### Export to JSON string

```python
json_string = builder.to_json(indent=2)
print(json_string)
```

## Complete Examples

### Example 1: Simple Rectangular Track

```python
from gym_donkeycar.core import TrackBuilder

builder = TrackBuilder(name="rectangle", width=4.0)

# Create a 100m x 60m rectangular track
builder.add_straight(100.0)
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")
builder.add_straight(60.0)
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")
builder.add_straight(100.0)
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")
builder.add_straight(60.0)
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")

track = builder.build()
print(f"Total length: {track['total_length']:.2f} meters")
```

### Example 2: Track with Elevation Changes

```python
from gym_donkeycar.core import TrackBuilder

builder = TrackBuilder(name="hilly_track", width=4.0)

# Flat start
builder.add_straight(50.0)

# Uphill section
builder.add_elevation(40.0, height_change=10.0, gradient=15.0)

# Flat at the top
builder.add_straight(30.0)

# Downhill section
builder.add_elevation(40.0, height_change=-10.0, gradient=-15.0)

# Curve back
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")
builder.add_straight(50.0)

track = builder.build()
```

### Example 3: Complex Racing Circuit

```python
from gym_donkeycar.core import TrackBuilder

builder = TrackBuilder(name="grand_prix", width=6.0)

# Start/finish straight
builder.add_straight(200.0)

# Chicane
builder.add_curve(15.7, radius=10.0, angle=45.0, direction="right")
builder.add_straight(20.0)
builder.add_curve(15.7, radius=10.0, angle=45.0, direction="left")

# Back straight with elevation
builder.add_elevation(100.0, height_change=12.0)
builder.add_straight(80.0)
builder.add_elevation(100.0, height_change=-12.0)

# Hairpin turn
builder.add_curve(47.1, radius=15.0, angle=180.0, direction="left")

# Return to start
builder.add_straight(150.0)
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="right")
builder.add_straight(100.0)
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="right")

track = builder.build()
```

## Running the Examples

Run the included example script to see all the features in action:

```bash
python examples/create_custom_track.py
```

This will generate several track configurations and save them to `/tmp/`.

## Track Configuration Format

The `build()` method returns a dictionary with the following structure:

```python
{
    "name": "track_name",
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

## Advanced Usage

### Custom Segments

You can create custom segment types by extending the `TrackSegment` class:

```python
from gym_donkeycar.core import TrackSegment

class BankedCurveSegment(TrackSegment):
    def __init__(self, length, radius, angle, direction, banking_angle):
        super().__init__(length)
        self.segment_type = "banked_curve"
        self.radius = radius
        self.angle = angle
        self.direction = direction
        self.banking_angle = banking_angle
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "radius": self.radius,
            "angle": self.angle,
            "direction": self.direction,
            "banking_angle": self.banking_angle
        })
        return data

# Use the custom segment
builder = TrackBuilder()
custom_segment = BankedCurveSegment(31.4, 20.0, 90.0, "left", 15.0)
builder.add_segment(custom_segment)
```

### Procedural Track Generation

Generate random tracks:

```python
import random
from gym_donkeycar.core import TrackBuilder

def generate_random_track(num_segments=10):
    builder = TrackBuilder(name="random_track", width=4.0)
    
    for i in range(num_segments):
        segment_type = random.choice(["straight", "curve"])
        
        if segment_type == "straight":
            length = random.uniform(30.0, 100.0)
            builder.add_straight(length)
        else:
            radius = random.uniform(15.0, 40.0)
            angle = random.uniform(30.0, 120.0)
            direction = random.choice(["left", "right"])
            length = (3.14159 * radius * angle) / 180.0
            builder.add_curve(length, radius, angle, direction)
    
    return builder.build()

track = generate_random_track()
```

## Integration with Simulator

**Note:** The Track Builder generates track configuration data in JSON format. To use these tracks with the Donkey Car simulator:

1. The track configuration describes the geometry of the track
2. These configurations can be used to:
   - Generate track meshes in Unity
   - Create procedural track generators
   - Define waypoints for pathfinding
   - Store and share track designs

The JSON format is designed to be extensible and can be adapted for different track generation systems or simulators.

## API Reference

### Classes

- `TrackBuilder`: Main class for building tracks
- `TrackSegment`: Base class for track segments
- `StraightSegment`: Straight track segment
- `CurveSegment`: Curved track segment
- `ElevationSegment`: Segment with elevation change

### Functions

- `create_simple_oval()`: Create a simple oval track
- `create_figure_eight()`: Create a figure-eight track
- `create_s_curve()`: Create an S-curve track

For detailed API documentation, see the docstrings in the source code.
