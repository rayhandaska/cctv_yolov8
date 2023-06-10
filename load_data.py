from ultralytics import YOLO

model = YOLO('yolov8s.pt')

results = model.train(
    data = 'data.yaml',
    imgsz = 800,
    epochs = 82,
    name = 'mstp_dataset'

)
#82 epochs completed in 7.566 hours.