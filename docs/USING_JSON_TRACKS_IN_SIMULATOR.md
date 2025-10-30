# Using JSON Track Files in the Donkey Car Simulator

This guide explains how to use the JSON track files created by the Track Builder API with the Donkey Car simulator.

## Quick Answer

**Can I load JSON tracks directly in the pre-built simulator?**

**No, not without modifications.** The pre-built Donkey Car simulator binaries use pre-baked Unity scenes and cannot dynamically load JSON track files. However, there are several ways to use these JSON files effectively.

## What Are JSON Track Files?

The Track Builder API creates JSON files that are **track geometry specifications**. They describe:
- Track layout (segments, curves, straights, elevation)
- Dimensions (width, length, radii)
- Metadata (name, start position)

These files serve as:
- 📊 **Blueprints** for track design
- 📈 **Specifications** for Unity implementation
- 🎨 **Visualization** sources for track plots
- 📝 **Documentation** of track layouts
- 🤝 **Sharing format** for track designs

## Current Simulator Architecture

```
Pre-built Simulator Binary
  └─ Unity Scenes (baked into executable)
      ├─ warehouse
      ├─ generated-track
      ├─ mountain-track
      └─ ... other scenes
```

The simulator loads scenes that are compiled into the executable. It does **not** have a runtime JSON loader.

## Options for Using JSON Tracks

### Option 1: Visualize and Plan (No Build Required) ✅

Use the JSON files with visualization tools:

```bash
# Create high-quality plots
python examples/visualize_track_matplotlib.py sample_track.json --save track.png --dpi 300

# View in terminal
python examples/visualize_track.py sample_track.json

# Enhanced visualization
python examples/visualize_track_enhanced.py sample_track.json --width 100 --height 50
```

**Use cases:**
- Documentation and presentations
- Track design iteration
- Team collaboration and review
- Research papers and reports

### Option 2: Use as Blueprint for Unity (Requires Unity) 🔧

Convert JSON specifications to Unity scenes:

