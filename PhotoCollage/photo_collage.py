from pathlib import Path
from PIL import Image, ImageOps
import math

# =========================
# Settings - adjust as needed
# =========================
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

CANVAS_SIZE = 2048
OUTER_MARGIN = 80
GAP = 32
BACKGROUND_COLOR = (255, 255, 255)
JPEG_QUALITY = 95

SUPPORTED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"
}


def load_photo(path: Path) -> Image.Image:
    """Load an image, apply EXIF orientation, and convert it to RGB."""
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source)
        # Composite transparent images onto a white background.
        if image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        ):
            rgba = image.convert("RGBA")
            white = Image.new("RGBA", rgba.size, BACKGROUND_COLOR + (255,))
            image = Image.alpha_composite(white, rgba).convert("RGB")
        else:
            image = image.convert("RGB")
        return image.copy()


def fit_size(image: Image.Image, max_width: int, max_height: int):
    """Return dimensions that fit inside a box without cropping."""
    width, height = image.size
    scale = min(max_width / width, max_height / height)
    return max(1, round(width * scale)), max(1, round(height * scale))


def resize_pair_to_similar_area(img1: Image.Image, img2: Image.Image,
                                box_width: int, box_height: int):
    """
    Resize both photos without cropping.
    Each photo gets the same displayed pixel area, while staying inside
    its own half of the canvas. This helps avoid one photo looking much
    larger than the other when their aspect ratios differ.
    """
    max1 = fit_size(img1, box_width, box_height)
    max2 = fit_size(img2, box_width, box_height)

    area1 = max1[0] * max1[1]
    area2 = max2[0] * max2[1]
    target_area = min(area1, area2)

    def dimensions_for_area(image):
        width, height = image.size
        scale = math.sqrt(target_area / (width * height))
        return max(1, round(width * scale)), max(1, round(height * scale))

    return dimensions_for_area(img1), dimensions_for_area(img2)


def paste_center(canvas: Image.Image, photo: Image.Image,
                 area_left: int, area_top: int,
                 area_width: int, area_height: int):
    """Resize and center a photo inside the specified area."""
    new_size = fit_size(photo, area_width, area_height)
    resized = photo.resize(new_size, Image.Resampling.LANCZOS)
    x = area_left + (area_width - new_size[0]) // 2
    y = area_top + (area_height - new_size[1]) // 2
    canvas.paste(resized, (x, y))


def create_pair_collage(path1: Path, path2: Path, output_path: Path):
    img1 = load_photo(path1)
    img2 = load_photo(path2)

    usable = CANVAS_SIZE - OUTER_MARGIN * 2
    cell_width = (usable - GAP) // 2
    cell_height = usable

    # Calculate equal-area dimensions while preserving each photo's ratio.
    size1, size2 = resize_pair_to_similar_area(
        img1, img2, cell_width, cell_height
    )

    canvas = Image.new(
        "RGB", (CANVAS_SIZE, CANVAS_SIZE), BACKGROUND_COLOR
    )

    x1_area = OUTER_MARGIN
    x2_area = OUTER_MARGIN + cell_width + GAP
    y_area = OUTER_MARGIN

    resized1 = img1.resize(size1, Image.Resampling.LANCZOS)
    resized2 = img2.resize(size2, Image.Resampling.LANCZOS)

    x1 = x1_area + (cell_width - resized1.width) // 2
    y1 = y_area + (cell_height - resized1.height) // 2
    x2 = x2_area + (cell_width - resized2.width) // 2
    y2 = y_area + (cell_height - resized2.height) // 2

    canvas.paste(resized1, (x1, y1))
    canvas.paste(resized2, (x2, y2))

    canvas.save(output_path, "JPEG", quality=JPEG_QUALITY, optimize=True)


def create_single_collage(path: Path, output_path: Path):
    """Place an unpaired final photo in the center of the full canvas."""
    photo = load_photo(path)
    canvas = Image.new(
        "RGB", (CANVAS_SIZE, CANVAS_SIZE), BACKGROUND_COLOR
    )
    usable = CANVAS_SIZE - OUTER_MARGIN * 2
    paste_center(canvas, photo, OUTER_MARGIN, OUTER_MARGIN, usable, usable)
    canvas.save(output_path, "JPEG", quality=JPEG_QUALITY, optimize=True)


def main():
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    photos = [
        path for path in INPUT_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    # Sort by file modification time: oldest first.
    # Filename is used as a stable tie-breaker when times are identical.
    photos.sort(key=lambda path: (path.stat().st_mtime, path.name.lower()))

    if not photos:
        print(f"No photos found in: {INPUT_DIR.resolve()}")
        print("Put your photos in the input folder and run this program again.")
        return

    print(f"Found {len(photos)} photo(s).")
    print("Order: file modification time, oldest to newest.")
    print()

    output_number = 1
    index = 0

    while index + 1 < len(photos):
        photo1 = photos[index]
        photo2 = photos[index + 1]
        output_path = OUTPUT_DIR / f"collage_{output_number:03d}.jpg"

        try:
            create_pair_collage(photo1, photo2, output_path)
            print(f"[OK] {photo1.name} + {photo2.name} -> {output_path.name}")
        except Exception as error:
            print(f"[ERROR] {photo1.name} + {photo2.name}: {error}")

        output_number += 1
        index += 2

    # If the number of photos is odd, output the last one by itself.
    if index < len(photos):
        last_photo = photos[index]
        output_path = OUTPUT_DIR / f"collage_{output_number:03d}.jpg"
        try:
            create_single_collage(last_photo, output_path)
            print(f"[OK] {last_photo.name} -> {output_path.name} (single photo)")
        except Exception as error:
            print(f"[ERROR] {last_photo.name}: {error}")

    print()
    print(f"Finished. Output folder: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
