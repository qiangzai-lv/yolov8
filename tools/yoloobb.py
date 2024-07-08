from pathlib import Path
from xml_utils import parse_xml
import cv2

from ultralytics.data.converter import convert_dota_to_yolo_obb
from ultralytics.utils import TQDM

# convert_dota_to_yolo_obb('./dataset')  # convert DOTA dataset to YOLO format

def convert_plane_to_yolo_obb(plane_root_path: str):
    dota_root_path = Path(plane_root_path)

    def convert_label(image_name, image_width, image_height, orig_label_dir, save_dir):

        orig_label_path = orig_label_dir / f"{image_name}.xml"
        save_path = save_dir / f"{image_name}.txt"
        # xml读取
        orig_label_xml = parse_xml(orig_label_path)

        with save_path.open("w") as g:
            for obj in orig_label_xml.objects:
                class_idx = obj.possible_result
                coords = [point for point in obj.points]
                normalized_coords = [
                    coords[i] / image_width if i % 2 == 0 else coords[i] / image_height for i in range(8)
                ]
                formatted_coords = ["{:.6g}".format(coord) for coord in normalized_coords]
                g.write(f"{class_idx} {' '.join(formatted_coords)}\n")

    for phase in ["train", "val"]:
        image_dir = dota_root_path / "images" / phase
        orig_label_dir = dota_root_path / "labels" / f"{phase}_original"
        save_dir = dota_root_path / "labels" / phase

        save_dir.mkdir(parents=True, exist_ok=True)

        image_paths = list(image_dir.iterdir())
        for image_path in TQDM(image_paths, desc=f"Processing {phase} images"):
            if image_path.suffix != ".tif":
                continue
            image_name_without_ext = image_path.stem
            img = cv2.imread(str(image_path))
            h, w = img.shape[:2]
            convert_label(image_name_without_ext, w, h, orig_label_dir, save_dir)

if __name__ == '__main__':
    convert_plane_to_yolo_obb('./dataset-plane')  # convert DOTA dataset to YOLO format
