from PIL import Image, ImageChops, ImageFilter, ImageDraw
import numpy as np
import cv2

threshold = 50
  
for i in range(48):
    img1 = Image.open(f"images/{i}.jpeg")
    img2 = Image.open(f"images/{i+1}.jpeg") 
    diff = ImageChops.difference(img1, img2) 
    diff = diff.convert('L')
    diff = diff.filter(ImageFilter.GaussianBlur(radius=3))

    thresholded_diff = diff.point(lambda p: p > 100 and 255)
    thresholded_np = np.array(thresholded_diff)


    contours, _ = cv2.findContours(thresholded_np, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    diff.convert('RGB')
    if contours:
        draw = ImageDraw.Draw(diff)
        for contour in contours:
            # Find the bounding box of the contour
            bbox = cv2.boundingRect(contour)
            center = (bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2)
            radius = max(bbox[2] // 2, bbox[3] // 2)
            draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline="red", width=2)

    # square_size = 165
    # draw = ImageDraw.Draw(diff)
    # for y in range(200, img1.size[1], square_size):
    #     for x in range(110, img1.size[0], square_size):
    #         # Define the current square region
    #         box = (x, y, x + square_size, y + square_size)

    #         # Crop the thresholded image to the current square
    #         square = thresholded_diff.crop(box)

    #         # Find the brightest point in the square
    #         brightest_point = max(square.getdata())

    #         # If the brightest point is above the threshold, draw a red circle
    #         if brightest_point > 120:
    #             center = (x + square_size // 2, y + square_size // 2)
    #             radius = square_size // 2
    #             draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline="red", width=2)
        

    diff.save(f"tests/{i}-{i+1}.jpeg")
# showing the difference 
diff.show() 