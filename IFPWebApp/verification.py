import logging
import re
import io
import base64
import random
import string
import time
from datetime import datetime
from PIL import Image, ImageEnhance
import pytesseract
from pdf2image import convert_from_bytes
import cv2
import numpy as np
import face_recognition

logger = logging.getLogger(__name__)

# ==========================
# IMAGE PROCESSING & OCR
# ==========================

def enhance_image_for_ocr(image):
    try:
        image = image.convert('L')  # Grayscale
        image = ImageEnhance.Contrast(image).enhance(2.0)
        image = ImageEnhance.Sharpness(image).enhance(2.0)
        return image
    except Exception as e:
        logger.error(f"Image enhancement error: {e}")
        return image

def extract_id_from_image(image):
    try:
        processed_image = enhance_image_for_ocr(image)
        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(processed_image, config=config)
        logger.debug("OCR Text Output:\n%s", text)
        match = re.search(r'\b\d{13}\b', text)
        return match.group() if match else None
    except Exception as e:
        logger.error(f"OCR extraction error: {e}")
        return None

def extract_id_from_pdf(pdf_file):
    try:
        images = convert_from_bytes(pdf_file.read())
        for image in images:
            extracted_id = extract_id_from_image(image)
            if extracted_id:
                return extracted_id
        return None
    except Exception as e:
        logger.error(f"PDF OCR error: {e}")
        return None

# ==========================
# UTILITY: OTP Generator
# ==========================

def generate_otp(length=6):
    """Generate OTP with at least 2 digits"""
    if length < 2:
        raise ValueError("OTP must be at least 2 characters long")
    digits = random.choices(string.digits, k=2)
    others = random.choices(string.ascii_uppercase + string.digits, k=length - 2)
    otp_chars = digits + others
    random.shuffle(otp_chars)
    return ''.join(otp_chars)

# ==========================
# FACE VERIFICATION
# ==========================

def verify_faces(stored_image_path, captured_image_data):
    try:
        # Get encoding from stored photo
        stored_image = face_recognition.load_image_file(stored_image_path)
        stored_encoding = face_recognition.face_encodings(stored_image)
        
        if not stored_encoding:
            return False, 'No face detected in stored photo.'
        
        # Process captured image
        decoded_image = base64.b64decode(captured_image_data.split(',')[1])
        nparr = np.frombuffer(decoded_image, np.uint8)
        captured_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_captured_img = captured_img[:, :, ::-1]
        
        captured_encoding = face_recognition.face_encodings(rgb_captured_img)
        
        if not captured_encoding:
            return False, 'No face detected in captured image.'
        
        results = face_recognition.compare_faces([stored_encoding[0]], captured_encoding[0], tolerance=0.6)
        return results[0], 'Face verification successful' if results[0] else 'Face verification failed'
        
    except Exception as e:
        logger.error(f"Face verification error: {e}")
        return False, f'Error: {str(e)}'