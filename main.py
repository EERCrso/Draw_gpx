import os
import glob
import gpxpy
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from math import radians, cos, sin, sqrt, atan2

def load_gpx_files(folder):
    gpx_files = glob.glob(os.path.join(folder, '*.gpx'))
    tracks = []

    for file in gpx_files:
        with open(file, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                for segment in track.segments:
                    points = [(point.longitude, point.latitude) for point in segment.points]
                    tracks.append(points)

    return tracks


def haversine(coord1, coord2):
    # Haversine formula to calculate distance between two lat/lon coordinates
    R = 6371.0  # Earth radius in kilometers

    lon1, lat1 = coord1
    lon2, lat2 = coord2

    dlon = radians(lon2 - lon1)
    dlat = radians(lat2 - lat1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def calculate_total_distance(tracks):
    total_distance = 0.0

    for track in tracks:
        for i in range(1, len(track)):
            total_distance += haversine(track[i - 1], track[i])

    return total_distance


def draw_map(tracks, resolution=(1024, 1024), line_width=2):
    fig, ax = plt.subplots(figsize=(resolution[0] / 100, resolution[1] / 100), dpi=100)

    all_points = [point for track in tracks for point in track]
    x_coords, y_coords = zip(*all_points)

    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    # Normalize the coordinates for all tracks
    normalized_tracks = []
    for track in tracks:
        normalized_track = [(x, y) for x, y in track]
        normalized_tracks.append(normalized_track)

    # Create line segments for each track
    line_segments = LineCollection(normalized_tracks, linewidths=line_width, colors='black')

    ax.add_collection(line_segments)
    ax.axis('off')  # Turn off the axis

    plt.show()


if __name__ == "__main__":
    folder_path = "files"  # Update this to the path of your GPX folder
    tracks = load_gpx_files(folder_path)

    total_distance = calculate_total_distance(tracks)
    print(f"Total distance: {total_distance:.2f} km")

    draw_map(tracks, resolution=(3500, 3500), line_width=2)
