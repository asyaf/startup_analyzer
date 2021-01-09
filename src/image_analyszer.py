import cv2
from pyagender import PyAgender


if __name__ == '__main__':
    img_path = r'C:\Users\Asya\PycharmProjects\startup_analyzer\data\1NS.jpg'
    img = cv2.imread(img_path)
    agender = PyAgender()
    cv2.imshow('t', img)
    cv2.waitKey(0)
    faces = agender.detect_genders_ages(img)
    print(faces)
