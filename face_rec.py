import face_recognition as fr
import numpy as np
import os

class Register:

    def __init__(self):
        self.known_face_encodings=[]
        self.known_face_names=[]

    def register_user(self, name, image_file):
        print(image_file, name)
        face_encoding = fr.face_encodings(fr.load_image_file(image_file))[0]
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(name)

    def get_known_encodings(self):
        return self.known_face_encodings

    def get_known_faces(self):
        return self.known_face_encodings, self.known_face_names


class Predict:

    @staticmethod
    def get_predictions(rgb_small_frame, register):

        known_face_encodings, known_face_names = register.get_known_faces()

        face_locations = fr.face_locations(rgb_small_frame)
        face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = fr.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = fr.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] > 0.45:
                name = "Unknown"
            elif matches[best_match_index]:
                name = known_face_names[best_match_index] + '({0:.3f})'.format(face_distances[best_match_index])

            face_names.append(name)

        return face_locations, face_names
