# from ultralytics import YOLO
# from PIL import Image
# import numpy as np
# import torch
# from torchvision import transforms, datasets
# import cv2
# import tempfile
# import timm
# from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
# # =========================================
# # DEVICE
# # =========================================
# device = torch.device(
#     "cuda" if torch.cuda.is_available() else "cpu"
# )

# # =========================================
# # YOLO MODEL
# # =========================================
# yolo_model = YOLO("models/best.pt")

# # =========================================
# # BREED CLASSES
# # =========================================

# breed_classes = ['Buffalo_Chhattisgarhi', 'Buffalo_Jaffarabadi', 'Buffalo_banni', 'Buffalo_bargur', 'Buffalo_bhadwari', 'Buffalo_chilika', 'Buffalo_gojri', 'Buffalo_kalahandi', 'Buffalo_luit', 'Buffalo_marathwada', 'Buffalo_mehsana', 'Buffalo_murrah', 'Buffalo_nagpuri', 'Buffalo_nili-ravi', 'Buffalo_pandharpuri', 'Buffalo_surti', 'Buffalo_toda', 'Cow_Amritmahal', 'Cow_Ayrshire', 'Cow_Bargur', 'Cow_Dangi', 'Cow_Deoni', 'Cow_Gir', 'Cow_Hallikar', 'Cow_Hariana', 'Cow_Himachali Pahari', 'Cow_Kangayam', 'Cow_Kankrej', 'Cow_Kenkatha', 'Cow_Khariar', 'Cow_Khillari', 'Cow_Konkan Kapila', 'Cow_Kosali', 'Cow_Krishna_Valley', 'Cow_Ladakhi', 'Cow_Lakhimi', 'Cow_Malnad_gidda', 'Cow_Mewati', 'Cow_Nari', 'Cow_Nimari', 'Cow_Ongole', 'Cow_Poda Thirupu', 'Cow_Pulikulam', 'Cow_Punganur', 'Cow_Purnea', 'Cow_Rathi', 'Cow_Red kandhari', 'Cow_Red_Sindhi', 'Cow_Sahiwal', 'Cow_Shweta Kapila', 'Cow_Tharparkar', 'Cow_Umblachery', 'Cow_Vechur', 'Cow_bachaur', 'Cow_badri', 'Cow_bhelai', 'Cow_dagri', 'Cow_gangatari', 'Cow_gaolao', 'Cow_ghumsari', 'Cow_kherigarh', 'Cow_malvi', 'Cow_motu', 'Cow_nagori', 'Cow_ponwar', 'Cow_siri', 'Cow_thutho', 'resnet_croped_train_dataset']

# num_classes = 67 

# # =========================================
# # RESNET MODEL
# # =========================================
# resnet_model = timm.create_model(
#     "resnetv2_50",
#     pretrained=False,
#     num_classes=num_classes
# )

# resnet_model.load_state_dict(
#     torch.load(
#         "models/resnetv2_breed_classifier.pth",
#         map_location=device
#     )
# )

# resnet_model.to(device)

# resnet_model.eval()

# # =========================================
# # TRANSFORM
# # =========================================
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
# ])

# # =========================================
# # BREED CLASSIFICATION
# # =========================================
# def classify_breed(crop_img):

#     crop_pil = Image.fromarray(crop_img)

#     input_tensor = transform(crop_pil)

#     input_tensor = input_tensor.unsqueeze(0).to(device)

#     with torch.no_grad():

#         outputs = resnet_model(input_tensor)

#         probabilities = torch.softmax(outputs, dim=1)

#         confidence, predicted = torch.max(
#             probabilities,
#             1
#         )

#     breed_name = breed_classes[predicted.item()]

#     return breed_name, float(confidence.item())

# # =========================================
# # IMAGE PREDICTION
# # =========================================
# def detect_and_classify_image(image):

#     image_np = np.array(image)

#     # YOLO detection
#     results = yolo_model(image_np)

#     # YOLO plotted image
#     detected_img = results[0].plot()

#     predictions = []

#     boxes = results[0].boxes.xyxy.cpu().numpy()

#     for box in boxes:

#         x1, y1, x2, y2 = map(int, box)

#         crop = image_np[y1:y2, x1:x2]

#         breed_name, confidence = classify_breed(crop)

#         predictions.append({
#             "breed": breed_name,
#             "confidence": confidence
#         })

#     return detected_img, predictions

# # =========================================
# # VIDEO PROCESSING
# # =========================================
# def process_video(video_path):

#     cap = cv2.VideoCapture(video_path)

#     fps = cap.get(cv2.CAP_PROP_FPS)

#     if fps == 0:
#         fps = 25

#     frames = []

#     all_predictions = []

#     while True:

#         ret, frame = cap.read()

#         if not ret:
#             break

#         # YOLO Detection
#         results = yolo_model(frame)

#         detected_frame = results[0].plot()

#         boxes = results[0].boxes.xyxy.cpu().numpy()

#         frame_predictions = []

#         for box in boxes:

#             x1, y1, x2, y2 = map(int, box)

#             crop = frame[y1:y2, x1:x2]

#             if crop.size == 0:
#                 continue

#             breed_name, confidence = classify_breed(crop)

#             frame_predictions.append(
#                 f"{breed_name} ({confidence:.2f})"
#             )

#         if frame_predictions:

#             all_predictions.extend(frame_predictions)

#         # Convert BGR to RGB
#         detected_frame = cv2.cvtColor(
#             detected_frame,
#             cv2.COLOR_BGR2RGB
#         )

#         frames.append(detected_frame)

#     cap.release()

#     # =========================================
#     # CREATE VIDEO USING MOVIEPY
#     # =========================================
#     output_path = tempfile.mktemp(suffix=".mp4")

