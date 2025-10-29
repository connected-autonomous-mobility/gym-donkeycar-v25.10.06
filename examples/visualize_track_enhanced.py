"""
visualize_track_enhanced.py - Enhanced track visualization with boundaries and styling

This script creates a detailed visualization of track configurations showing:
- Left and right track boundaries
- Center line
- Track elements with segment IDs
- Shaded track surface
- Clear boundary markers

Usage:
    python visualize_track_enhanced.py <track_file.json>
    python visualize_track_enhanced.py my_custom_track.json [--width WIDTH] [--height HEIGHT]

Examples:
    python visualize_track_enhanced.py oval.json
    python visualize_track_enhanced.py circuit.json --width 80 --height 40
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
    print("\n" + "=" * 80)
    print(f"TRACK: {track.get('name', 'Unknown')}")
    print("=" * 80)
    print(f"Track Width:        {track.get('width', 0):.2f} meters")
    print(f"Total Length:       {track.get('total_length', 0):.2f} meters")
    print(f"Number of Segments: {track.get('num_segments', 0)}")

    start_pos = track.get("start_position", {})
    print(
        f"Start Position:     x={start_pos.get('x', 0):.2f}, " f"y={start_pos.get('y', 0):.2f}, z={start_pos.get('z', 0):.2f}"
    )
    print("=" * 80 + "\n")


def print_segments(track: Dict) -> None:
    """Print detailed information about each segment with IDs."""
    segments = track.get("segments", [])

    if not segments:
        print("No segments found in track.\n")
        return

    print("SEGMENT DETAILS:")
    print("-" * 80)

    for i, segment in enumerate(segments, 1):
        seg_type = segment.get("type", "unknown")
        length = segment.get("length", 0)

        print(f"\n[ID: {i}] {seg_type.upper()} (Length: {length:.2f}m)")

        if seg_type == "straight":
            print(f"        Type: Straight section")

        elif seg_type == "curve":
            radius = segment.get("radius", 0)
            angle = segment.get("angle", 0)
            direction = segment.get("direction", "unknown")
            print(f"        Radius: {radius:.2f}m")
            print(f"        Angle: {angle:.2f}°")
            print(f"        Direction: {direction}")
            print(f"        Arc length: {length:.2f}m")

        elif seg_type == "elevation":
            height_change = segment.get("height_change", 0)
            gradient = segment.get("gradient", "N/A")
            direction_text = "Uphill" if height_change > 0 else "Downhill"
            print(f"        {direction_text}: {abs(height_change):.2f}m")
            if gradient is not None:
                print(f"        Gradient: {gradient}°")

    print("\n" + "-" * 80 + "\n")


def calculate_track_boundaries(
    track: Dict, num_points_per_segment: int = 20
) -> Tuple[List[Tuple[float, float, int]], List[Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Calculate the center line, left boundary, and right boundary of the track.

    Returns:
        (centerline, left_boundary, right_boundary)
        centerline: List of (x, y, segment_id) tuples
        left_boundary: List of (x, y) tuples
        right_boundary: List of (x, y) tuples
    """
    segments = track.get("segments", [])
    start_pos = track.get("start_position", {})
    track_width = track.get("width", 4.0)

    # Starting position and heading
    x = start_pos.get("x", 0)
    y = start_pos.get("z", 0)  # Use z as y for top-down view
    heading = 0  # Radians, 0 = east, pi/2 = north

    centerline = [(x, y, 0)]
    left_boundary = []
    right_boundary = []

    # Half width for boundaries
    half_width = track_width / 2.0

    def add_boundary_points(cx, cy, h):
        """Add left and right boundary points perpendicular to heading."""
        # Left boundary (perpendicular left to heading)
        lx = cx + half_width * math.cos(h + math.pi / 2)
        ly = cy + half_width * math.sin(h + math.pi / 2)
        left_boundary.append((lx, ly))

        # Right boundary (perpendicular right to heading)
        rx = cx + half_width * math.cos(h - math.pi / 2)
        ry = cy + half_width * math.sin(h - math.pi / 2)
        right_boundary.append((rx, ry))

    # Add initial boundaries
    add_boundary_points(x, y, heading)

    for seg_id, segment in enumerate(segments, 1):
        seg_type = segment.get("type")
        length = segment.get("length", 0)

        if seg_type == "straight":
            # Move straight in current heading direction
            for i in range(1, num_points_per_segment + 1):
                t = i / num_points_per_segment
                step_length = length * t
                x_start = centerline[-1][0]
                y_start = centerline[-1][1]
                x = x_start + (length / num_points_per_segment) * math.cos(heading)
                y = y_start + (length / num_points_per_segment) * math.sin(heading)
                centerline.append((x, y, seg_id))
                add_boundary_points(x, y, heading)

        elif seg_type == "curve":
            radius = segment.get("radius", 0)
            angle = segment.get("angle", 0)
            direction = segment.get("direction", "left")

            # Convert angle to radians
            angle_rad = math.radians(angle)

            # Determine curve direction
            turn_direction = 1 if direction == "left" else -1

            # Calculate curve with multiple points
            angle_step = angle_rad / num_points_per_segment

            for i in range(1, num_points_per_segment + 1):
                # Update heading
                heading += turn_direction * angle_step

                # Calculate position (moving along the arc)
                step_length = length / num_points_per_segment
                x += step_length * math.cos(heading)
                y += step_length * math.sin(heading)
                centerline.append((x, y, seg_id))
                add_boundary_points(x, y, heading)

        elif seg_type == "elevation":
            # Elevation changes don't affect 2D path
            for i in range(1, num_points_per_segment + 1):
                x += (length / num_points_per_segment) * math.cos(heading)
                y += (length / num_points_per_segment) * math.sin(heading)
                centerline.append((x, y, seg_id))
                add_boundary_points(x, y, heading)

    return centerline, left_boundary, right_boundary