**Steps:**
1. Install Unity (2020.3 LTS or compatible)
2. Clone [Donkey Simulator source](https://github.com/tawnkramer/sdsandbox)
3. Load JSON and create track geometry:

```python
import json

# Load your track design
with open('sample_track.json') as f:
    track = json.load(f)

print(f"Building track: {track['name']}")
print(f"Track width: {track['width']}m")

# Implement each segment in Unity
for i, segment in enumerate(track['segments'], 1):
    print(f"\n=== Segment {i}: {segment['type'].upper()} ===")
    print(f"Length: {segment['length']}m")
    
    if segment['type'] == 'straight':
        print("→ Create straight road section")
        
    elif segment['type'] == 'curve':
        print(f"→ Create curved section:")
        print(f"  Radius: {segment['radius']}m")
        print(f"  Angle: {segment['angle']}°")
        print(f"  Direction: {segment['direction']}")
        print(f"  Arc length: {segment['length']}m")
        
    elif segment['type'] == 'elevation':
        print(f"→ Create elevation change:")
        print(f"  Height change: {segment.get('height_change', 0)}m")
        if segment.get('gradient'):
            print(f"  Gradient: {segment['gradient']}°")
```

4. Use Unity ProBuilder or terrain tools to create geometry
5. Build the simulator with your custom track

**Resources:**
- [Unity Documentation](https://docs.unity3d.com/)
- [Donkey Sim Unity Project](https://github.com/tawnkramer/sdsandbox)
- [ProBuilder](https://unity.com/features/probuilder) for track geometry

### Option 3: Use Built-in Simulator Tracks (No Build Required) ✅

The simulator includes many pre-built tracks you can use immediately:

```python
import gym
import gym_donkeycar
import numpy as np

# Available tracks (no JSON loading needed)
track_envs = [
    "donkey-warehouse-v0",
    "donkey-generated-roads-v0",
    "donkey-avc-sparkfun-v0",
    "donkey-generated-track-v0",
    "donkey-roboracingleague-track-v0",
    "donkey-waveshare-v0",
    "donkey-minimonaco-track-v0",
    "donkey-warren-track-v0",
    "donkey-thunderhill-track-v0",
    "donkey-circuit-launch-track-v0",
]

# Run with built-in track
exe_path = "/path/to/donkey_sim.exe"
conf = {"exe_path": exe_path, "port": 9091}

env = gym.make("donkey-generated-track-v0", conf=conf)
obs = env.reset()

for step in range(1000):
    action = np.array([0.0, 0.5])  # [steering, throttle]
    obs, reward, done, info = env.step(action)
    if done:
        break

env.close()
```

### Option 4: Future Procedural Generation (Development Required) 🚀

A future enhancement could add runtime JSON loading:

**Concept:**
```python
# Hypothetical future API
from gym_donkeycar.core import TrackBuilder
import gym
import gym_donkeycar

# Create track
builder = TrackBuilder(name="my_track")
builder.add_straight(100.0).add_curve(31.4, 20.0, 90.0, "left")
track_config = builder.build()

# Load in simulator (requires custom plugin)
conf = {
    "exe_path": "/path/to/donkey_sim.exe",
    "port": 9091,
    "custom_track": track_config,  # Future feature
}
env = gym.make("donkey-custom-track-v0", conf=conf)
```

**Requirements:**
- Unity plugin for procedural track generation
- Runtime mesh generation from JSON specs
- Track builder component in simulator
- Physics and collision setup

## Example: Using sample_track.json

The included `examples/sample_track.json` is a complete example:

```bash
# 1. Visualize the track
python examples/visualize_track_matplotlib.py examples/sample_track.json --save my_track.png

# 2. Inspect the specification
python -c "
import json
with open('examples/sample_track.json') as f:
    track = json.load(f)
print(f'Track: {track[\"name\"]}')
print(f'Length: {track[\"total_length\"]}m')
print(f'Width: {track[\"width\"]}m')
print(f'Segments: {track[\"num_segments\"]}')
for i, seg in enumerate(track['segments'], 1):
    print(f'{i}. {seg[\"type\"]}: {seg[\"length\"]}m')
"

# 3. Use as blueprint for Unity development
# (Follow Option 2 above)

# 4. Run simulator with built-in track for testing
python -c "
import gym
import gym_donkeycar
import numpy as np

exe_path = '/path/to/donkey_sim.exe'  # Update this
conf = {'exe_path': exe_path, 'port': 9091}
env = gym.make('donkey-generated-track-v0', conf=conf)

obs = env.reset()
for step in range(100):
    action = np.array([0.0, 0.5])
    obs, reward, done, info = env.step(action)
    if done:
        break
env.close()
print('Simulator test complete!')
"
```

## Comparison Table

| Method | Build Required? | JSON Support | Difficulty | Use Case |
|--------|-----------------|--------------|------------|----------|
| Visualize Only | ❌ No | ✅ Full | ⭐ Easy | Design & documentation |
| Built-in Tracks | ❌ No | ❌ No | ⭐ Easy | Quick testing & training |
| Unity Custom Scene | ✅ Yes | 📋 Blueprint | ⭐⭐⭐ Hard | Custom track implementation |
| Future Procedural | ✅ Yes | ✅ Full | ⭐⭐⭐⭐ Very Hard | Runtime track loading |

## Why This Architecture?

**Advantages of pre-built scenes:**
- Fast loading and rendering
- Optimized physics and collisions
- Stable performance
- No runtime errors from invalid geometry

**Limitations:**
- Cannot load tracks dynamically
- Requires rebuild to add new tracks
- Less flexible for experimentation

## Frequently Asked Questions

**Q: Can I modify the simulator to load JSON tracks?**

A: Yes, but it requires Unity development. You would need to:
1. Clone the simulator source code
2. Create a JSON parser in Unity (C#)
3. Build procedural track generation system
4. Compile a new simulator binary

**Q: Will future versions support JSON loading?**

A: This would require significant development effort. Consider contributing to the [Donkey Car project](https://github.com/tawnkramer/gym-donkeycar) if you're interested in this feature.

**Q: What's the best workflow for custom tracks today?**

A: 
1. Design track with Track Builder API
2. Visualize with matplotlib
3. Use visualization as reference to build Unity scene
4. Compile custom simulator with your track

**Q: Can I share my track designs?**

A: Yes! Share the JSON files. Others can:
- Visualize them
- Use as blueprints for Unity
- Modify and extend the designs

## Next Steps

- **Design tracks:** Use the [Track Builder API](TRACK_BUILDER.md)
- **Visualize:** Try the [visualization tools](../examples/README.md)
- **Build in Unity:** Follow the [Donkey Sim documentation](https://docs.donkeycar.com/guide/simulator/)
- **Get started:** Read the [Getting Started Guide](GETTING_STARTED_WITH_CUSTOM_TRACKS.md)

## Contributing

Interested in adding JSON track loading to the simulator? The project welcomes contributions:
- [Donkey Car GitHub](https://github.com/tawnkramer/gym-donkeycar)
- [Simulator Source](https://github.com/tawnkramer/sdsandbox)

Consider implementing a procedural track generator plugin for Unity that reads Track Builder JSON files!