#     clip = ImageSequenceClip(frames, fps=fps)

#     clip.write_videofile(
#         output_path,
#         codec="libx264",
#         audio=False
#     )

#     return output_path, list(set(all_predictions))

import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["YOLO_CONFIG_DIR"] = "/tmp"

import streamlit as st
import torch
import timm
import cv2
import numpy as np
import tempfile

from PIL import Image
from torchvision import transforms
from ultralytics import YOLO
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

# =========================================
# DEVICE
# =========================================
DEVICE = torch.device("cpu")

# =========================================
# BREED CLASSES
# =========================================
BREED_CLASSES = [
    'Buffalo_Chhattisgarhi',
    'Buffalo_Jaffarabadi',
    'Buffalo_banni',
    'Buffalo_bargur',
    'Buffalo_bhadwari',
    'Buffalo_chilika',
    'Buffalo_gojri',
    'Buffalo_kalahandi',
    'Buffalo_luit',
    'Buffalo_marathwada',
    'Buffalo_mehsana',
    'Buffalo_murrah',
    'Buffalo_nagpuri',
    'Buffalo_nili-ravi',
    'Buffalo_pandharpuri',
    'Buffalo_surti',
    'Buffalo_toda',
    'Cow_Amritmahal',
    'Cow_Ayrshire',
    'Cow_Bargur',
    'Cow_Dangi',
    'Cow_Deoni',
    'Cow_Gir',
    'Cow_Hallikar',
    'Cow_Hariana',
    'Cow_Himachali Pahari',
    'Cow_Kangayam',
    'Cow_Kankrej',
    'Cow_Kenkatha',
    'Cow_Khariar',
    'Cow_Khillari',
    'Cow_Konkan Kapila',
    'Cow_Kosali',
    'Cow_Krishna_Valley',
    'Cow_Ladakhi',
    'Cow_Lakhimi',
    'Cow_Malnad_gidda',
    'Cow_Mewati',
    'Cow_Nari',
    'Cow_Nimari',
    'Cow_Ongole',
    'Cow_Poda Thirupu',
    'Cow_Pulikulam',
    'Cow_Punganur',
    'Cow_Purnea',
    'Cow_Rathi',
    'Cow_Red kandhari',
    'Cow_Red_Sindhi',
    'Cow_Sahiwal',
    'Cow_Shweta Kapila',
    'Cow_Tharparkar',
    'Cow_Umblachery',
    'Cow_Vechur',
    'Cow_bachaur',
    'Cow_badri',
    'Cow_bhelai',
    'Cow_dagri',
    'Cow_gangatari',
    'Cow_gaolao',
    'Cow_ghumsari',
    'Cow_kherigarh',
    'Cow_malvi',
    'Cow_motu',
    'Cow_nagori',
    'Cow_ponwar',
    'Cow_siri',
    'Cow_thutho'
]

# =========================================
# IMAGE TRANSFORM
# =========================================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# =========================================
# LOAD YOLO MODEL
# =========================================
@st.cache_resource
def load_yolo_model():

    model = YOLO("models/best.pt")

    return model

# =========================================
# LOAD RESNET MODEL
# =========================================
@st.cache_resource
def load_resnet_model():

    model = timm.create_model(
        "resnetv2_50",
        pretrained=False,
        num_classes=len(BREED_CLASSES)
    )

    model.load_state_dict(
        torch.load(
            "models/resnetv2_breed_classifier.pth",
            map_location=DEVICE
        )
    )

    model.to(DEVICE)

    model.eval()

    return model

# =========================================
# CLASSIFY CROPPED IMAGE
# =========================================
def classify_crop(crop_img, resnet_model):

    crop_pil = Image.fromarray(crop_img)

    input_tensor = transform(crop_pil)

    input_tensor = input_tensor.unsqueeze(0).to(DEVICE)

    with torch.no_grad():

        outputs = resnet_model(input_tensor)

        probs = torch.softmax(outputs, dim=1)

        conf, pred = torch.max(probs, 1)

    breed = BREED_CLASSES[pred.item()]

    return breed, float(conf.item())

# =========================================
# IMAGE PREDICTION
# =========================================
def detect_and_classify_image(image):

    yolo_model = load_yolo_model()

    resnet_model = load_resnet_model()

    image_np = np.array(image)

    results = yolo_model(
        image_np,
        imgsz=320
    )

    detected_img = results[0].plot()

    predictions = []

    boxes = results[0].boxes.xyxy.cpu().numpy()

    for box in boxes:

        x1, y1, x2, y2 = map(int, box)

        crop = image_np[y1:y2, x1:x2]

        if crop.size == 0:
            continue

        breed, conf = classify_crop(
            crop,
            resnet_model
        )

        predictions.append({
            "breed": breed,
            "confidence": conf
        })

    return detected_img, predictions

# =========================================
# VIDEO PROCESSING
# ========================================
def process_video(video_path):

    yolo_model = load_yolo_model()

    resnet_model = load_resnet_model()

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 25

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Final playable mp4 output
    output_path = tempfile.mktemp(suffix=".mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    all_predictions = set()

    frame_skip = 3
    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # Skip frames for optimization
        if frame_count % frame_skip != 0:
            continue

        results = yolo_model(
            frame,
            imgsz=320,
            verbose=False
        )

        detected_frame = results[0].plot()

        boxes = results[0].boxes.xyxy.cpu().numpy()

        for box in boxes:

            x1, y1, x2, y2 = map(int, box)

            crop = frame[y1:y2, x1:x2]

            if crop.size == 0:
                continue

            breed, conf = classify_crop(
                crop,
                resnet_model
            )

            all_predictions.add(
                f"{breed} ({conf:.2f})"
            )

        out.write(detected_frame)

    cap.release()

    out.release()

    return output_path, list(all_predictions)

