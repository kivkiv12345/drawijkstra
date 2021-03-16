from PIL import Image

imgpath = 'images/circlesmall.gif'

img_width, img_height = Image.open(imgpath).size
img_width /= 2
img_height /= 2