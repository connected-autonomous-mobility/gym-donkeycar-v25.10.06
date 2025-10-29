# Examples

some sample code to use the gym-donkeycar environment

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

Visualize track configurations from JSON files. Displays:
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

See also: [Track Builder Quick Start Guide](TRACK_BUILDER_QUICKSTART.md)

## reinforcement_learning

A dir of sample code of [reinforcement learning](https://github.com/tawnkramer/gym-donkeycar/tree/master/examples/reinforcement_learning) with gym-donkeycar

## supervised_learning

A dir of sample code of [supervised learning](https://github.com/tawnkramer/gym-donkeycar/tree/master/examples/supervised_learning) with gym-donkeycar

