# Import modules
import cv2
import pandas as pd

# Open camera
cam = cv2.VideoCapture(0)
cv2.namedWindow("Capture")
img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Capture", frame)

    k = cv2.waitKey(1)
    if k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        print("Escape hit, closing...")
        break

cam.release()

cv2.destroyAllWindows()

# Load Image and dataset
img=cv2.imread(img_name)
#img=cv2.imread("colorpic.png")  #default image to test with.
index = ["color", "color_name", "hex", "R", "G", "B"]
df=pd.read_csv("D:/Color-Detection dataset/colors.csv", names=index, header=None)

# Declaring global variables
clicked=False
r=g=b=x_pos=y_pos=0

# Function to get the color name
def get_colorName(R,G,B):
    min=10000
    for i in range(len(df)):
        dist = abs(R-int(df.loc[i,"R"])) + abs(G - int(df.loc[i,"G"])) + abs(B - int(df.loc[i,"B"]))
        if(dist<min):
            min = dist
            colorName = df.loc[i,'color_name']
    return colorName

# Function to define x,y coordinates
def draw(event, x, y, flags, param):
    if(event==cv2.EVENT_LBUTTONDBLCLK):
        global b,g,r,x_pos,y_pos,clicked
        clicked=True
        x_pos=x
        y_pos=y
        (b, g, r) = img[y, x]
        b=int(b)
        g=int(g)
        r=int(r)

# Opens the image that has been captured
cv2.namedWindow("Image")
cv2.setMouseCallback("Image",draw)
while True:
    cv2.imshow("Image",img)
    if clicked:
        cv2.rectangle(img , (20,20), (750,60), (b, g, r), -1)
        text = get_colorName(r,g,b)+" R= "+str(r)+" G= "+str(g)+" B= "+str(b)
        cv2.putText(img, text, (50,50), 2, 0.8, (255,255,255), 2, cv2.LINE_AA)
        if(r+g+b >= 600):
            cv2.putText(img, text, (50,50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)
        clicked=False
    if(cv2.waitKey(20) & 0xFF == 27):
        break
cv2.destroyAllWindows()