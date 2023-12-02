import cv2
import numpy as np

def find_pink_lines(image):
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the pink color in HSV
    lower_pink = np.array([140, 100, 100])
    upper_pink = np.array([170, 255, 255])

    # Threshold the image to get a binary mask for pink pixels
    pink_mask = cv2.inRange(hsv, lower_pink, upper_pink)

    # Apply a series of morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    pink_mask = cv2.morphologyEx(pink_mask, cv2.MORPH_CLOSE, kernel)
    pink_mask = cv2.morphologyEx(pink_mask, cv2.MORPH_OPEN, kernel)

    # Find contours in the binary mask
    contours, _ = cv2.findContours(pink_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a black background
    output_image = np.zeros_like(image)

    # Draw lines around the pink portions on the black background
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        cv2.drawContours(output_image, [approx], 0, (255, 0, 255), 2)  # Pink color is represented as (255, 0, 255)

    return output_image

# Read the input image
input_image = cv2.imread('demo.png')

# Call the function to find and draw lines around pink portions
output_image = find_pink_lines(input_image)

# Display only the pink lines
cv2.imshow('Pink Lines', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
