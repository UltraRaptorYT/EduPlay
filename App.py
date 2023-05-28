from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import os.path
import numpy as np
import streamlit as st
from pdf2image import convert_from_path
from PIL import Image
import streamlit.components.v1 as components


# Set the target width and height

st.markdown("<h1 style='text-align: center;'>AI Assistive Tool</h1>", unsafe_allow_html=True)

# Get the Presentation Slides from Streamlit Website,

uploaded_file = st.file_uploader("Choose a PDF file",  key="my_file_uploader", type="pdf")

st.markdown("<h6 style='text-align: center;'>pinky and thumb to move slide  ||   2 fingers for pointer   ||   1 finger to draw ||   3 finger to erase</h6>", unsafe_allow_html=True)
components.html(
    """
    <head>
    <title>Bootstrap Example</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
  
  </head>
  <body>
  
  <!-- Carousel -->
  <div id="demo" class="carousel slide" data-bs-ride="carousel">
  
    <!-- Indicators/dots -->
    <div class="carousel-indicators">
      <button type="button" data-bs-target="#demo" data-bs-slide-to="0" class="active"></button>
      <button type="button" data-bs-target="#demo" data-bs-slide-to="1"></button>
      <button type="button" data-bs-target="#demo" data-bs-slide-to="2"></button>
      <button type="button" data-bs-target="#demo" data-bs-slide-to="3"></button>
      <button type="button" data-bs-target="#demo" data-bs-slide-to="4"></button>
    </div>

  <!-- Indicators/dots
    <!-- The slideshow/carousel -->
    <div class="carousel-inner">
      <div class="carousel-item active">
        <img src="https://github.com/rajaselvam2003/intuition9/blob/main/g1.JPG?raw=true" alt="Chicago" class="d-block" style="width:100%">
      </div>
      <div class="carousel-item">
        <img src="https://github.com/rajaselvam2003/intuition9/blob/main/g2.JPG?raw=true" alt="Chicago" class="d-block" style="width:100%">
      </div>
      <div class="carousel-item">
        <img src="https://github.com/rajaselvam2003/intuition9/blob/main/g3.JPG?raw=true" alt="New York" class="d-block" style="width:100%">
      </div>
          <div class="carousel-item">
        <img src="https://github.com/rajaselvam2003/intuition9/blob/main/g4.JPG?raw=true" alt="New York" class="d-block" style="width:100%">
      </div>
          <div class="carousel-item">
        <img src="https://github.com/rajaselvam2003/intuition9/blob/main/g5.JPG?raw=true" alt="New York" class="d-block" style="width:100%">
      </div>
    </div>
  
      <button class="carousel-control-prev" type="button" data-bs-target="#demo" data-bs-slide="prev">
      <span class="carousel-control-prev-icon"></span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#demo" data-bs-slide="next">
      <span class="carousel-control-next-icon"></span>
    </button>
    </div>
     -->
    """
    , height=500, )

PATH = os.path.dirname(os.path.abspath(__file__))
PRESENTATION_FOLDER = os.path.join(PATH, "Presentation")
IMAGES_FOLDER = os.path.join(PATH, "Images")

# Create Presentation Folder if it doesn't exist
if not os.path.exists(PRESENTATION_FOLDER):
    os.makedirs(PRESENTATION_FOLDER)
# Create images folder if it doesn't exist
if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)
    
