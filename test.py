import cv2

img1 = cv2.resize(cv2.imread("./images/bg_1.jpg", cv2.CV_8UC3), (512, 512), interpolation=cv2.INTER_CUBIC)

roi = img1[180:200, 180:200]

tri_img = roi.copy()

roi_logo = cv2.circle(tri_img, (3,3), 2, (10,20,20))

cv2.imshow("SRC", img1)
cv2.imshow("roi", roi)
cv2.imshow("roi_ro", roi_logo)
cv2.waitKey(0)