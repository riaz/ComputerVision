import os

#Get jpg images in  pwd
def get_imlist(path):
    return [os.path.abspath(f) for f in os.listdir(path) if f.endswith('*.jpg')]

#get the size of an image
def imresize(im,sz):
    pil_im = Image.fromarray(uint8(im))
    return array(pil_im.resize(sz))

