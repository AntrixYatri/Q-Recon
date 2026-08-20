def get_box_geometry(box: list) -> dict:
    """
    Convert EasyOCR coordinate box polygon into geometry coordinates:
    x1, y1 (top-left), x2, y2 (bottom-right), xc, yc (center point), width, and height.
    """
    xs = [point[0] for point in box]
    ys = [point[1] for point in box]

    return {
        "x1": min(xs),
        "y1": min(ys),
        "x2": max(xs),
        "y2": max(ys),
        "xc": sum(xs) / len(xs),
        "yc": sum(ys) / len(ys),
        "width": max(xs) - min(xs),
        "height": max(ys) - min(ys)
    }
