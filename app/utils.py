def process_image(image_path):
    import cv2
    import numpy as np

    # Load image
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV range for gold
    lower_gold = np.array([15, 80, 100])
    upper_gold = np.array([35, 255, 255])

    # Create mask
    mask = cv2.inRange(hsv, lower_gold, upper_gold)

    # Optional: add a margin around the detected gold area
    kernel = np.ones((5, 5), np.uint8)
    mask_dilated = cv2.dilate(mask, kernel, iterations=2)

    # Apply the mask to get the result
    result = cv2.bitwise_and(image, image, mask=mask_dilated)

    return result, mask_dilated