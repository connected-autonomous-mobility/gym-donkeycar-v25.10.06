# Examples

some sample code to use the gym-donkeycar environment

## Sample Track Visualization

A high-resolution sample track visualization is included to showcase the matplotlib visualization capabilities:

**[sample_track_visualization.png](sample_track_visualization.png)** - 300 DPI example racing circuit

The sample track (`sample_track.json`) demonstrates:
- Complex racing circuit with 8 segments
- Combination of straights, curves, and a hairpin turn
- 588.5 meters total length
- Professional visualization with boundaries, center line, and segment labels

You can regenerate this visualization with:
```bash
python visualize_track_matplotlib.py sample_track.json --save sample_track_visualization.png --dpi 300
```

## gym_test.py

Some minimal code to load the gym-donkeycar environment and test

## create_custom_track.py

Comprehensive examples showing how to create custom tracks programmatically using the Track Builder API. Includes:
- Simple rectangular tracks
- Method chaining
- Tracks with elevation changes
- Predefined track templates (oval, figure-eight, S-curve)
- Saving and loading track configurations
- Complex racing circuits

## visualize_track.py

Basic track visualization from JSON files. Displays:
- 2D top-down ASCII visualization of the track layout
- Detailed track statistics (length, width, segments)
- Individual segment information (type, length, angles, etc.)
- Summary of segment types

Usage:
```bash
# Create a track
python -c "from gym_donkeycar.core import create_simple_oval; import json; \
           track = create_simple_oval(); \
           json.dump(track, open('my_track.json', 'w'), indent=2)"

# Visualize it
python visualize_track.py my_track.json
```

## visualize_track_matplotlib.py

**Professional track visualization using matplotlib** - Creates high-quality graphical plots. Features:
- **Left and right track boundaries** with clear lines
- **Center line** (dashed red line)
- **Shaded track surface** (filled polygon between boundaries)
- **Segment IDs** with labels showing segment types
- **Start position marker** (green dot)
- **Track statistics** displayed on plot
- **Grid lines** for reference
- **Export to PNG/PDF** with customizable DPI

Requirements:
```bash
pip install matplotlib
```

Usage:
```bash
# Display interactive plot
python visualize_track_matplotlib.py my_track.json

# Save to file
python visualize_track_matplotlib.py my_track.json --save my_track.png

# High resolution output
python visualize_track_matplotlib.py my_track.json --save my_track.png --dpi 300
```

## visualize_track_enhanced.py

**Enhanced ASCII track visualization** with detailed boundaries and styling. Shows:
- **Left and right track boundaries** (clear edge markers)
- **Center line** (dashed line down the middle)
- **Shaded track surface** (filled area between boundaries)
- **Segment IDs** (numbered markers for each segment)
- **Clear boundary visualization** (distinguishable track edges)

Usage:
```bash
# Basic usage
python visualize_track_enhanced.py my_track.json

# Custom dimensions
python visualize_track_enhanced.py my_track.json --width 100 --height 50
```

See also: [Track Builder Quick Start Guide](TRACK_BUILDER_QUICKSTART.md)

## reinforcement_learning

A dir of sample code of [reinforcement learning](https://github.com/tawnkramer/gym-donkeycar/tree/master/examples/reinforcement_learning) with gym-donkeycar

## supervised_learning

A dir of sample code of [supervised learning](https://github.com/tawnkramer/gym-donkeycar/tree/master/examples/supervised_learning) with gym-donkeycar

