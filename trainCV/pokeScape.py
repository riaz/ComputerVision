import BeautifulSoup
import urllib
import os

try:
    fd = urllib.urlopen("http://pokemondb.net/pokedex/national#gen-1")
except IOError:
    print "Erro: Reading url"
    exit(0)
doc = fd.read()

dom = BeautifulSoup.BeautifulSoup(doc)
elm = dom.find("div", {"class": "infocard-tall-list" })
spans = elm.findAll("span")

if os.path.isfile("pokedex.idx"):
    fd = open("pokedex.idx","a")
    for span in spans:
        fd.write(str(span))
        
    fd.close()    
    print "Pokedex was created successfully"
    exit(0)
print "Pokedex is the latest already"
