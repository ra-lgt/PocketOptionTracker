import cv2
import pyautogui
import numpy as np

# Specify the screen resolution (adjust as needed)
screen_width, screen_height = pyautogui.size()

# Specify the output video file and codec
output_file = 'screen_recording.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 30.0
out = cv2.VideoWriter(output_file, fourcc, fps, (screen_width, screen_height))

try:
    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)

        # Convert the frame from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the frame
        cv2.imshow('Screen Recording', frame)

        # Write the frame to the output video file
        out.write(frame)

        # Break the loop if the user presses 'q'
        if cv2.waitKey(1) == ord('q'):
            break

finally:
    # Release the video writer and close the OpenCV window
    out.release()
    cv2.destroyAllWindows()
