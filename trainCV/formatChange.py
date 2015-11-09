# Convert to convert file to another format

from PIL import Image
import os

d_ext = ".jpg"

for file in os.listdir('.'):
    name,ext = os.path.splitext(file)
    
    if ext == ".png": #save it as jpeg
        #first checkigng if the jpg version exits or not
        propName = name + d_ext

        if not os.path.isfile(propName):
            try:
                             
                f = open(file,'r')
                data = f.read()

                fnew = open(propName,'w')
                fnew.write(data)
                           
                print "Originally : " + os.path.abspath(file)
                print "Saved as   : " + os.path.abspath(propName)

            except IOError:
                print "cannot save in a different name"                

        else:
            print "Executing : ls on current directory"
            print "Output >> \n"
            for file in os.listdir('.'):
                print file

            
    
