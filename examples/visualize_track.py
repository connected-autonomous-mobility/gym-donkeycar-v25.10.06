"""
visualize_track.py - Visualize track configurations from JSON files

This script reads a track configuration JSON file and displays:
- 2D top-down visualization of the track
- Track statistics and segment information
- ASCII art representation for terminal viewing

Usage:
    python visualize_track.py <track_file.json>
    python visualize_track.py my_custom_track.json

Examples:
    # Create and visualize a simple oval
    python -c "from gym_donkeycar.core import create_simple_oval; import json; \
    track = create_simple_oval(); \
    json.dump(track, open('oval.json', 'w'), indent=2)"
    
    python visualize_track.py oval.json
"""

import argparse
import json
import math
import sys
from typing import Dict, List, Tuple


def load_track(filepath: str) -> Dict:
    """Load track configuration from JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filepath}': {e}")
        sys.exit(1)


def print_track_info(track: Dict) -> None:
    """Print detailed track information."""
    print("\n" + "=" * 70)
    print(f"TRACK: {track.get('name', 'Unknown')}")
    print("=" * 70)
    print(f"Track Width:      {track.get('width', 0):.2f} meters")
    print(f"Total Length:     {track.get('total_length', 0):.2f} meters")
    print(f"Number of Segments: {track.get('num_segments', 0)}")

    start_pos = track.get("start_position", {})
    print(f"Start Position:   x={start_pos.get('x', 0):.2f}, " f"y={start_pos.get('y', 0):.2f}, z={start_pos.get('z', 0):.2f}")
    print("=" * 70 + "\n")


def print_segments(track: Dict) -> None:
    """Print detailed information about each segment."""
    segments = track.get("segments", [])

    if not segments:
        print("No segments found in track.\n")
        return

    print("SEGMENTS:")
    print("-" * 70)

    for i, segment in enumerate(segments, 1):
        seg_type = segment.get("type", "unknown")
        length = segment.get("length", 0)

        print(f"\n{i}. {seg_type.upper()} (Length: {length:.2f}m)")

        if seg_type == "straight":
            print(f"   → Straight section")

        elif seg_type == "curve":
            radius = segment.get("radius", 0)
            angle = segment.get("angle", 0)
            direction = segment.get("direction", "unknown")
            print(f"   → Radius: {radius:.2f}m")
            print(f"   → Angle: {angle:.2f}°")
            print(f"   → Direction: {direction}")
            print(f"   → Arc length: {length:.2f}m")

        elif seg_type == "elevation":
            height_change = segment.get("height_change", 0)
            gradient = segment.get("gradient", "N/A")
            direction_text = "Uphill" if height_change > 0 else "Downhill"
            print(f"   → {direction_text}: {abs(height_change):.2f}m")
            if gradient is not None:
                print(f"   → Gradient: {gradient}°")

    print("\n" + "-" * 70 + "\n")


def calculate_track_path(track: Dict) -> List[Tuple[float, float, float]]:
    """
    Calculate the 2D path of the track for visualization.
    Returns list of (x, y, heading) tuples representing points along the track.
    """
    segments = track.get("segments", [])
    start_pos = track.get("start_position", {})

    # Starting position and heading
    x = start_pos.get("x", 0)
    y = start_pos.get("z", 0)  # Use z as y for top-down view
    heading = 0  # Radians, 0 = east, pi/2 = north

    path = [(x, y, heading)]

    for segment in segments:
        seg_type = segment.get("type")
        length = segment.get("length", 0)

        if seg_type == "straight":
            # Move straight in current heading direction
            x += length * math.cos(heading)
            y += length * math.sin(heading)
            path.append((x, y, heading))

        elif seg_type == "curve":
            radius = segment.get("radius", 0)
            angle = segment.get("angle", 0)
            direction = segment.get("direction", "left")

            # Convert angle to radians
            angle_rad = math.radians(angle)

            # Determine curve direction
            turn_direction = 1 if direction == "left" else -1

            # Calculate curve with multiple points for smoother visualization
            num_points = max(5, int(abs(angle) / 10))
            angle_step = angle_rad / num_points

            for i in range(num_points):
                # Update heading
                heading += turn_direction * angle_step

                # Calculate position (moving along the arc)
                step_length = length / num_points
                x += step_length * math.cos(heading)
                y += step_length * math.sin(heading)
                path.append((x, y, heading))

        elif seg_type == "elevation":
            # Elevation changes don't affect 2D path
            x += length * math.cos(heading)
            y += length * math.sin(heading)
            path.append((x, y, heading))

    return path


def create_ascii_visualization(path: List[Tuple[float, float, float]], width: int = 60, height: int = 30) -> str:
    """Create an ASCII art visualization of the track."""
    if not path:
        return "No path data to visualize"

    # Find bounds
    xs = [p[0] for p in path]
    ys = [p[1] for p in path]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Add padding
    padding = 0.1
    x_range = max_x - min_x
    y_range = max_y - min_y

    if x_range == 0:
        x_range = 1
    if y_range == 0:
        y_range = 1

    min_x -= x_range * padding
    max_x += x_range * padding
    min_y -= y_range * padding
    max_y += y_range * padding

    x_range = max_x - min_x
    y_range = max_y - min_y

    # Create grid
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Plot path
    for i, (x, y, _) in enumerate(path):
        # Convert to grid coordinates
        grid_x = int((x - min_x) / x_range * (width - 1))
        grid_y = int((y - min_y) / y_range * (height - 1))

        # Clamp to grid bounds
        grid_x = max(0, min(width - 1, grid_x))
        grid_y = max(0, min(height - 1, grid_y))

        # Invert y for display (top = high y value)
        grid_y = height - 1 - grid_y

        # Mark start position
        if i == 0:
            grid[grid_y][grid_x] = "S"
        # Mark path
        elif grid[grid_y][grid_x] == " ":
            grid[grid_y][grid_x] = "█"

    # Convert grid to string
    result = []
    result.append("┌" + "─" * width + "┐")
    for row in grid:
        result.append("│" + "".join(row) + "│")
    result.append("└" + "─" * width + "┘")

    return "\n".join(result)


def visualize_track(filepath: str) -> None:
    """Main visualization function."""
    # Load track
    track = load_track(filepath)

    # Print track information
    print_track_info(track)

    # Print segment details
    print_segments(track)

    # Calculate and display track path
    print("TRACK VISUALIZATION (Top-Down View):")
    print("-" * 70)
    path = calculate_track_path(track)
    ascii_art = create_ascii_visualization(path)
    print(ascii_art)
    print("\nLegend: S = Start, █ = Track path")
    print("-" * 70 + "\n")

    # Statistics summary
    print("SUMMARY:")
    print("-" * 70)
    print(f"File:             {filepath}")
    print(f"Track Name:       {track.get('name', 'Unknown')}")
    print(f"Total Length:     {track.get('total_length', 0):.2f} meters")
    print(f"Track Width:      {track.get('width', 0):.2f} meters")
    print(f"Segments:         {track.get('num_segments', 0)}")

    # Count segment types
    segments = track.get("segments", [])
    segment_counts = {}
    for seg in segments:
        seg_type = seg.get("type", "unknown")
        segment_counts[seg_type] = segment_counts.get(seg_type, 0) + 1

    if segment_counts:
        print("\nSegment Breakdown:")
        for seg_type, count in sorted(segment_counts.items()):
            print(f"  - {seg_type}: {count}")

    print("-" * 70 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Visualize track configurations from JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python visualize_track.py my_track.json
  python visualize_track.py examples/oval_track.json
  
Create a track and visualize it:
  python -c "from gym_donkeycar.core import create_simple_oval; import json; \\
             track = create_simple_oval(); \\
             json.dump(track, open('oval.json', 'w'), indent=2)"
  python visualize_track.py oval.json
        """,
    )

    parser.add_argument("track_file", type=str, help="Path to the track JSON file")

    args = parser.parse_args()

    try:
        visualize_track(args.track_file)
    except KeyboardInterrupt:
        print("\n\nVisualization interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError during visualization: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
