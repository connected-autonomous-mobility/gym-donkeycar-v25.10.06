"""
visualize_track_matplotlib.py - Professional track visualization using matplotlib

This script creates high-quality graphical visualizations of track configurations using matplotlib.
Shows:
- Left and right track boundaries
- Center line
- Shaded track surface
- Segment IDs and labels
- Professional 2D plot with measurements

Usage:
    python visualize_track_matplotlib.py <track_file.json>
    python visualize_track_matplotlib.py my_track.json --save output.png
    python visualize_track_matplotlib.py my_track.json --dpi 300

Requirements:
    pip install matplotlib

Examples:
    # Display interactive plot
    python visualize_track_matplotlib.py my_track.json

    # Save to file
    python visualize_track_matplotlib.py my_track.json --save my_track.png

    # High resolution output
    python visualize_track_matplotlib.py my_track.json --save my_track.png --dpi 300
"""

import argparse
import json
import math
import sys
from typing import Dict, List, Tuple

try:
    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Polygon
except ImportError:
    print("Error: matplotlib is required for this script.")
    print("Install it with: pip install matplotlib")
    sys.exit(1)


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


def calculate_track_boundaries(
    track: Dict, num_points_per_segment: int = 50
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
                step_length = length / num_points_per_segment
                x += step_length * math.cos(heading)
                y += step_length * math.sin(heading)
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
                step_length = length / num_points_per_segment
                x += step_length * math.cos(heading)
                y += step_length * math.sin(heading)
                centerline.append((x, y, seg_id))
                add_boundary_points(x, y, heading)

    return centerline, left_boundary, right_boundary


def plot_track(track: Dict, save_path: str = None, dpi: int = 150, show_grid: bool = True):
    """
    Create a matplotlib visualization of the track.

    Args:
        track: Track configuration dictionary
        save_path: Optional path to save the figure
        dpi: DPI for saved figure
        show_grid: Whether to show grid lines
    """
    # Calculate track boundaries
    centerline, left_boundary, right_boundary = calculate_track_boundaries(track)

    # Extract coordinates
    center_x = [p[0] for p in centerline]
    center_y = [p[1] for p in centerline]
    left_x = [p[0] for p in left_boundary]
    left_y = [p[1] for p in left_boundary]
    right_x = [p[0] for p in right_boundary]
    right_y = [p[1] for p in right_boundary]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_aspect("equal")

    # Create track surface polygon (between boundaries)
    # Combine left and reversed right boundary to create a closed polygon
    track_polygon_coords = list(zip(left_x, left_y)) + list(zip(right_x[::-1], right_y[::-1]))
    track_polygon = Polygon(track_polygon_coords, facecolor="lightgray", edgecolor="none", alpha=0.5, label="Track Surface")
    ax.add_patch(track_polygon)

    # Plot boundaries
    ax.plot(left_x, left_y, "k-", linewidth=2.5, label="Left Boundary", zorder=3)
    ax.plot(right_x, right_y, "k-", linewidth=2.5, label="Right Boundary", zorder=3)

    # Plot center line (dashed)
    ax.plot(center_x, center_y, "r--", linewidth=1.5, label="Center Line", alpha=0.7, zorder=2)

    # Mark start position
    ax.plot(center_x[0], center_y[0], "go", markersize=12, label="Start", zorder=5)

    # Add segment labels
    segments = track.get("segments", [])
    segment_positions = {}

    # Find representative position for each segment
    for x, y, seg_id in centerline:
        if seg_id > 0:
            if seg_id not in segment_positions:
                segment_positions[seg_id] = []
            segment_positions[seg_id].append((x, y))

    # Place labels at midpoint of each segment
    for seg_id, positions in segment_positions.items():
        if positions:
            mid_idx = len(positions) // 2
            mid_x, mid_y = positions[mid_idx]

            # Get segment info
            if seg_id <= len(segments):
                segment = segments[seg_id - 1]
                seg_type = segment.get("type", "unknown")

                # Create label
                label_text = f"[{seg_id}]\n{seg_type}"

                # Add text with background
                ax.text(
                    mid_x,
                    mid_y,
                    label_text,
                    fontsize=9,
                    ha="center",
                    va="center",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7, edgecolor="black"),
                    zorder=4,
                )

    # Set labels and title
    ax.set_xlabel("X Position (meters)", fontsize=12)
    ax.set_ylabel("Y Position (meters)", fontsize=12)
    track_name = track.get("name", "Unknown Track")
    ax.set_title(f"Track Visualization: {track_name}", fontsize=14, fontweight="bold")

    # Add grid
    if show_grid:
        ax.grid(True, alpha=0.3, linestyle=":", linewidth=0.5)

    # Add legend
    ax.legend(loc="best", fontsize=10)

    # Add track statistics as text box
    stats_text = (
        f"Track: {track.get('name', 'Unknown')}\n"
        f"Length: {track.get('total_length', 0):.2f} m\n"
        f"Width: {track.get('width', 0):.2f} m\n"
        f"Segments: {track.get('num_segments', 0)}"
    )

    ax.text(
        0.02,
        0.98,
        stats_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="gray"),
    )

    # Adjust layout
    plt.tight_layout()

    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches="tight")
        print(f"Track visualization saved to: {save_path}")
    else:
        plt.show()

    plt.close()


def print_track_info(track: Dict):
    """Print detailed track information to console."""
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

    # Print segments
    segments = track.get("segments", [])
    if segments:
        print("SEGMENT DETAILS:")
        print("-" * 80)
        for i, segment in enumerate(segments, 1):
            seg_type = segment.get("type", "unknown")
            length = segment.get("length", 0)
            print(f"\n[ID: {i}] {seg_type.upper()} (Length: {length:.2f}m)")

            if seg_type == "curve":
                print(f"        Radius: {segment.get('radius', 0):.2f}m")
                print(f"        Angle: {segment.get('angle', 0):.2f}°")
                print(f"        Direction: {segment.get('direction', 'unknown')}")
            elif seg_type == "elevation":
                print(f"        Height change: {segment.get('height_change', 0):.2f}m")
                if segment.get("gradient") is not None:
                    print(f"        Gradient: {segment.get('gradient')}°")

        print("\n" + "-" * 80 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Visualize track configurations using matplotlib",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Display interactive plot
  python visualize_track_matplotlib.py my_track.json
  
  # Save to file
  python visualize_track_matplotlib.py my_track.json --save my_track.png
  
  # High resolution output
  python visualize_track_matplotlib.py my_track.json --save my_track.png --dpi 300
  
  # Without grid
  python visualize_track_matplotlib.py my_track.json --no-grid
        """,
    )

    parser.add_argument("track_file", type=str, help="Path to the track JSON file")

    parser.add_argument("--save", type=str, help="Save plot to file instead of displaying", metavar="FILE")

    parser.add_argument("--dpi", type=int, default=150, help="DPI for saved figure (default: 150)")

    parser.add_argument("--no-grid", action="store_true", help="Disable grid lines")

    args = parser.parse_args()

    try:
        # Load track
        track = load_track(args.track_file)

        # Print track information
        print_track_info(track)

        # Create visualization
        print("Creating matplotlib visualization...")
        plot_track(track, save_path=args.save, dpi=args.dpi, show_grid=not args.no_grid)

        if not args.save:
            print("Displaying interactive plot...")

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
