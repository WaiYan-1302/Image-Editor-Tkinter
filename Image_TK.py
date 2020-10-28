import cv2
from tkinter import *
import PIL.Image , PIL.ImageTk

root = Tk()
root.title("CV and Tkinter")
root.geometry('900x700')
cv_img = cv2.cvtColor(cv2.imread("Moom2.jpeg") , cv2.COLOR_BGR2RGB)

blur = cv2.bilateralFilter(cv_img,8,75,75)




#cv_img = cv2.cvtColor(root , cv2.COLOR_BGR2RGB)



height , width , channel = cv_img.shape

canvas = Canvas(root , width = width , height = height)

canvas.place(x = 10 , y = 10)


image_gray = cv2.cvtColor(cv_img , cv2.COLOR_RGB2GRAY)
image_gray =  PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(image_gray))

photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))

canvas.create_image(0 , 0 , image = photo , anchor = NW)

blur = cv2.bilateralFilter(cv_img,10,75,75)
photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(blur))

def cartoonize(rgb_image, *,num_pyr_downs=2, num_bilaterals=7):
 # STEP 1 -- Apply a bilateral filter to reduce the color palette of
 # the image.
	downsampled_img = rgb_image
	for _ in range(num_pyr_downs):
		 downsampled_img = cv2.pyrDown(downsampled_img)
	for _ in range(num_bilaterals):
		filterd_small_img = cv2.bilateralFilter(downsampled_img, 9, 9, 7)
	filtered_normal_img = filterd_small_img
	for _ in range(num_pyr_downs):
		filtered_normal_img = cv2.pyrUp(filtered_normal_img)
		 # make sure resulting image has the same dims as original
	if filtered_normal_img.shape != rgb_image.shape:
		filtered_normal_img = cv2.resize(filtered_normal_img, rgb_image.shape[:2])
	# STEP 2 -- Convert the original color image into grayscale.
	img_gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
	# STEP 3 -- Apply amedian blur to reduce image noise.
	img_blur = cv2.medianBlur(img_gray, 5)
 # STEP 4 -- Use adaptive thresholding to detect and emphasize the edges
 # in an edge mask.
	gray_edges = cv2.adaptiveThreshold(img_blur, 234,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 5, 7)
 # STEP 5 -- Combine the color image from step 1 with the edge mask
 # from step 4.
	rgb_edges = cv2.cvtColor(gray_edges, cv2.COLOR_GRAY2RGB)
	return cv2.bitwise_and(filtered_normal_img, rgb_edges)


cartoonized = cartoonize(cv_img , num_pyr_downs= 1 , num_bilaterals = 7)
cartoonized = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cartoonized))



#canvas.create_image(0 , 0 , image = photo , anchor = NW)

def pencil_sketch_on_canvas(image , canvas = None):

	gray_image = cv2.cvtColor(image , cv2.COLOR_RGB2GRAY)
	blurred_image = cv2.GaussianBlur(gray_image , (21, 21), 0, 0)
	gray_sketch = cv2.divide(gray_image , blurred_image , scale = 240)
	if canvas is not None:
		gray_sketch = cv2.multiply(gray_sketch , canvas , scale= 1/ 256)

	return cv2.cvtColor(gray_sketch , cv2.COLOR_GRAY2RGB)

sketch_img = pencil_sketch_on_canvas(cv_img , canvas = None)
sketch_img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(sketch_img))

org_img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))

def Reset():

	canvas.create_image(0 ,0 , image = org_img , anchor = NW)

def Smooth():


	canvas.create_image(0 , 0 , image = photo1 , anchor = NW)

def Click_Cartoon():

	canvas.create_image(0,0 , image = cartoonized , anchor = NW)

def Click_Sketch():

	canvas.create_image(0,0 , image = sketch_img , anchor = NW)

def Click_BnW():

	canvas.create_image(0 , 0 , image = image_gray , anchor = NW)

reset_ico = cv2.imread("reset.png")
reset_ico = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(reset_ico))

sketch_ico = cv2.imread("sketch.png")
sketch_ico = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(sketch_ico))

smooth_ico = cv2.imread('smooth.png')
smooth_ico = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(smooth_ico))

BnW_ico = cv2.imread('blackandwhite.png')
BnW_ico = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(BnW_ico))

cartoon_ico = cv2.imread('cartoonize.png')
cartoon_ico = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cartoon_ico))





Smooth_Btn = Button(root, image = smooth_ico , command = Smooth)
Smooth_Btn.config(text = "Smooth")
Smooth_Btn.place(x = 20 , y= 600)

Cartoon_Btn = Button(root , image = cartoon_ico , command = Click_Cartoon)
Cartoon_Btn.place(x = 180 , y= 600)

Sketch_Btn = Button(root , image = sketch_ico , command = Click_Sketch)
Sketch_Btn.place(x = 340 , y = 600 )

BnW_Btn = Button(root , image = BnW_ico , command = Click_BnW)
BnW_Btn.place(x = 500 , y= 600)

Reset_Btn = Button(root , image = reset_ico , command = Reset)
Reset_Btn.place(x = 680 , y = 600)

root.mainloop()


cv2.destroyAllWindows()