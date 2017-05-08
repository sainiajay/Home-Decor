## Introduction

This is a prototype for demonstrating idea about applying virtual reality for Home Decor, just like virtual mirror for decorating homes. We could visualize our home (room or hall basically) with objects like furniture, paintings etc using this application. This visualization is done via 360 images of room, which can be viewed in any VR headset or desktop.

## Implementation
We have used image processing (OpenCV) heavily for working 360 photospheres of room and imageset of object. The imageset comprises of images of object from  various discrete angles. In this implementation we have hardcoded the image of room and the object.

## Installation

You will need python 2.7 on your system for project. Follow the following steps to install other dependencies.
* Install OpenCV 2 for python.

    ```sudo apt-get install python-opencv```

* Install Tkinter for python.

    ```sudo apt-get install python-tk```

* Install glut for python.

    ```sudo apt-get install freeglut3 freeglut3-dev```

* Install python dependencies.

    ```sudo pip install -r requirements.txt```
