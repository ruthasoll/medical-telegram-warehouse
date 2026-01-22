import os
import pandas as pd
import logging
from ultralytics import YOLO
import glob

# Setup logging
logging.basicConfig(filename='logs/yolo_detect.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_objects(images_dir, output_csv):
    # Load model
    try:
        model = YOLO("yolov8n.pt")  # Load pretrained model
    except Exception as e:
        logging.error(f"Failed to load YOLO model: {e}")
        return

    detection_results = []
    
    # Find all images
    image_paths = glob.glob(os.path.join(images_dir, "**", "*.jpg"), recursive=True)
    logging.info(f"Found {len(image_paths)} images to process.")

    for img_path in image_paths:
        try:
            # Run inference
            results = model(img_path)
            
            # Extract info
            # We assume one result per image
            result = results[0]
            
            # Get path components (channel, message_id)
            # Path structure: data/raw/images/{channel_name}/{message_id}.jpg
            parts = os.path.normpath(img_path).split(os.sep)
            if len(parts) >= 2:
                message_id = os.path.splitext(parts[-1])[0]
                channel_name = parts[-2]
            else:
                logging.warning(f"Could not parse path correctly: {img_path}")
                continue

            detected_objects = []
            has_person = False
            has_product = False
            
            # Common product classes in COCO (bottle, cup, bowl, etc.)
            product_classes = [39, 40, 41, 39] # 39: bottle, 40: wine glass, 41: cup. 
            # Let's rely on class names for better readability
            
            for box in result.boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                conf = float(box.conf[0])
                
                detected_objects.append(f"{cls_name}:{conf:.2f}")
                
                if cls_name == 'person':
                    has_person = True
                if cls_name in ['bottle', 'cup', 'bowl', 'vase', 'suitcase', 'handbag', 'backpack']: # Broad definition of product container
                    has_product = True
            
            # Classification
            if has_person and has_product:
                category = 'promotional'
            elif has_product and not has_person:
                category = 'product_display'
            elif has_person and not has_product:
                category = 'lifestyle'
            else:
                category = 'other'

            detection_results.append({
                'message_id': message_id,
                'channel_name': channel_name,
                'image_path': img_path,
                'detected_objects': "; ".join(detected_objects),
                'image_category': category
            })
            
        except Exception as e:
            logging.error(f"Error processing {img_path}: {e}")

    # Save to CSV
    if detection_results:
        df = pd.DataFrame(detection_results)
        df.to_csv(output_csv, index=False)
        logging.info(f"Saved detection results to {output_csv}")
    else:
        logging.info("No detections to save.")

if __name__ == "__main__":
    detect_objects("data/raw/images", "data/raw/yolo_detections.csv")
