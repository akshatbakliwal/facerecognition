import face_recognition as fr


class Register:

    def __init__(self):
        self.known_face_encodings=[]
        self.known_face_names=[]

    def register_user(self, name, image_file):
        face_encoding = fr.face_encodings(fr.load_image_file(image_file))[0]
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(name)

    def get_known_encodings(self):
        return self.known_face_encodings

    def get_known_faces(self):
        return self.known_face_encodings, self.known_face_names