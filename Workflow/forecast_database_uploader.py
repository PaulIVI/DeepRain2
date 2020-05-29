import pickle
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime
from PIL import Image
import numpy as np
import time

#return the cordinates of the pixel by [y (lng), x (lat)]
#TODO es kommen bei einem 900x900 grid natürlich andere Pixel raus als bei 1100x900, aber sind diese Werte richtig?
def return_pixel_from_coordinates(latitude, longitude, coordinate_lists):
    listLatitude = coordinate_lists[0]
    listLongitude = coordinate_lists[1]
    listCoordinates = coordinate_lists[2]

    #check, if the pixel coordinates for this latitude and longitude is already calculated
    for latitude_index in range(len(latitude_longitude_pixels)):
        if latitude_longitude_pixels[latitude_index][0] == latitude:
            if latitude_longitude_pixels[latitude_index][1] == longitude:
                return latitude_longitude_pixels[latitude_index][2]

    dist_to_pixel = []
    for idx in range(len(listLatitude)):
        dist_to_pixel.append(np.linalg.norm([latitude - listLatitude[idx], longitude - listLongitude[idx]]))
    index_of_min_dist = dist_to_pixel.index(min(dist_to_pixel))

    pixel_coordinates = listCoordinates[index_of_min_dist]

    latitude_longitude_pixels.append([latitude, longitude, pixel_coordinates])

    return pixel_coordinates

def return_rain_intense_from_forecast_by_latlng(latitude, longitude, image, coordinate_lists):

    #get the pixel coordinate for this long and latitude in format [y,x]
    pixel_cordinate = return_pixel_from_coordinates(latitude, longitude, coordinate_lists)

    #get the value of the pixel
    rain_intense = image.getpixel((pixel_cordinate[1], pixel_cordinate[0]))

    return rain_intense


def delete_collection(coll_ref):
    docs = coll_ref.stream()
    for doc in docs:
        doc.reference.delete()

def upload_data_to_firbase(forecast_images, time_of_forecasts, coordinate_lists):
    # Never, ever upload this Certificate file to git
    cred = credentials.Certificate('./deeprain-firebase-adminsdk-xpcbj-bcbc99b37e.json')
    default_app = firebase_admin.initialize_app(cred, {'storageBucket': 'deeprain.appspot.com'})
    bucket = storage.bucket()
    db = firestore.client()


    # Counter for the ID of Data
    ID = 0

    # list for all latitudes and longitudes which are already calulated
    # [latitude, longitude, pixels]
    latitude_longitude_pixels = []


    # all regions where are users
    regions = db.collection(u'Regions').stream()
    regions = list(regions)

    # For each region where are users, (Device Tokens in the Regions/Region/tokens collection), a forecast need to be pushed
    for region in regions:
        start = time.time()
        print('Start with: ', region.id)
        ID = 0
        #get the latitude and longitude of the current region
        region_lat_lng = region.to_dict()
        region_latitude = region_lat_lng['Latitude']
        region_longitude = region_lat_lng['Longitude']

        forecast_collection = db.collection('Regions').document(region.id).collection('forecast')

        #delete the old data
        delete_collection(forecast_collection)

        is_pushnotification_sended = False

        #calculate for each image the rain intense and load it to firebase
        for image in range(len(forecast_images)):
            # the unique id for the documents of database.
            documentID = 'deeprain_' + time_of_forecasts[image] + '_' + str(ID)

            rainIntense = return_rain_intense_from_forecast_by_latlng(region_latitude, region_longitude, forecast_images[image], coordinate_lists)

            #upload the forecast data to firebase
            doc_ref = forecast_collection.document(str(documentID))
            doc_ref.set({
                'rainIntense': rainIntense,
                'time': time_of_forecasts[image]
            })

            ID = ID +1

            # send push notifications to devices.
            if is_pushnotification_sended == False:
                if(rainIntense > 90):
                    doc_ref = db.collection('RainWarningPushNotification').document(str(documentID))
                    doc_ref.set({
                        'title': 'Es gibt eine Regenwarnung!',
                        'body': 'Nehmen Sie besser Ihren Regenschirm mit, es wird in 30 Minuten regenen!',
                        'time_before_raining': '30',
                        'region': region.id
                    })
                    is_pushnotification_sended = True
        is_pushnotification_sended == False

        # print('Upload erfolgeich. ID:' + str(ID) + '. rainIntense: ' + str(rainIntense) + '. time: ' + str(current_time))
        end = time.time()
        print('Time needed: ', end - start)

        #db.collection('Regions').document(region.id).collection('forecast').document(forecasts[0].id).delete()