import pytesseract
from pdf2image import convert_from_path
import cv2
import os

def pdf_to_img(pdf):
    pdf_pages = convert_from_path(pdf, dpi=350)
    img_list = []
    for i, page in enumerate(pdf_pages):
        img_path = f'/tmp/page_{i}.jpg'
        page.save(img_path, 'JPEG')
        img_list.append(img_path)
    print('PDF to Image Conversion Successful!')
    return img_list

def bounding_boxes(img_list, show_boxes):
    boxes = {}
    for curr_img in img_list:
        img = cv2.imread(curr_img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, ksize=(9, 9), sigmaX=0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        dilate = cv2.dilate(thresh, kernel, iterations=4)
        contours, _ = cv2.findContours(dilate, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

        temp = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 10000:
                continue
            temp.append([x, y, w, h])
            if show_boxes:
                cv2.rectangle(img, (x, y), (x + w, y + h), color=(255, 0, 255), thickness=3)
                cv2.imshow('Bounding Boxes', img)
                cv2.waitKey(0)
        if show_boxes:
            cv2.destroyAllWindows()
        boxes[curr_img] = temp
    print('Contours saved Successfully!')
    return boxes

def extract_text(boxes):
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    text = ''
    for key in boxes:
        img = cv2.imread(key)
        for x, y, w, h in boxes[key]:
            cropped_image = img[y:y + h, x:x + w]
            _, thresh = cv2.threshold(cropped_image, 127, 255, cv2.THRESH_BINARY)
            text += pytesseract.image_to_string(thresh, config='--psm 6')
    print('Text Extraction Completed!')
    return text

def process_pdf(pdf_file, show_boxes=False):
    if not os.path.isfile(pdf_file):
        print(f'File not found: {pdf_file}')
        return ''
    
    img_list = pdf_to_img(pdf_file)
    boxes = bounding_boxes(img_list, show_boxes)
    text = extract_text(boxes)
    
    return text
