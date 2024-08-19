from ultralytics import YOLO

class YOLOService:

    classNames = []
    model = None

    def LoadModel(self, weights):
        
        self.model = YOLO(weights)

    def Configure(self, weights_file, classNames):
        self.LoadModel(weights_file)
        self.classNames = classNames

    def RecognizeObjects(self, rgb) -> list:

        # Detect objects with YOLO
        yolo_results = self.model.predict(rgb)
        boxes = yolo_results[0].boxes.data  # Bounding box information

        # Map detected class IDs to class names
        detected_objects = []
        for box in boxes:
            class_id = int(box[5])
            class_name = self.classNames[class_id]
            detected_objects.append(class_name)
        
        print(f"Detected objects: {detected_objects}")

        return detected_objects, boxes