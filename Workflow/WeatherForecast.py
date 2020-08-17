from CreateRainPNG import create_rain_image, resize_images, take_slice_of_image
import numpy as np
from tensorflow.keras.models import load_model
import PIL
from PIL import Image
from Database import replace_forecast_in_firebase
from dwd_data import get_new_radar_pngs
from NeuralNetwork import predict_weather
from time import sleep
from transform import *
import os

PATH_TO_FORECAST_DIR = '/home/paul/Documents/Master1/DeepRain_Teamproject/HomeOffice/Workflow/forecast/'
HISTORICAL_PICTURE_PATH = '/home/paul/Documents/Master1/DeepRain_Teamproject/HomeOffice/Workflow/historical_data/images/'
SCLICE_PICTURE_PATH = '/home/paul/Documents/Master1/DeepRain_Teamproject/HomeOffice/Workflow/historical_data/slices/'
FORECAST_GRAYSCALE_PATH = '/home/paul/Documents/Master1/DeepRain_Teamproject/HomeOffice/Workflow/forecast_grayscale/'
HISTORICAL_RADAR_DATA_PATH = '/home/paul/Documents/Master1/DeepRain_Teamproject/HomeOffice/Workflow/historical_data/bin/'
PATH_TO_NN = '/home/paul/Documents/Master1/DeepRain_Teamproject/HomeOffice/Workflow/NeuralNetworks/UNet64_categorical_crossentropy448x448x5.h5'
DIMENSION = (448,448)
TARGET_DIMENSION = [450, 450]
IMAGE_POS = [0, 0]
RESIZE = True
SLICES = [256, 320, 256, 320]
SLICES = [800, 864, 450, 514]
SLICES = [389, 453, 218, 282]
SLICES = [180, 116, 345, 409]
SLICES = [116, 180, 345, 409]
SLICES = [100, 548, 200, 648]
SLICES = [0, 896, 0, 896]
INPUT_TRANSFORMATIONS = [Normalize()]
OUTPUT_TRANSFORMATIONS = [from_sparse_categorical()]
# INPUT_TRANSFORMATIONS = None
NUMBER_OF_INPUT_IMAGES = 5
NUMBER_OF_PREDICTIONS = 10
NUMBER_OF_HISTORICAL_IMAGES = 10
# HISTORICAL_RADAR_DATA_ZIPPED_PATH = '/home/paul/Documents/Master1/DeepRain_Teamproject/HomeOffice/Workflow/historical_data/zipped/'


if __name__ == '__main__':
    model = load_model(PATH_TO_NN)
    new_radar_data_downloaded = False
    while True:
        while not new_radar_data_downloaded:
            new_radar_data_downloaded = get_new_radar_pngs(HISTORICAL_RADAR_DATA_PATH, HISTORICAL_PICTURE_PATH)
            if not new_radar_data_downloaded:
                print('New radar data is not available')
                sleep(5)
        new_radar_data_downloaded = False

        if SLICES is not None:
            take_slice_of_image(SLICES, HISTORICAL_PICTURE_PATH, SCLICE_PICTURE_PATH, NUMBER_OF_HISTORICAL_IMAGES)
        else:
            SCLICE_PICTURE_PATH = HISTORICAL_PICTURE_PATH
        if RESIZE is not None:
            resize_images(DIMENSION, SCLICE_PICTURE_PATH, FORECAST_GRAYSCALE_PATH, NUMBER_OF_HISTORICAL_IMAGES, reverse=SLICES is None)
        print('Predicting the weather')
        predict_weather(model, NUMBER_OF_INPUT_IMAGES, NUMBER_OF_PREDICTIONS, FORECAST_GRAYSCALE_PATH,
                        transform_input=INPUT_TRANSFORMATIONS, transform_output=OUTPUT_TRANSFORMATIONS)

        print('Create forecast images')
        forecast_picture_list = os.listdir(FORECAST_GRAYSCALE_PATH)
        forecast_picture_list.sort()

        historical_images = []
        for path in forecast_picture_list[:10]:
            img = np.asanyarray(PIL.Image.open(FORECAST_GRAYSCALE_PATH + path, mode='r'))
            img_rgba = np.asanyarray(PIL.Image.open(FORECAST_GRAYSCALE_PATH + path, mode='r').convert(mode='RGBA'))
            historical_images.append(PIL.Image.fromarray(create_rain_image(img, img_rgba, TARGET_DIMENSION, IMAGE_POS), mode='RGBA'))
        #historical_images.reverse()

        forecast_images = []
        for path in forecast_picture_list[10:]:
            img = np.asanyarray(PIL.Image.open(FORECAST_GRAYSCALE_PATH + path, mode='r'))
            img_rgba = np.asanyarray(PIL.Image.open(FORECAST_GRAYSCALE_PATH + path, mode='r').convert(mode='RGBA'))
            forecast_images.append(PIL.Image.fromarray(create_rain_image(img, img_rgba, TARGET_DIMENSION, IMAGE_POS), mode='RGBA'))

        print('Upload forecast images')
        replace_forecast_in_firebase(historical_images, forecast_images, PATH_TO_FORECAST_DIR)
        print('Done. Weather Forecast is up to date')