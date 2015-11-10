import os

#Get jpg images in  pwd
def get_imlist(path):
    return [os.path.abspath(f) for f in os.listdir(path) if f.endswith('*.jpg')]

#get the size of an image
def imresize(im,sz):
    pil_im = Image.fromarray(uint8(im))
    return array(pil_im.resize(sz))

#compute image average
def compute_average(imlist):
    """ Computes the averga of a list of images """

    #open first image and make into an array of type float
    averageim = array(Image.open(imlist[0]),'f')

    for imname in imlist[1:]:
        try:
            averageim +=  array(Image.open(imname))
        except:
            print imname + "...skipped"

        averageim = averageim/len(imlist)
return array(averageim,'uint8')
    
    

