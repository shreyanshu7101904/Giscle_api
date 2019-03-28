from Scripts.config import api_key, secret_key, url, toStore
from Scripts.detectFace import detectFace
import os
import argparse

if __name__ == "__main__":
    face_ob = detectFace(api_key, secret_key)
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True,
        help="path to input video file")
    args = vars(ap.parse_args())
    try:
        saveframedir = str(os.getcwd()) + "/Scripts/Frames/"
        face_ob.generateImageFromVideo(args["video"], saveframedir)
        os.chdir(saveframedir)
        images_list = list(os.listdir())

        for image_data in images_list:
            payload = face_ob.convertImageToBase64(image_data)
            detcted = face_ob.uploadData(payload = payload, url = url, storage = toStore, image_name = image_data)
            if detcted:
                break
                print("#"*10, "More than 6 face detected", "#"*10)
    except Exception as e:
        print("#"*10, "Exception", e, "Occured", "#"*10)


    