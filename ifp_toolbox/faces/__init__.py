import cv2
import os

class FaceDetector(object):
    def __init__(self, scale_factor=1.3, min_neighbors=5):
        module_path = os.path.dirname(__file__)
        classifier_path = os.path.join(module_path, 'haarcascade_frontalface_default.xml')
        self.detector = cv2.CascadeClassifier(classifier_path)      
        if self.detector.empty():
            raise Exception('Classifier xml file was not found.')
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        print self.detector

    def detect_faces(self, I):
        faces = self.detector.detectMultiScale(I, self.scale_factor, self.min_neighbors)
        return faces

    def crop_face_out(self, I, loc):
        (x,y,w,h) = loc
        I_crop = I[y:y+h,x:x+h]
        return I_crop

 
