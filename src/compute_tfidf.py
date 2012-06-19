import shelve
import numpy as np
import sys
import time
import pickle as pl
import math
from settings import *


class c_tfidf:

    def __init__(self):
        self.fldict = shelve.open("%s_%s"%(flickr_inp,bin_size))
        self.twitdict = shelve.open("%s_%s"%(twitter_inp,bin_size))
        self.fl_ubins = shelve.open("%s_%s.dat"%(flickr_out,bin_size))
        self.tw_ubins = shelve.open("%s_%s.dat"%(twitter_out,bin_size))

    def __del__(self):
        self.fldict.close()
        self.twitdict.close()
        self.fl_ubins.close()
        self.tw_ubins.close()



def form_tuples(bin_size):
    fldict = shelve.open("%s_%s"%(flickr_inp,bin_size))
    twitdict = shelve.open("%s_%s"%(twitter_inp,bin_size))
    funames = fldict.keys()
    tunames = twitdict.keys()
    unames = set(funames)&set(tunames)
    fl_ubins = shelve.open("%s_%s"%(flickr_out,bin_size))
    tw_ubins = shelve.open("%s_%s"%(twitter_out,bin_size))
    def make_shelf(shelf,name,bin,tags):
        if shelf=='f':
            if name in fl_ubins.keys():
                fl_ubins[name][bin] = tags
            else:
                fl_ubins[name] = {bin : tags}
        else:
            if name in fl_ubins.keys():
                tw_ubins[name][bin] = tags
            else:
                tw_ubins[name] = {bin :tags}
    map(lambda name: map(lambda bin: make_shelf('f',name,bin,fldict[name][bin][2]),   fldict[name].keys()   ), unames)
    map(lambda name: map(lambda bin: make_shelf('t',name,bin,twitdict[name][bin][2]), twitdict[name].keys() ), unames)
    fldict.close()
    twitdict.close()
    return fl_ubins,tw_ubins
 
def main():
    bins = ["4"]
    for bin_size in bins:
        try:
            fl_ubins,tw_ubins = form_tuples(bin_size)
            print fl_ubins, tw_ubins
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

if __name__ == "__main__":
    sys.exit(main())

