import requests
import cv2
import base64
import time
import os
import math


class detectFace:
    

    def __init__(self, api_key, secret):
        self.api_key = api_key
        self.secret = secret


    def generateImageFromVideo(self, video, loc):
        vidcap = cv2.VideoCapture(video)
        success,image = vidcap.read()
        count = 1
        frameRate = vidcap.get(5)
        while vidcap.isOpened():
            frameId = vidcap.get(1) 
            ret, frame = vidcap.read()
            if (ret != True):
                break
            if (frameId % math.floor(frameRate) == 0):
                filename = loc + "frame" + str(count) + ".jpeg"
                cv2.imwrite(filename, frame)
                count += 1
        vidcap.release()



    def convertImageToBase64(self, image_path):
        img = open(image_path,'rb')
        img = img.read()
        image = base64.b64encode(img)
        payload = {'image':image}
        print("#"*10, "Converted image", "#"*10)

        return payload


    def uploadData(self, payload, url, storage, image_name):
        response = requests.post(
            url + ':80/image',
            files=payload, 
            headers={'token':self.api_key,'store': storage}
            )
        if response.ok:
            print(response)
            result =response.json()           
            print(result)
            val = len(result['Data'][2].keys())
            print(len(result['Data'][2].keys()))
            if val >6:
                try:
                    os.system('spd-say "Alert detected more than 6 people."')
                    return 1, val
                except Exception as ex:
                    print("#"*10, "Speech processing software not installed", "#"*10)
                    print("#"*10, "Alert Alert Alert", "#"*10)
            else:
                print("#"*10, "no issues", "#"*10)
                return 0
        else:
            print("#"*10, "Kindly check your api_key or Internet connection", "#"*10)
