# Examples

Sample code demonstrating gym-donkeycar environment usage and Track Builder API

## 📚 Track Builder Documentation

For complete documentation on creating custom tracks, see:
- **[Documentation Index](../docs/TRACK_BUILDER_INDEX.md)** - Navigate all Track Builder documentation
- **[Getting Started Guide](../docs/TRACK_BUILDER_GETTING_STARTED.md)** - Step-by-step tutorial
- **[API Reference](../docs/TRACK_BUILDER_API_REFERENCE.md)** - Complete API documentation
- **[PRD](../docs/TRACK_BUILDER_PRD.md)** - Product vision and requirements
- **[Quick Reference](TRACK_BUILDER_QUICKSTART.md)** - One-page cheat sheet

## Sample Track Visualization

A high-resolution sample track visualization is included to showcase the matplotlib visualization capabilities:

**[sample_track_visualization.png](sample_track_visualization.png)** - 300 DPI example racing circuit

The sample track (`sample_track.json`) demonstrates:
- Complex racing circuit with 8 segments
- Combination of straights, curves, and a hairpin turn
- 588.5 meters total length
- Professional visualization with boundaries, center line, and segment labels

### Using sample_track.json

**Important:** The JSON file is a track geometry specification, not directly loadable in the pre-built simulator. Use it for:

1. **Visualization:**
   ```bash
   python visualize_track_matplotlib.py sample_track.json --save my_visualization.png --dpi 300
   ```

2. **As a blueprint for Unity development:**
   - Load the JSON to understand track layout
   - Use the segment data to build track geometry in Unity
   - See [Simulator Integration Guide](../docs/TRACK_BUILDER_SIMULATOR_GUIDE.md) for details

3. **Track design reference:**
   ```python
   import json
   with open('sample_track.json') as f:
       track = json.load(f)
   
   # Inspect segments for implementation
   for seg in track['segments']:
       print(f"{seg['type']}: {seg['length']}m")
   ```

**To run in the simulator:** Use built-in tracks like `donkey-generated-track-v0` or build a custom Unity scene following the [Simulator Integration Guide](../docs/TRACK_BUILDER_SIMULATOR_GUIDE.md).

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

## visualize_track_matplotlib.py

**Professional track visualization using matplotlib** - Creates high-quality graphical plots from JSON track files. Features:
- **Left and right track boundaries** with clear lines
- **Center line** (dashed red line)
- **Shaded track surface** (filled polygon between boundaries)
- **Segment IDs** with labels showing segment types
- **Start position marker** (green dot)
- **Track statistics** displayed on plot
- **Grid lines** for reference
- **Export to PNG/PDF/SVG** with customizable DPI

Requirements:
```bash
pip install matplotlib
# or
pip install gym-donkeycar[viz]
```

Usage:
```bash
# Create a track
python -c "from gym_donkeycar.core import create_simple_oval; import json; \
           track = create_simple_oval(); \
           json.dump(track, open('my_track.json', 'w'), indent=2)"

# Display interactive plot
python visualize_track_matplotlib.py my_track.json

# Save to file
python visualize_track_matplotlib.py my_track.json --save my_track.png

# High resolution output (300 DPI)
python visualize_track_matplotlib.py my_track.json --save my_track.png --dpi 300

# Disable grid
python visualize_track_matplotlib.py my_track.json --no-grid
```

See also: [Track Builder Quick Start Guide](TRACK_BUILDER_QUICKSTART.md)

## reinforcement_learning

A dir of sample code of [reinforcement learning](https://github.com/tawnkramer/gym-donkeycar/tree/master/examples/reinforcement_learning) with gym-donkeycar

## supervised_learning

A dir of sample code of [supervised learning](https://github.com/tawnkramer/gym-donkeycar/tree/master/examples/supervised_learning) with gym-donkeycar

