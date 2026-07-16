#!/usr/bin/env python3
"""
Analyze a GPX route file: total distance/elevation, and sustained climb segments.

Standalone stdlib script (no pip installs needed) so route-vetting stays
consistent across sessions instead of ad-hoc one-off scripts each time.

Usage:
    python scripts/analyze_gpx.py <path/to/route.gpx> [options]

Options:
    --grade-threshold FLOAT   Grade %% above which a window counts as "climbing" (default 3.0)
    --window METERS           Forward-looking distance window for grade calc (default 300)
    --merge-gap KM            Merge climb segments separated by less than this gap (default 0.3)
    --min-climb-km KM         Drop merged segments shorter than this (default 0.4)
    --smooth-window N         Points per smoothing bucket for elevation gain/loss (default 5)
"""
import argparse
import bisect
import math
import xml.etree.ElementTree as ET


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def load_points(path):
    tree = ET.parse(path)
    root = tree.getroot()
    ns = root.tag.split("}")[0].strip("{")

    def extract(tag):
        pts = []
        for el in root.iter("{%s}%s" % (ns, tag)):
            lat = float(el.get("lat"))
            lon = float(el.get("lon"))
            ele_el = el.find("{%s}ele" % ns)
            ele = float(ele_el.text) if ele_el is not None else None
            pts.append((lat, lon, ele))
        return pts

    pts = extract("trkpt")
    if not pts:
        pts = extract("rtept")
    if not pts:
        raise ValueError("No <trkpt> or <rtept> points found in GPX file")
    return pts


def cumulative_distances(pts):
    dists = [0.0]
    for i in range(1, len(pts)):
        d = haversine(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1])
        dists.append(dists[-1] + d)
    return dists


def smoothed_elevations(elevations, smooth_window):
    """Bucket-average elevation to reduce GPS/barometric noise before summing gain/loss."""
    n = len(elevations)
    smoothed = []
    for i in range(n):
        lo = max(0, i - smooth_window // 2)
        hi = min(n, i + smooth_window // 2 + 1)
        window = [e for e in elevations[lo:hi] if e is not None]
        smoothed.append(sum(window) / len(window) if window else None)
    return smoothed


def gain_loss(elevations):
    gain = loss = 0.0
    for i in range(1, len(elevations)):
        a, b = elevations[i - 1], elevations[i]
        if a is None or b is None:
            continue
        de = b - a
        if de > 0:
            gain += de
        else:
            loss += -de
    return gain, loss


def climb_segments(dists, elevations, window, grade_threshold, merge_gap_km, min_climb_km):
    grades = []
    n = len(dists)
    for i in range(n):
        target = dists[i] + window
        j = bisect.bisect_left(dists, target, lo=i)
        if j >= n:
            break
        d_seg = dists[j] - dists[i]
        if d_seg < window * 0.3 or elevations[i] is None or elevations[j] is None:
            continue
        e_seg = elevations[j] - elevations[i]
        grades.append((dists[i] / 1000, e_seg / d_seg * 100, i, j))

    runs = []
    cur_start = cur_end = cur_i0 = None
    for dkm, g, i, j in grades:
        if g > grade_threshold:
            if cur_start is None:
                cur_start, cur_i0 = dkm, i
            cur_end = dkm
        else:
            if cur_start is not None:
                runs.append((cur_start, cur_end, cur_i0))
                cur_start = None
    if cur_start is not None:
        runs.append((cur_start, cur_end, cur_i0))

    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] < merge_gap_km:
            merged[-1] = (merged[-1][0], r[1], merged[-1][2])
        else:
            merged.append(list(r))

    segments = []
    for s_km, e_km, i0 in merged:
        if e_km - s_km < min_climb_km:
            continue
        i_start = bisect.bisect_left(dists, s_km * 1000)
        i_end = bisect.bisect_left(dists, e_km * 1000)
        i_end = min(i_end, n - 1)
        seg_gain = elevations[i_end] - elevations[i_start]
        length_km = e_km - s_km
        avg_grade = seg_gain / (length_km * 1000) * 100 if length_km > 0 else 0

        # steepest sub-window within this segment (same forward-window size)
        max_g = None
        for i in range(i_start, i_end):
            target = dists[i] + window
            j = bisect.bisect_left(dists, target, lo=i)
            if j >= n or j > i_end:
                continue
            d_seg = dists[j] - dists[i]
            if d_seg < window * 0.3 or elevations[i] is None or elevations[j] is None:
                continue
            g = (elevations[j] - elevations[i]) / d_seg * 100
            if max_g is None or g > max_g:
                max_g = g

        segments.append({
            "start_km": round(s_km, 2),
            "end_km": round(e_km, 2),
            "length_km": round(length_km, 2),
            "gain_m": round(seg_gain, 1),
            "avg_grade_pct": round(avg_grade, 1),
            "max_grade_pct": round(max_g, 1) if max_g is not None else None,
        })
    return segments


def analyze(path, grade_threshold=3.0, window=300, merge_gap_km=0.3, min_climb_km=0.4, smooth_window=5):
    pts = load_points(path)
    dists = cumulative_distances(pts)
    raw_elevations = [p[2] for p in pts]
    smoothed = smoothed_elevations(raw_elevations, smooth_window)

    total_distance_km = dists[-1] / 1000
    gain, loss = gain_loss(smoothed)
    valid_ele = [e for e in raw_elevations if e is not None]

    segments = climb_segments(dists, smoothed, window, grade_threshold, merge_gap_km, min_climb_km)

    return {
        "num_points": len(pts),
        "total_distance_km": round(total_distance_km, 2),
        "elevation_gain_m": round(gain, 1),
        "elevation_loss_m": round(loss, 1),
        "min_elevation_m": min(valid_ele) if valid_ele else None,
        "max_elevation_m": max(valid_ele) if valid_ele else None,
        "climb_segments": segments,
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze a GPX route's distance, elevation, and climb structure.")
    parser.add_argument("gpx_path")
    parser.add_argument("--grade-threshold", type=float, default=3.0)
    parser.add_argument("--window", type=float, default=300)
    parser.add_argument("--merge-gap", type=float, default=0.3)
    parser.add_argument("--min-climb-km", type=float, default=0.4)
    parser.add_argument("--smooth-window", type=int, default=5)
    args = parser.parse_args()

    result = analyze(
        args.gpx_path,
        grade_threshold=args.grade_threshold,
        window=args.window,
        merge_gap_km=args.merge_gap,
        min_climb_km=args.min_climb_km,
        smooth_window=args.smooth_window,
    )

    print(f"Points: {result['num_points']}")
    print(f"Total distance: {result['total_distance_km']} km")
    print(f"Elevation gain: {result['elevation_gain_m']} m (smoothed, window={args.smooth_window})")
    print(f"Elevation loss: {result['elevation_loss_m']} m")
    print(f"Elevation range: {result['min_elevation_m']}-{result['max_elevation_m']} m")
    print(f"\nSustained climb segments (>{args.grade_threshold}% avg over {args.window}m windows, "
          f"merge gap <{args.merge_gap}km, min length {args.min_climb_km}km):")
    if not result["climb_segments"]:
        print("  (none found — route is rolling/flat by these thresholds)")
    for seg in result["climb_segments"]:
        print(f"  {seg['start_km']}-{seg['end_km']} km (len {seg['length_km']} km): "
              f"+{seg['gain_m']} m, avg {seg['avg_grade_pct']}%, max {seg['max_grade_pct']}%")


if __name__ == "__main__":
    main()