# Get the Presentation Slides from Streamlit Website,
if uploaded_file is not None:

    # First delete previously uploaded files from Presentation Folder
    

    for file_name in os.listdir(PRESENTATION_FOLDER):
        file_path = os.path.join(PRESENTATION_FOLDER, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"Deleted {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

    # Then upload fresh file to folder
    file_name = uploaded_file.name
    print(f'file_name ----------------------------------------------------:{file_name}')
    file_path = os.path.join(PRESENTATION_FOLDER, uploaded_file.name)
    print(file_path,'thjis doiqwdauiNSfij')
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File saved successfully.")

    # Get name of file
    folder_path = PRESENTATION_FOLDER
    file_names = os.listdir(folder_path)
    
    PDF_Name = file_names[0]

    #find the path of that file to convert
    PDF_path = os.path.join(PRESENTATION_FOLDER , PDF_Name)
    images = convert_from_path(PDF_path)
    Present_Images_Folder  = IMAGES_FOLDER
    # Save each PNG image with a numbered filename
    for i, image in enumerate(images):
        image.save(os.path.join(Present_Images_Folder, f'{i+1}.png'))

    # Parameters
    width, height = 1280, 720
    gestureThreshold = 300
    folderPath = IMAGES_FOLDER

    # Camera Setup
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)



    # Hand Detector
    detectorHand = HandDetector(detectionCon=0.7, maxHands=1)

    # Variables
    imgList = []
    delay = 12
    buttonPressed = False
    counter = 0
    drawMode = False
    imgNumber = 0
    delayCounter = 0
    #2 delays - 1 for slide change, 1 for updating
    SlideDelay = 12
    DrawDelay = 16
    annotations = [[]]
    annotationNumber = -1
    annotationStart = False
    hs, ws = int(120 * 2), int(213 * 1.75)  # width and height of small image

    #Dev Mode:  if Test = true, skip all image pro



    # Get list of presentation images
    pathImages = sorted(os.listdir(folderPath), key=len)
    print(pathImages)

    if len(os.listdir(Present_Images_Folder)) == 0:
        print(f"The folder '{folder_path}' is empty")

    else:

        # Loop through all PNG images in the folder
        folderPath = IMAGES_FOLDER
        for filename in os.listdir(folder_path):
            if filename.endswith('.png'):
                # Open the image and resize it
                image_path = os.path.join(folder_path, filename)
                image = Image.open(image_path)
                resized_image = image.resize((width, height))


                resized_image_path = os.path.join(folder_path, 'resized_' + filename)
                resized_image.save(resized_image_path)

        while True:
            # Get image frame

            success, img = cap.read()
            img = cv2.flip(img, 1)
            pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
            imgCurrent = cv2.imread(pathFullImage)

            # Find the hand and its landmarks
            hands, img = detectorHand.findHands(img)  # with draw
            # Draw Gesture Threshold line
            cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

            if hands and buttonPressed is False:  # If hand is detected

                hand = hands[0]
                cx, cy = hand["center"]
                lmList = hand["lmList"]  # List of 21 Landmark points
                fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

                # Constrain values for easier drawing
                xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width + 500]))
                yVal = int(np.interp(lmList[8][1], [100, height - 100], [0, height + 500]))
                indexFinger = xVal, yVal

                if cy <= gestureThreshold:  # If hand is at the height of the face
                    if fingers == [1, 0, 0, 0, 0]:
                        print("Left")
                        buttonPressed = True
                        if imgNumber > 0:
                            imgNumber -= 1
                            annotations = [[]]
                            annotationNumber = -1
                            annotationStart = False
                    if fingers == [0, 0, 0, 0, 1]:
                        print("Right")
                        buttonPressed = True
                        if imgNumber < len(pathImages) - 1:
                            imgNumber += 1
                            annotations = [[]]
                            annotationNumber = -1
                            annotationStart = False

                if fingers == [0, 1, 1, 0, 0]:
                    cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

                if fingers == [0, 1, 0, 0, 0]:
                    if annotationStart is False:
                        annotationStart = True
                        annotationNumber += 1
                        annotations.append([])
                    print(annotationNumber)
                    annotations[annotationNumber].append(indexFinger)
                    cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

                else:
                    annotationStart = False

                if fingers == [0, 1, 1, 1, 0]:
                    if annotations:
                        annotations.pop(-1)
                        annotationNumber -= 1
                        buttonPressed = True

            else:
                annotationStart = False

            if buttonPressed:
                counter += 1
                if counter > delay:
                    counter = 0
                    buttonPressed = False

            for i, annotation in enumerate(annotations):
                for j in range(len(annotation)):
                    if j != 0:
                        cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

            imgSmall = cv2.resize(img, (ws, hs))
            h, w, _ = imgCurrent.shape
            imgCurrent[0:hs, w - ws: w] = imgSmall

            # Slides sizing
            imgCurrent = cv2.resize(imgCurrent, (1280, 720))

            cv2.imshow("Slides", imgCurrent)
            cv2.imshow("Image", img)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
