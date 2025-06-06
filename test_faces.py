from insightface.app import FaceAnalysis
import cv2

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0)

# Replace this with an actual image path on your system
img = cv2.imread("/Users/im_tra/Desktop/Deep-Live-Cam/sample.jpg")

faces = app.get(img)
print(f"Detected {len(faces)} face(s)")
for face in faces:
    print(face)
