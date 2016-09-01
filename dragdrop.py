import Tkinter as tk
from Tkinter import *
from PIL import Image, ImageTk
import PIL
import cv2
import PhotoSphere

imageFile = "input.jpg"
left  = [0,0]
objPos = [0,0]
image = cv2.imread(imageFile)

class SampleApp(tk.Tk):
    '''Illustrate how to drag items on a Tkinter canvas'''
    #objFile = "img1.jpg"
    objSize = [0,0]
    objectfile="01";
    #obj = cv2.imread('bw\\'+objectfile+'.jpg')

    def printObject(self):
        x = left[0] + objPos[0]
        y = left[1] + objPos[1]
        roi = image[y:y+self.objSize[1],x:x+self.objSize[0]]
        
        # Now create a mask of logo and create its inverse mask also
        img2 = cv2.imread ('png/' + self.objectfile + '.png',-1)
        img2 = cv2.resize(img2,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        r,c,_ = img2.shape

        b1,g1,r1,alpha = cv2.split(img2)
        img2 = cv2.merge((b1,g1,r1))
        _,mask = cv2.threshold(alpha,100,1,cv2.THRESH_BINARY)

        fg_b = cv2.multiply(b1,mask)
        fg_g = cv2.multiply(g1,mask)
        fg_r = cv2.multiply(r1,mask)
        fg = cv2.merge((fg_b,fg_g,fg_r))
        
        b2,g2,r2 = cv2.split(roi)
        bg_b = cv2.multiply(b2,1-mask)
        bg_g = cv2.multiply(g2,1-mask)
        bg_r = cv2.multiply(r2,1-mask)
        bg = cv2.merge((bg_b,bg_g,bg_r))
        
        image[y:y+c, x:x+r] = cv2.add(bg,fg)
        cv2.imwrite ('output.jpg',image)
        PhotoSphere.Main('output.jpg')

    def reloadObject(self):
        image = Image.open("png/"+ self.objectfile +".png")
        basewidth = 300
        wpercent = (basewidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        self.objSize = [basewidth,hsize]
        print(self.objSize)
        self.photos = ImageTk.PhotoImage(image)
        self.canvas.create_image(objPos[0] + image.size[0]/2,objPos[1] + image.size[1]/2, image=self.photos, tags="token2")

    def moveUp(self):
        a = self.objectfile[0]
        if a > '0':
            self.objectfile = (chr(ord(a) - 1) + self.objectfile[1])
        #reload image on canvas
        self.reloadObject()

    def moveDown(self):
        a = self.objectfile[0]
        if a < '2':
            self.objectfile = (chr(ord(a) + 1) + self.objectfile[1])
        #reload image on canvas
        self.reloadObject()
    
    def moveLeft(self):
        a = self.objectfile[1]
        if a < '8':
            self.objectfile = (self.objectfile[0] + chr(ord(a) + 1))
        #reload image on canvas
        self.reloadObject()

    def moveRight(self):
        a = self.objectfile[1]
        if a > '1':
            self.objectfile = (self.objectfile[0] + chr(ord(a) - 1))
        #reload image on canvas
        self.reloadObject()
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #self.attributes('-fullscreen', True)
        self.diff = 0
        
        # create a canvas
        self.canvas = tk.Canvas()
        self.canvas.pack(fill="both", expand=True)
        win = tk.Tk()
        self.printButton = Button(win,text='Print',command = self.printObject)
        self.leftButton = Button(win,text='Left',command = self.moveLeft)
        self.rightButton = Button(win,text='Right',command = self.moveRight)
        self.upButton = Button(win,text='Up',command = self.moveUp)
        self.downButton = Button(win,text='Down',command = self.moveDown)
        self.printButton.pack()
        self.leftButton.pack()
        self.rightButton.pack()
        self.upButton.pack()
        self.downButton.pack()
        
        # this data is used to keep track of an 
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # create a couple movable objects
        self._create_token( "white")
        # self._create_token((200, 100), "black")

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token1", "<ButtonPress-1>", self.OnTokenButtonPress)
        self.canvas.tag_bind("token1", "<ButtonRelease-1>", self.OnTokenButtonRelease)
        self.canvas.tag_bind("token1", "<B1-Motion>", self.OnTokenMotion1)

        self.canvas.tag_bind("token2", "<ButtonPress-1>", self.OnTokenButtonPress)
        self.canvas.tag_bind("token2", "<ButtonRelease-1>", self.OnTokenButtonRelease)
        self.canvas.tag_bind("token2", "<B1-Motion>", self.OnTokenMotion2)


    def _create_token(self, color):
        '''Create a token at the given coordinate in the given color'''
        
        image = Image.open(imageFile)
        self.x_factor = image.size[0] - self.canvas.winfo_screenwidth()
        self.y_factor = image.size[1] - self.canvas.winfo_screenheight()
        
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(image.size[0]/2,image.size[1]/2, image=self.photo, tags="token1")
        
        image = Image.open("png/01.png")
        basewidth = 300
        wpercent = (basewidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        self.objSize = [basewidth,hsize]
        self.photos = ImageTk.PhotoImage(image)
        self.canvas.create_image(image.size[0]/2,image.size[1]/2, image=self.photos, tags="token2")

        '''self.canvas.create_oval(x-25, y-25, x+25, y+25, 
                                outline=color, fill=color, tags="token")
        '''
        
    def OnTokenButtonPress(self, event):
        '''Being drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def OnTokenButtonRelease(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def OnTokenMotion1(self, event):
        '''Handle dragging of an object'''
        # compute how much this object has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]

        x_diff = left[0] - delta_x
        y_diff = left[1] - delta_y

        if x_diff < 0 or x_diff  > self.x_factor:
            delta_x = 0
        else:
            left[0] = x_diff

        if y_diff < 0 or y_diff > self.y_factor:
            delta_y = 0
        else:
            left[1] = y_diff

        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        x = left[0] + objPos[0]
        y = left[1] + objPos[1]
        #print(x,y)

    def OnTokenMotion2(self, event):
        '''Handle dragging of an object'''
        # compute how much this object has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]

        objPos[0] += delta_x
        objPos[1] += delta_y

        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        x = left[0] + objPos[0]
        y = left[1] + objPos[1]

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
