import cv2 as cv
import easyocr
from PIL import Image, ImageOps
from paddleocr import PPStructure, draw_structure_result, save_structure_res
from matplotlib import pyplot as plt  # plot images
import numpy as np
import os  # folder directory navigation


class OCR:
    def __init__(self, work_id):
        self.work_id = work_id

    def paddleTextDetector(self, path, imageName):
        img_path = os.path.join(path, imageName)
        table_engine = PPStructure(show_log=True)

        # save_folder = './table'
        # img_path = 'Image3.jpg'

        def sharpen_image(im):
            kernel = np.ones((6, 6), np.float32)/90
            im = cv.filter2D(im, -2, kernel)
            return im

        img = cv.imread(img_path, 0)
        blurred_frame = cv.GaussianBlur(img, (3, 3), 0)
        blurred_frame = sharpen_image(img)

        img = cv.resize(blurred_frame, (1200, 1800))

        result = table_engine(img)
        # save_structure_res(result, save_folder,
        #                    os.path.basename(img_path).split('.')[0])

        for line in result:
            line.pop('img')

        font_path = './PaddleOCR/doc/fonts/latin.ttf'
        image = Image.open(img_path).convert('RGB')
        im_show = draw_structure_result(image, result, font_path=font_path)
        im_show = Image.fromarray(im_show)

        im_show.save(
            './OCR_work_order 1_/dtv_999_1478523696_1_1234548951651.jpg')
        # im_show.save('result.jpg')

        res = self.easyOcrDetector(
            "./OCR_work_order 1_/dtv_999_1478523696_1_1234548951651.jpg")
        print(res)

    def easyOcrDetector(self, image):
        reader = easyocr.Reader(['en'], gpu=True)

        img = cv.imread(image, 0)
        # height, width, _ = img.shape
        # img = img[img.shape[0]:img.shape[1]//2]

        height = img.shape[0]
        width = img.shape[1]

        # Cut the image in half
        width_cutoff = width // 2
        s2 = img[:, width_cutoff:]

        _, binary = cv.threshold(s2, 150, 255, cv.THRESH_BINARY_INV)
        kernel = np.ones((2, 2), np.uint8)
        opening = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
        results = reader.readtext(opening, detail=1, paragraph=False)

        for (bbox, text, prob) in results:
            # (tl, tr, br, bl) = bbox
            # tl = (int(tl[0]), int(tl[1]))
            # tr = (int(tr[0]), int(tr[1]))
            # br = (int(br[0]), int(br[1]))
            # bl = (int(bl[0]), int(bl[1]))

            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()

        a = []
        for re in results:
            a.append(re[1])

        return a
