import cv2


class EyeMaskerApp:

    def __init__(self):
        # Initialize video capture
        self.cap = cv2.VideoCapture(0)

        # Load both Face and Eye Haar Cascades
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

        if self.face_cascade.empty() or self.eye_cascade.empty():
            raise IOError("Unable to load one or more cascade classifier XML files.")

    def run(self):
        print("Eye Masker Started.")
        print("Press 'q' to Quit")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame from camera.")
                break

            # Mirror the frame for a natural feel
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 1. First, detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100)
            )

            for x, y, w, h in faces:
                # Isolate the Regions of Interest (ROI) for the face
                # This prevents the eye detector from finding "eyes" in the background
                roi_gray = gray[y : y + h, x : x + w]
                roi_color = frame[y : y + h, x : x + w]

                # 2. Detect eyes within the face region
                eyes = self.eye_cascade.detectMultiScale(
                    roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(15, 15)
                )

                for ex, ey, ew, eh in eyes:
                    # Calculate center and radius for the eye circle
                    eye_center = (ex + ew // 2, ey + eh // 2)
                    radius = int(max(ew, eh) * 0.6)

                    # Draw solid purple circle on the color ROI
                    # BGR Color: Purple is (128, 0, 128) or bright magenta/purple (255, 0, 128)
                    # thickness = -1 makes the circle completely solid (opaque)
                    cv2.circle(roi_color, eye_center, radius, (255, 0, 128), thickness=-1)

            # Display the result
            cv2.imshow("Opaque Eye Masker", frame)

            # Check for quit key
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = EyeMaskerApp()
    app.run()
