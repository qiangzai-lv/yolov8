from ultralytics import YOLO


def main():
    model = YOLO('config/yolov8s-obb.yaml').load('weights/yolov8l-obb.pt')  # build from YAML and transfer weights
    model.train(data='config/dota8-obb.yaml', epochs=100, imgsz=1024, batch=4, workers=4)


if __name__ == '__main__':
    main()