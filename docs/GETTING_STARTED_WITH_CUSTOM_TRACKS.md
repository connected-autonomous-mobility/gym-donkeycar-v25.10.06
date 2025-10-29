# Getting Started with Custom Tracks

This guide walks you through the complete process of creating and running custom tracks in the Donkey Car simulator, from installation to execution.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Install the Simulator](#step-1-install-the-simulator)
3. [Step 2: Install gym-donkeycar](#step-2-install-gym-donkeycar)
4. [Step 3: Create a Custom Track](#step-3-create-a-custom-track)
5. [Step 4: Visualize Your Track](#step-4-visualize-your-track)
6. [Step 5: Run in the Simulator](#step-5-run-in-the-simulator)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.7 or later
- Operating System: Windows, macOS, or Linux
- Basic Python knowledge

## Step 1: Install the Simulator

### Download the Simulator

1. Go to the [gym-donkeycar releases page](https://github.com/tawnkramer/gym-donkeycar/releases)
2. Download the appropriate simulator binary for your platform:
   - **Windows**: `DonkeySimWin.zip`
   - **macOS**: `DonkeySimMac.zip`
   - **Linux**: `DonkeySimLinux.zip`

3. Extract the downloaded file to a directory of your choice

### Verify Installation

Run the simulator executable:
- **Windows**: Double-click `donkey_sim.exe`
- **macOS**: Open `donkey_sim.app`
- **Linux**: Run `./donkey_sim.x86_64`

You should see the simulator window open with a menu to select different tracks.

## Step 2: Install gym-donkeycar

### Install from PyPI

```bash
pip install gym-donkeycar
```

### Or Install from Source

```bash
git clone https://github.com/tawnkramer/gym-donkeycar
cd gym-donkeycar
pip install -e .
```

### Verify Installation

```bash
python -c "import gym_donkeycar; print('Successfully installed gym-donkeycar')"
```

## Step 3: Create a Custom Track

### Option A: Use Predefined Templates (Easiest)

Create a simple oval track:

```python
from gym_donkeycar.core import create_simple_oval

# Create an oval track
track = create_simple_oval(length=100.0, width=60.0, track_width=4.0)

# Save to file
import json
with open("my_oval_track.json", "w") as f:
    json.dump(track, f, indent=2)

print(f"Created track with {track['num_segments']} segments")
print(f"Total length: {track['total_length']:.2f} meters")
```

### Option B: Build a Custom Track

Create a custom track with straights, curves, and elevation:

```python
from gym_donkeycar.core import TrackBuilder

# Initialize the builder
builder = TrackBuilder(name="my_custom_track", width=4.0)

# Add track segments
builder.add_straight(100.0)  # 100m straight
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")  # Left turn
builder.add_straight(60.0)   # 60m straight
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")  # Left turn
builder.add_elevation(50.0, height_change=10.0)  # Uphill section
builder.add_straight(40.0)   # 40m straight at elevation
builder.add_elevation(50.0, height_change=-10.0)  # Downhill section

# Build and save
track = builder.build()
builder.save("my_custom_track.json")

print(f"Created custom track: {track['name']}")
print(f"Segments: {track['num_segments']}")
print(f"Total length: {track['total_length']:.2f} meters")
```

### Option C: Quick Track with Method Chaining

```python
from gym_donkeycar.core import TrackBuilder

track = (TrackBuilder(name="racing_circuit", width=6.0)
    .add_straight(150.0)
    .add_curve(47.1, radius=30.0, angle=90.0, direction="right")
    .add_straight(100.0)
    .add_curve(47.1, radius=30.0, angle=90.0, direction="right")
    .add_straight(150.0)
    .add_curve(47.1, radius=30.0, angle=90.0, direction="right")
    .add_straight(100.0)
    .add_curve(47.1, radius=30.0, angle=90.0, direction="right")
    .build())

# Save to file
import json
with open("racing_circuit.json", "w") as f:
    json.dump(track, f, indent=2)
```

## Step 4: Visualize Your Track

Use the included visualization script to see your track:

```bash
python examples/visualize_track.py my_custom_track.json
```

This will display:
- A 2D top-down view of the track
- Track statistics (length, number of segments, etc.)
- Individual segment details

See the [Track Visualization](#track-visualization) section below for more details.

## Step 5: Run in the Simulator

### Understanding Track JSON Format

The Track Builder creates JSON files that describe track geometry. These files contain:
- Track metadata (name, width, start position)
- Segment definitions (straight, curve, elevation)
- Total length and segment count

**Important Note:** The current Donkey Car simulator uses pre-built Unity scenes. The JSON track files created by the Track Builder API define track geometry that can be:
1. Used as specifications for creating Unity scene tracks
2. Loaded by custom track generation systems
3. Used for procedural track generation tools
4. Shared as track design blueprints

### Running with Existing Simulator Tracks

To run the car in the simulator with existing tracks:

```python
import gym
import gym_donkeycar
import numpy as np

# Configuration
exe_path = "/path/to/your/donkey_sim.exe"  # Update this path
port = 9091

conf = {
    "exe_path": exe_path,
    "port": port,
    "body_style": "donkey",
    "body_rgb": (128, 128, 128),
    "car_name": "MyRacer",
    "font_size": 100,
}

# Create environment with a built-in track
env = gym.make("donkey-generated-track-v0", conf=conf)

# Reset and run
obs = env.reset()
for step in range(1000):
    # Simple forward action
    action = np.array([0.0, 0.5])  # [steering, throttle]
    obs, reward, done, info = env.step(action)
    
    if done:
        print(f"Episode finished at step {step}")
        print(f"Final position: {info['pos']}")
        break

env.close()
```

### Future: Using Custom Tracks

The Track Builder API prepares track definitions for future use. To use custom tracks in the simulator, you would need:

1. **A custom track loader plugin** for the Unity simulator
2. **A procedural track generator** that reads JSON and creates Unity scenes
3. **Integration with track generation tools** that accept the JSON format

Example workflow (future):
```python
# This is the intended future workflow
from gym_donkeycar.core import TrackBuilder
import gym
import gym_donkeycar

# Create custom track
builder = TrackBuilder(name="my_track")
builder.add_straight(100.0).add_curve(31.4, 20.0, 90.0, "left")
track_config = builder.build()

# Future: Load custom track in simulator
conf = {
    "exe_path": "/path/to/donkey_sim.exe",
    "port": 9091,
    "custom_track": track_config,  # Future feature
}
env = gym.make("donkey-custom-track-v0", conf=conf)
```

## Track Visualization

### Using the Visualization Script

The Track Builder includes a visualization script that displays your track:

```bash
# Visualize a track file
python examples/visualize_track.py my_custom_track.json

# Create and visualize in one command
python -c "
from gym_donkeycar.core import create_simple_oval
import json

track = create_simple_oval(length=100.0, width=60.0)
with open('temp_track.json', 'w') as f:
    json.dump(track, f)
print('Track saved to temp_track.json')
print('Run: python examples/visualize_track.py temp_track.json')
"
```

The visualization shows:
- Track layout in 2D
- Segment types (straight, curve, elevation)
- Measurements and angles
- Start/finish position

## Example: Complete Workflow

Here's a complete example from track creation to simulation:

```python
"""
complete_workflow.py - Create a track and run simulation
"""
import gym
import gym_donkeycar
import numpy as np
from gym_donkeycar.core import TrackBuilder

# Step 1: Create a custom track
print("Creating custom track...")
track = (TrackBuilder(name="test_circuit", width=5.0)
    .add_straight(80.0)
    .add_curve(31.4, 20.0, 90.0, "left")
    .add_straight(60.0)
    .add_curve(31.4, 20.0, 90.0, "left")
    .add_straight(80.0)
    .add_curve(31.4, 20.0, 90.0, "left")
    .add_straight(60.0)
    .add_curve(31.4, 20.0, 90.0, "left")
    .build())

# Save track configuration
import json
with open("test_circuit.json", "w") as f:
    json.dump(track, f, indent=2)

print(f"✓ Track created: {track['name']}")
print(f"  Length: {track['total_length']:.2f}m")
print(f"  Segments: {track['num_segments']}")
print(f"✓ Saved to: test_circuit.json")

# Step 2: Visualize (optional)
print("\nVisualize with: python examples/visualize_track.py test_circuit.json")

# Step 3: Run in simulator (using built-in track for now)
print("\nStarting simulator...")
conf = {
    "exe_path": "/path/to/donkey_sim.exe",  # Update this
    "port": 9091,
}

# Use a built-in track (custom track loading is a future feature)
env = gym.make("donkey-generated-track-v0", conf=conf)

obs = env.reset()
print("✓ Simulator started")

# Simple drive loop
for i in range(100):
    action = np.array([0.0, 0.3])  # Drive straight slowly
    obs, reward, done, info = env.step(action)
    
    if i % 20 == 0:
        print(f"  Step {i}: position={info['pos']}, speed={info['speed']:.2f}")
    
    if done:
        break

env.close()
print("\n✓ Complete!")
```

## Troubleshooting

### Simulator Won't Start

**Problem:** Simulator executable doesn't launch

**Solutions:**
- Ensure you extracted the full contents of the zip file
- On Linux, make the file executable: `chmod +x donkey_sim.x86_64`
- On macOS, allow the app in System Preferences → Security & Privacy
- Check that you have sufficient GPU/graphics capabilities

### Connection Errors

**Problem:** Python script can't connect to simulator

**Solutions:**
- Ensure the simulator is running before starting your Python script
- Check that the port number matches (default: 9091)
- Verify firewall settings aren't blocking the connection
- Try using `host="127.0.0.1"` in the conf dictionary

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'gym_donkeycar'`

**Solutions:**
```bash
# Reinstall gym-donkeycar
pip install --upgrade gym-donkeycar

# Or install from source
git clone https://github.com/tawnkramer/gym-donkeycar
cd gym-donkeycar
pip install -e .
```

### Track Builder Issues

**Problem:** Track Builder import fails

**Solutions:**
```bash
# Ensure you have the latest version
pip install --upgrade gym-donkeycar

# Verify Track Builder is available
python -c "from gym_donkeycar.core import TrackBuilder; print('Track Builder OK')"
```

## Next Steps

- Read the [Track Builder API Documentation](TRACK_BUILDER.md) for advanced features
- Check out [Track Builder Quick Start](../examples/TRACK_BUILDER_QUICKSTART.md)
- Explore [example scripts](../examples/create_custom_track.py)
- Experiment with procedural track generation
- Share your track designs as JSON files

## Additional Resources

- [Donkey Car Documentation](http://docs.donkeycar.com/)
- [OpenAI Gym Documentation](https://gym.openai.com/)
- [gym-donkeycar GitHub](https://github.com/tawnkramer/gym-donkeycar)
- [Simulator Releases](https://github.com/tawnkramer/gym-donkeycar/releases)

## Need Help?

- Create an issue on [GitHub](https://github.com/tawnkramer/gym-donkeycar/issues)
- Check existing issues for solutions
- Review the examples folder for working code

Happy racing! 🏎️
