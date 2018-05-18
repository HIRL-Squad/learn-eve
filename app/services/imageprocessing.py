import json

import cv2
import os
import numpy as np
from flask import make_response

from Documents.testdata import Testdata

COLUMN_COUNT = 10
ROW_COUNT = 11
dir_path = os.path.dirname(os.path.realpath(__file__))
tick_img_path = dir_path + '/../resources/images/check_bg.png'
cross_img_path = dir_path + '/../resources/images/cross_bg.png'
overlay_tick_img = cv2.imread(tick_img_path, -1)
overlay_cross_img = cv2.imread(cross_img_path, -1)


def load_symbol_img(digit):
    img_path = dir_path + '/../resources/images/vas' + str(digit) + '.png'
    img = cv2.imread(filename=img_path, flags=0)
    # expand the image into RGBA 4 channels
    alpha_channel = np.ones(img.shape,dtype=img.dtype) * 255
    img = cv2.merge((img, img, img, alpha_channel))
    return img


symbol_image_dict = {}
for i in range(1, 10):
    symbol_image_dict[i] = load_symbol_img(i)


def load_testdata(test_id):
    data = Testdata.objects(id=test_id).first()
    if data:
        return data
    raise FileNotFoundError('Cannot find testdata object with given id')


def draw_greyscale_digit(points_list, width, height):
    # Create a black image
    img = np.zeros((height, width, 4), np.float32)
    img.fill(1.)

    processed_array = [np.array(item, np.int32).reshape((-1, 1, 2)) for item in points_list]

    img = cv2.polylines(img, processed_array, False, (0., 0., 0., 1), 12)

    return img


def strip_label(point_list):
    result = [[item['x'], item['y']] for item in point_list]
    return result


def fit_symbol_img(img, width, height):
    img = cv2.resize(img, (width, height))
    return img


def overlay_image_on_top(img, overlay_img):
    img = img * 255
    overlay_img = overlay_img
    if img.shape != overlay_img.shape:
        raise ValueError('Overlay image and target image not the same shape.')
    alpha_s = overlay_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s
    for c in range(0, 3):
        img[:, :, c] = (alpha_s * overlay_img[:, :, c] +
                        alpha_l * img[:, :, c])
    img = img / 255.0
    return img


def render_test_result(test_id):
    testdata = load_testdata(test_id)
    result = testdata['test'].get('result', None)
    vas_cog_block = testdata['test']['vas_cog_block']
    vas_block_size = testdata['test']['vas_block_size']
    width = vas_block_size['width']
    height = vas_block_size['height']
    symbol_height = width * 3 // 4
    big_img = np.zeros(((height + symbol_height) * ROW_COUNT, width * COLUMN_COUNT, 4), np.float32)
    big_img.fill(1.)
    current_column_index = 0
    current_row_index = 0

    for i in range(len(vas_cog_block)):
        data = vas_cog_block[str(i)]
        path_list = data['path_list']
        if path_list:
            # draw current block
            points_list = [strip_label(item['point_list']) for item in path_list]
            img = draw_greyscale_digit(points_list, width, height)
            # overlay ticks on current block
            if result:
                if result[str(i)]:
                    overlay_img = overlay_tick_img
                else:
                    overlay_img = overlay_cross_img
                overlay_img = cv2.resize(overlay_img, (img.shape[1], img.shape[0]))
                img = overlay_image_on_top(img, overlay_img)
            # line up current block
            y_offset = current_row_index * width
            x_offset = current_column_index * (height + symbol_height) + symbol_height
            big_img[x_offset:x_offset + height, y_offset:y_offset + width] = img
        # draw symbol images
        digit = data['vas_ques']
        symbol_img = symbol_image_dict[digit]
        symbol_img = fit_symbol_img(symbol_img, width, symbol_height)
        y_offset = current_row_index * width
        x_offset = current_column_index * (height + symbol_height)
        big_img[x_offset:x_offset + symbol_height, y_offset:y_offset + width] = symbol_img
        # increment index
        current_row_index += 1
        if current_row_index >= COLUMN_COUNT:
            current_column_index += 1
            current_row_index = 0
    big_img *= 255  # get back the correct range, normalized value won't display correctly
    _, encoded_img = cv2.imencode('.png', big_img)
    return encoded_img
