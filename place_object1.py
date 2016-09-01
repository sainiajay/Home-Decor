import cv2
img1 = cv2.imread('xyz.jpg')
img2 = cv2.imread('bw\\05.jpg')
x1 = img1.shape[0]//2
y1 = img1.shape[1]//2
# I want to put logo on top-left corner, So I create a ROI
rows,cols,channels = img2.shape
print (img1.shape)
img2 = cv2.resize(img2,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
r,c,ch = img2.shape
roi = img1[x1:x1+r, y1:y1+c]

# Now create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

cv2.imwrite('mask2.jpg',mask)
cv2.imwrite('mask_inv2.jpg',mask_inv)

# Now black-out the area of logo in ROI
img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

# Take only region of logo from logo image.
img2_fg = cv2.bitwise_and(img2,img2,mask = mask)

cv2.imwrite('bg2.jpg',img1_bg)
cv2.imwrite('fg2.jpg',img2_fg)

# Put logo in ROI and modify the main image
dst = cv2.add(img1_bg,img2_fg)
cv2.imwrite ("dst.jpg",dst)
img1[x1:x1+r, y1:y1+c] = dst

