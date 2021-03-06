import os

import cv2
import numpy


def align_face(I, src_points_in, dest_points_in, output_img_size):

    src_points = numpy.zeros((3, 2), 'float32')
    dest_points = numpy.zeros((3, 2), 'float32')

    for i in range(len(src_points_in)):
        src_points[i, :] = numpy.array(src_points_in[i])
        dest_points[i, :] = numpy.array(dest_points_in[i])

    M = cv2.getAffineTransform(src_points, dest_points)
    I_aligned = cv2.warpAffine(I, M, output_img_size)
    return I_aligned


class FaceDetector(object):
    def __init__(self, scale_factor=1.3, min_neighbors=5,
                 min_size_scalar=0.25, max_size_scalar=0.75):
        module_path = os.path.dirname(__file__)
        classifier_path = os.path.join(module_path,
                                       'haarcascade_frontalface_default.xml')
        self.detector = cv2.CascadeClassifier(classifier_path)
        if self.detector.empty():
            raise Exception('Classifier xml file was not found.')
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size_scalar = min_size_scalar
        self.max_size_scalar = max_size_scalar
        #print self.detector

    def detect_faces(self, I):
        height, width, num_channels = I.shape
        min_dim = numpy.min([height, width])
        min_size = (int(min_dim*self.min_size_scalar),
                    int(min_dim*self.min_size_scalar))
        max_size = (int(min_dim*self.max_size_scalar),
                    int(min_dim*self.max_size_scalar))

        faces = self.detector.detectMultiScale(I, self.scale_factor,
                                               self.min_neighbors, 0,
                                               min_size,
                                               max_size)
        return faces

    def crop_face_out(self, I, loc):
        (x, y, w, h) = loc
        I_crop = I[y:y+h, x:x+w, :]
        return I_crop


class EyeDetector(object):
    def __init__(self, scale_factor=1.3, min_neighbors=5):
        module_path = os.path.dirname(__file__)
        classifier_path = os.path.join(module_path, 'haarcascade_eye.xml')
        self.detector = cv2.CascadeClassifier(classifier_path)
        if self.detector.empty():
            raise Exception('Classifier xml file was not found.')
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        #print self.detector

    def detect_eyes(self, I):
        eyes = self.detector.detectMultiScale(I, self.scale_factor,
                                              self.min_neighbors)
        return eyes


class NoseDetector(object):
    def __init__(self, scale_factor=1.3, min_neighbors=5):
        module_path = os.path.dirname(__file__)
        classifier_path = os.path.join(module_path, 'haarcascade_mcs_nose.xml')
        self.detector = cv2.CascadeClassifier(classifier_path)
        if self.detector.empty():
            raise Exception('Classifier xml file was not found.')
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        #print self.detector

    def detect_noses(self, I):
        noses = self.detector.detectMultiScale(I, self.scale_factor,
                                               self.min_neighbors)
        return noses
