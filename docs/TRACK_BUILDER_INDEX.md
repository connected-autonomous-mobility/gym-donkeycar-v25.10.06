# Track Builder API - Documentation Index

Welcome to the Track Builder API documentation! This guide helps you navigate the complete documentation suite.

---

## 📚 Documentation Structure

### 1. 📋 [Product Requirements Document (PRD)](TRACK_BUILDER_PRD.md)
**Audience**: Product managers, architects, technical leadership, contributors

**Purpose**: Comprehensive overview of product vision, requirements, architecture, and implementation

**Contents**:
- Executive summary and problem statement
- Product vision and target users
- Functional and non-functional requirements
- Technical architecture and design patterns
- Implementation details and code structure
- Testing strategy and coverage
- Current limitations and future roadmap
- Success metrics and release notes

**When to Read**: 
- Understanding the big picture
- Contributing to the project
- Planning extensions or integrations
- Writing research papers about the project

---

### 2. 🚀 [Getting Started Guide](TRACK_BUILDER_GETTING_STARTED.md)
**Audience**: End users, beginners, first-time users

**Purpose**: Quick start guide to create your first track

**Contents**:
- Installation instructions (with/without visualization)
- Prerequisites and dependencies
- Step-by-step track creation tutorial
- Visualization workflow
- Common usage patterns
- Troubleshooting guide
- FAQ

**When to Read**:
- First time using Track Builder
- Quick reference for common tasks
- Installation problems
- Basic usage questions

---

### 3. 📖 [API Reference](TRACK_BUILDER_API_REFERENCE.md)
**Audience**: Developers, power users, integration developers

**Purpose**: Complete reference for all classes, methods, and functions

**Contents**:
- `TrackBuilder` class documentation
- Segment types (`StraightSegment`, `CurveSegment`, `ElevationSegment`)
- Template functions (`create_simple_oval`, `create_figure_eight`, `create_s_curve`)
- Method signatures and parameters
- Return types and exceptions
- Usage examples for each method
- JSON schema specification

**When to Read**:
- Writing code with Track Builder
- Understanding specific method behavior
- Looking up parameter requirements
- Implementing custom extensions

---

### 4. 🎮 [Simulator Integration Guide](TRACK_BUILDER_SIMULATOR_GUIDE.md)
**Audience**: Advanced users, Unity developers, simulator integrators

**Purpose**: Understanding how JSON tracks relate to the Donkey Car simulator

**Contents**:
- Simulator architecture explanation
- JSON track limitations and alternatives
- Options for using tracks without building from source
- Complete Unity development workflow
- Building custom simulator with JSON support
- Practical examples and workarounds

**When to Read**:
- Planning to use tracks in simulator
- Understanding JSON vs. Unity scenes
- Developing Unity track implementations
- Building simulator from source

---

## 🎯 Quick Navigation by Task

### "I want to create my first track"
→ Start with [Getting Started Guide](TRACK_BUILDER_GETTING_STARTED.md)

### "I need API details for a specific method"
→ Check [API Reference](TRACK_BUILDER_API_REFERENCE.md)

### "I want to understand the product vision"
→ Read [PRD](TRACK_BUILDER_PRD.md)

### "I want to use tracks in the simulator"
→ See [Simulator Guide](TRACK_BUILDER_SIMULATOR_GUIDE.md)

### "I want to contribute to the project"
→ Start with [PRD](TRACK_BUILDER_PRD.md), then [API Reference](TRACK_BUILDER_API_REFERENCE.md)

---

## 💡 Example Code Snippets

### Quick Start Example

```python
from gym_donkeycar.core import TrackBuilder, create_simple_oval

# Create a simple oval track
track = create_simple_oval(length=100.0, width=60.0)

# Build a custom track
builder = TrackBuilder(name="my_circuit", width=6.0)
builder.add_straight(150.0)
builder.add_curve(31.4, radius=20.0, angle=90.0, direction="left")
builder.add_straight(120.0)
track = builder.build()

# Save to JSON
builder.save("my_track.json")
```

### Visualization Example

```bash
# Install matplotlib
pip install matplotlib

# Visualize track
python examples/visualize_track_matplotlib.py my_track.json

# Save high-resolution image
python examples/visualize_track_matplotlib.py my_track.json --save track.png --dpi 300
```

---

## 📁 Additional Resources

### Code Examples
- **[examples/create_custom_track.py](../examples/create_custom_track.py)** - Comprehensive usage examples
- **[examples/sample_track.json](../examples/sample_track.json)** - Example track configuration
- **[examples/sample_track_visualization.png](../examples/sample_track_visualization.png)** - Example visualization output (300 DPI)

### Visualization Tool
- **[examples/visualize_track_matplotlib.py](../examples/visualize_track_matplotlib.py)** - Professional track visualization

### Tests
- **[tests/test_track_builder.py](../tests/test_track_builder.py)** - Comprehensive test suite (317 lines)

### Quick Reference
- **[examples/TRACK_BUILDER_QUICKSTART.md](../examples/TRACK_BUILDER_QUICKSTART.md)** - One-page quick reference

---

## 🔗 External Links

- **GitHub Repository**: [gym-donkeycar-v25.10.06](https://github.com/connected-autonomous-mobility/gym-donkeycar-v25.10.06)
- **Donkey Car Project**: [donkeycar.com](https://www.donkeycar.com/)
- **Unity Simulator Source**: [sdsandbox](https://github.com/tawnkramer/sdsandbox)
- **OpenAI Gym**: [gym.openai.com](https://gym.openai.com/)

---

## 📊 Documentation Statistics

- **Total Documentation**: 4 comprehensive guides + 1 PRD + 1 index
- **Total Lines**: ~2,500 lines of documentation
- **Code Examples**: 15+ complete examples
- **API Methods**: 10+ documented methods
- **Test Coverage**: 100% for core functionality

---

## 🆘 Getting Help

### Common Issues

**Issue**: "Cannot install matplotlib"
- **Solution**: See [Getting Started - Installation](TRACK_BUILDER_GETTING_STARTED.md#installation)

**Issue**: "How do I load JSON tracks in simulator?"
- **Solution**: See [Simulator Guide - Limitations](TRACK_BUILDER_SIMULATOR_GUIDE.md)

**Issue**: "What parameters does add_curve accept?"
- **Solution**: See [API Reference - CurveSegment](TRACK_BUILDER_API_REFERENCE.md#curvesegment)

### Support Channels

- **Bug Reports**: [GitHub Issues](https://github.com/connected-autonomous-mobility/gym-donkeycar-v25.10.06/issues)
- **Questions**: [GitHub Discussions](https://github.com/connected-autonomous-mobility/gym-donkeycar-v25.10.06/discussions)
- **Pull Requests**: [GitHub PRs](https://github.com/connected-autonomous-mobility/gym-donkeycar-v25.10.06/pulls)

---

## 📝 Document Information

**Version**: 1.0  
**Last Updated**: October 31, 2025  
**Maintained By**: gym-donkeycar development team  

**Change Log**:
- 2025-10-31: Initial documentation index created
- Documentation structure consolidated and organized
- All documents renamed for clarity and consistency
