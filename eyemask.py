import cv2


class EyeMaskerApp:
    def __init__(self):
        # Open the default webcam
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise IOError("Could not open webcam.")

        # Load Haar Cascade classifiers
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )

        if self.face_cascade.empty() or self.eye_cascade.empty():
            raise IOError("Failed to load Haar Cascade XML files.")

        # Load emoji image
        self.emoji = cv2.imread("274c.png", cv2.IMREAD_UNCHANGED)
        if self.emoji is None:
            raise IOError("Failed to load emoji image. Check file path.")

    def run(self):
        print("Eye Masker Started")
        print("Press 'Q' to quit.")

        while True:
            # Capture frame
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to read frame from webcam.")
                break

            # Mirror the image
            frame = cv2.flip(frame, 1)

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )

            # Process each detected face
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]

                # Detect eyes inside the face
                eyes = self.eye_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.1,
                    minNeighbors=10,
                    minSize=(15, 15)
                )

                # Overlay emoji on each detected eye
                for (ex, ey, ew, eh) in eyes:
                    # Adjust coordinates to full frame
                    frame_x = x + ex
                    frame_y = y + ey

                    # Resize emoji to eye size
                    emoji_resized = cv2.resize(self.emoji, (ew, eh))

                    # Paste emoji on frame
                    frame[frame_y:frame_y+eh, frame_x:frame_x+ew] = emoji_resized[:, :, :3]

            # Display the result
            cv2.imshow("Eye Emoji Mask", frame)

            # Quit when Q is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = EyeMaskerApp()
    app.run()
