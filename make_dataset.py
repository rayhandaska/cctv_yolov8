from ultralytics import YOLO

model = YOLO('yolov8s.pt')

results = model.train(
    data='data.yaml',
    imgsz=800,
    epochs=100,
    name='running_dataset'
)
