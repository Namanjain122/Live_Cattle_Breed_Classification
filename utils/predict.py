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
# CONFIGURATION & CLASSES
# =========================================
BREED_CLASSES = ['Buffalo_Chhattisgarhi', 'Buffalo_Jaffarabadi', 'Buffalo_banni', 'Buffalo_bargur', 'Buffalo_bhadwari', 'Buffalo_chilika', 'Buffalo_gojri', 'Buffalo_kalahandi', 'Buffalo_luit', 'Buffalo_marathwada', 'Buffalo_mehsana', 'Buffalo_murrah', 'Buffalo_nagpuri', 'Buffalo_nili-ravi', 'Buffalo_pandharpuri', 'Buffalo_surti', 'Buffalo_toda', 'Cow_Amritmahal', 'Cow_Ayrshire', 'Cow_Bargur', 'Cow_Dangi', 'Cow_Deoni', 'Cow_Gir', 'Cow_Hallikar', 'Cow_Hariana', 'Cow_Himachali Pahari', 'Cow_Kangayam', 'Cow_Kankrej', 'Cow_Kenkatha', 'Cow_Khariar', 'Cow_Khillari', 'Cow_Konkan Kapila', 'Cow_Kosali', 'Cow_Krishna_Valley', 'Cow_Ladakhi', 'Cow_Lakhimi', 'Cow_Malnad_gidda', 'Cow_Mewati', 'Cow_Nari', 'Cow_Nimari', 'Cow_Ongole', 'Cow_Poda Thirupu', 'Cow_Pulikulam', 'Cow_Punganur', 'Cow_Purnea', 'Cow_Rathi', 'Cow_Red kandhari', 'Cow_Red_Sindhi', 'Cow_Sahiwal', 'Cow_Shweta Kapila', 'Cow_Tharparkar', 'Cow_Umblachery', 'Cow_Vechur', 'Cow_bachaur', 'Cow_badri', 'Cow_bhelai', 'Cow_dagri', 'Cow_gangatari', 'Cow_gaolao', 'Cow_ghumsari', 'Cow_kherigarh', 'Cow_malvi', 'Cow_motu', 'Cow_nagori', 'Cow_ponwar', 'Cow_siri', 'Cow_thutho']
DEVICE = torch.device("cpu")

class ModelHandler:
    @staticmethod
    @st.cache_resource
    def load_models():
        yolo = YOLO("models/best.pt")
        resnet = timm.create_model("resnetv2_50", pretrained=False, num_classes=len(BREED_CLASSES))
        resnet.load_state_dict(torch.load("models/resnetv2_breed_classifier.pth", map_location=DEVICE))
        return yolo, resnet.to(DEVICE).eval()

    @staticmethod
    def transform_image(img):
        transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
        return transform(Image.fromarray(img)).unsqueeze(0).to(DEVICE)

# =========================================
# PROCESSING LOGIC
# =========================================
def classify_crop(crop_img, resnet):
    input_tensor = ModelHandler.transform_image(crop_img)
    with torch.no_grad():
        outputs = resnet(input_tensor)
        probs = torch.softmax(outputs, dim=1)
        conf, pred = torch.max(probs, 1)
    return BREED_CLASSES[pred.item()], float(conf.item())

def process_media(media_input, is_video=False):
    yolo, resnet = ModelHandler.load_models()
    
    if not is_video:
        # Image Logic
        img = np.array(media_input)
        results = yolo(img, imgsz=320)
        detected_img = results[0].plot()
        preds = []
        for box in results[0].boxes.xyxy.cpu().numpy():
            x1, y1, x2, y2 = map(int, box)
            crop = img[y1:y2, x1:x2]
            if crop.size > 0:
                breed, conf = classify_crop(crop, resnet)
                preds.append(f"{breed} ({conf:.2f})")
        return detected_img, preds
    
    else:
        # Video Logic
        cap = cv2.VideoCapture(media_input)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        frames, all_preds = [], set()
        
        while True:
            ret, frame = cap.read()
            if not ret: break
            results = yolo(frame, imgsz=320)
            det_frame = cv2.cvtColor(results[0].plot(), cv2.COLOR_BGR2RGB)
            frames.append(det_frame)
            for box in results[0].boxes.xyxy.cpu().numpy():
                x1, y1, x2, y2 = map(int, box)
                crop = frame[y1:y2, x1:x2]
                if crop.size > 0:
                    b, c = classify_crop(crop, resnet)
                    all_preds.add(f"{b} ({c:.2f})")
        
        cap.release()
        out_path = tempfile.mktemp(suffix=".mp4")
        ImageSequenceClip(frames, fps=fps).write_videofile(out_path, codec="libx264", audio=False, logger=None)
        return out_path, list(all_preds)

# =========================================
# STREAMLIT UI
# =========================================
st.title("Livestock Breed Classifier")
uploaded_file = st.file_uploader("Upload Image/Video", type=["jpg", "png", "mp4"])

if uploaded_file:
    if uploaded_file.type.startswith("image"):
        img = Image.open(uploaded_file)
        res_img, preds = process_media(img)
        st.image(res_img)
        st.write("Detected Breeds:", preds)
    else:
        with open("temp_vid.mp4", "wb") as f: f.write(uploaded_file.read())
        path, preds = process_media("temp_vid.mp4", is_video=True)
        st.video(path)
        st.write("Identified Breeds in Video:", preds)
