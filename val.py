from ultralytics import YOLO


def main():
    model = YOLO(r'runs/obb/train/weights/best.pt')
    model.val(data='dota8-obb.yaml', imgsz=1024, batch=4, workers=4)


if __name__ == '__main__':
    main()
