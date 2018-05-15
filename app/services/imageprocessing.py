import json

import cv2
import os
import numpy as np
from flask import make_response

from Documents.testdata import Testdata

COLUMN_COUNT = 10
ROW_COUNT = 11


def load_testdata(test_id):
    data = Testdata.objects(id=test_id).first()
    if data:
        return data
    raise FileNotFoundError('Cannot find testdata object with given id')


def draw_greyscale_digit(points_list, width, height):
    # Create a black image
    img = np.zeros((height, width, 1), np.float32)
    img.fill(1.)

    processed_array = [np.array(item, np.int32).reshape((-1, 1, 2)) for item in points_list]

    img = cv2.polylines(img, processed_array, False, 0., 12)

    return img


def strip_label(point_list):
    result = [[item['x'], item['y']] for item in point_list]
    return result


def render_test_result(test_id):
    testdata = load_testdata(test_id)
    vas_cog_block = testdata['test']['vas_cog_block']
    vas_block_size = testdata['test']['vas_block_size']
    width = vas_block_size['width']
    height = vas_block_size['height']
    big_img = np.zeros((height * ROW_COUNT, width * COLUMN_COUNT, 1), np.float32)
    big_img.fill(1.)
    current_column_index = 0
    current_row_index = 0
    for index, data in vas_cog_block.items():
        path_list = data['path_list']
        if path_list:
            # draw current block
            points_list = [strip_label(item['point_list']) for item in path_list]
            img = draw_greyscale_digit(points_list, width, height)
            # line up current block
            y_offset = current_row_index * width
            x_offset = current_column_index * height
            big_img[x_offset:x_offset + height, y_offset:y_offset + width] = img
        # increment index
        current_row_index += 1
        if current_row_index >= 10:
            current_column_index += 1
            current_row_index = 0
    big_img *= 255  # get back the correct range, normalized value won't display correctly
    _, encoded_img = cv2.imencode('.png', big_img)
    return encoded_img