def create_enhanced_visualization(
    centerline: List[Tuple[float, float, int]],
    left_boundary: List[Tuple[float, float]],
    right_boundary: List[Tuple[float, float]],
    width: int = 80,
    height: int = 40,
) -> str:
    """Create an enhanced ASCII art visualization showing boundaries and center line."""
    if not centerline:
        return "No path data to visualize"

    # Collect all points for bounds
    all_points = [(p[0], p[1]) for p in centerline] + left_boundary + right_boundary

    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Add padding
    padding = 0.15
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

    # Create grid with segment IDs
    grid = [[" " for _ in range(width)] for _ in range(height)]
    segment_grid = [[0 for _ in range(width)] for _ in range(height)]

    def to_grid_coords(x, y):
        """Convert world coordinates to grid coordinates."""
        grid_x = int((x - min_x) / x_range * (width - 1))
        grid_y = int((y - min_y) / y_range * (height - 1))
        grid_x = max(0, min(width - 1, grid_x))
        grid_y = max(0, min(height - 1, grid_y))
        grid_y = height - 1 - grid_y  # Invert y for display
        return grid_x, grid_y

    # First, mark all boundary and centerline points
    left_grid_points = set()
    right_grid_points = set()
    center_grid_points = {}

    for lx, ly in left_boundary:
        gx, gy = to_grid_coords(lx, ly)
        left_grid_points.add((gx, gy))

    for rx, ry in right_boundary:
        gx, gy = to_grid_coords(rx, ry)
        right_grid_points.add((gx, gy))

    for cx, cy, seg_id in centerline:
        gx, gy = to_grid_coords(cx, cy)
        center_grid_points[(gx, gy)] = seg_id

    # Fill track surface using flood-fill approach from centerline
    # Mark areas between boundaries as track surface
    for row_idx in range(height):
        in_track = False
        last_boundary_x = -1

        for col_idx in range(width):
            is_left = (col_idx, row_idx) in left_grid_points
            is_right = (col_idx, row_idx) in right_grid_points
            is_boundary = is_left or is_right

            if is_boundary:
                if not in_track:
                    in_track = True
                    last_boundary_x = col_idx
                elif in_track and col_idx > last_boundary_x + 1:
                    # Found second boundary, we were in track
                    in_track = False
            elif in_track:
                # We're between boundaries, fill with track surface
                grid[row_idx][col_idx] = "░"

    # Draw left boundary (outer edge)
    for i, (x, y) in enumerate(left_boundary):
        grid_x, grid_y = to_grid_coords(x, y)
        if i == 0:
            grid[grid_y][grid_x] = "S"  # Start marker
        else:
            grid[grid_y][grid_x] = "╫"  # Left boundary with strong marker

    # Draw right boundary (outer edge)
    for x, y in right_boundary:
        grid_x, grid_y = to_grid_coords(x, y)
        if grid[grid_y][grid_x] not in ["S", "╫"]:
            grid[grid_y][grid_x] = "╫"  # Right boundary with strong marker

    # Draw center line (dashed)
    for i, (x, y, seg_id) in enumerate(centerline):
        grid_x, grid_y = to_grid_coords(x, y)
        segment_grid[grid_y][grid_x] = seg_id

        if i == 0:
            grid[grid_y][grid_x] = "S"  # Start
        elif i % 4 == 0:  # Draw dashed center line
            if grid[grid_y][grid_x] == "░":
                grid[grid_y][grid_x] = "┼"  # Center line marker

    # Add segment ID labels
    segment_label_positions = {}
    for i, (x, y, seg_id) in enumerate(centerline):
        if seg_id > 0:
            # Pick positions spread throughout each segment
            if seg_id not in segment_label_positions:
                segment_label_positions[seg_id] = []
            if i % 25 == 12:  # Strategic spacing
                grid_x, grid_y = to_grid_coords(x, y)
                segment_label_positions[seg_id].append((grid_x, grid_y))

    # Place segment ID labels
    for seg_id, positions in segment_label_positions.items():
        if seg_id <= 9 and positions:  # Only single digit IDs
            # Use middle position for the label
            mid_pos = positions[len(positions) // 2]
            gx, gy = mid_pos
            if grid[gy][gx] in ["░", "┼", " "]:
                grid[gy][gx] = str(seg_id)

    # Convert grid to string
    result = []
    result.append("┌" + "─" * width + "┐")
    for row in grid:
        result.append("│" + "".join(row) + "│")
    result.append("└" + "─" * width + "┘")

    return "\n".join(result)


def visualize_track(filepath: str, viz_width: int = 80, viz_height: int = 40) -> None:
    """Main visualization function with enhanced display."""
    # Load track
    track = load_track(filepath)

    # Print track information
    print_track_info(track)

    # Print segment details with IDs
    print_segments(track)

    # Calculate track boundaries
    print("Calculating track boundaries...")
    centerline, left_boundary, right_boundary = calculate_track_boundaries(track)

    # Display enhanced visualization
    print("\nENHANCED TRACK VISUALIZATION (Top-Down View):")
    print("-" * 80)
    ascii_art = create_enhanced_visualization(centerline, left_boundary, right_boundary, viz_width, viz_height)
    print(ascii_art)

    print("\nLegend:")
    print("  S   = Start position")
    print("  ╫   = Track boundaries (left and right edges)")
    print("  ░   = Track surface (shaded area)")
    print("  ┼   = Center line (dashed)")
    print("  1-9 = Segment ID markers")
    print("-" * 80 + "\n")

    # Statistics summary
    print("SUMMARY:")
    print("-" * 80)
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

    print("-" * 80 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Enhanced track visualization with boundaries and segment IDs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python visualize_track_enhanced.py my_track.json
  python visualize_track_enhanced.py examples/oval_track.json --width 100 --height 50
  
Create a track and visualize it:
  python -c "from gym_donkeycar.core import create_simple_oval; import json; \\
             track = create_simple_oval(); \\
             json.dump(track, open('oval.json', 'w'), indent=2)"
  python visualize_track_enhanced.py oval.json
        """,
    )

    parser.add_argument("track_file", type=str, help="Path to the track JSON file")

    parser.add_argument("--width", type=int, default=80, help="Visualization width in characters (default: 80)")

    parser.add_argument("--height", type=int, default=40, help="Visualization height in characters (default: 40)")

    args = parser.parse_args()

    try:
        visualize_track(args.track_file, args.width, args.height)
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
