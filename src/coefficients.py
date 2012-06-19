import shelve
import numpy as np
import sys
import time
import pickle as pl
import math
from settings import *


class coeff:

    def __init__(self,bin_size):
        self.fldict = shelve.open("%s_%s"%(flickr_inp,bin_size))
        self.twitdict = shelve.open("%s_%s"%(twitter_inp,bin_size))
        self.fl_ubins = shelve.open("%s_%s.dat"%(fupbin,bin_size))
        self.tw_ubins = shelve.open("%s_%s.dat"%(tupbin,bin_size))
    
    def __del__(self):
        self.fldict.close()
        self.twitdict.close()
        self.fl_ubins.close()
        self.tw_ubins.close()
    
    def jaccard(self, a, b):
        anb = reduce(lambda x,y:x+y, map(lambda x,y: min(x,y), a,b))
        aub = reduce(lambda x,y:x+y, map(lambda x,y: max(x,y), a,b))
        jaccard = float(anb)/aub
        return jaccard

    def cosine(self, a, b):
        adotb = reduce(lambda x,y:x+y, map(lambda x,y: x*y, a,b))
        a_mag = math.sqrt(reduce(lambda x,y:x+y, map(lambda x: x*x, a)))
        b_mag = math.sqrt(reduce(lambda x,y:x+y, map(lambda x: x*x, b)))
        cosine = adotb/(a_mag*b_mag)
        return cosine

    def form_tuples(self, bin_size):
        
        funames = self.fldict.keys()
        tunames = self.twitdict.keys()
        unames = set(funames)&set(tunames)
        self.fl_ubins = shelve.open("%s_%s.dat"%(flickr_out,bin_size))
        self.tw_ubins = shelve.open("%s_%s.dat"%(twitter_out,bin_size))

        def insert_shelf(shelf,key, value):
            freq = map(lambda x:  (x,self.fldict[key][x][0] if shelf=='f' else self.twitdict[key][x][0]), value)
            if len(value) > 5 and max(freq) > 5:
                if shelf=='f':
                    self.fl_ubins[key]=freq
                else:
                    self.tw_ubins[key]=freq

        map(lambda x: insert_shelf('f',x,self.fldict[x].keys()), unames)
        map(lambda x: insert_shelf('t',x,self.twitdict[x].keys()), unames)
        self.fl_ubins.close()
        self.tw_ubins.close()


    def correlate_random(self, cf_type,bin_size, binary=False):
        c_shelf_name = "%s_%s"%((jc_rand_out if cf_type=='jaccard' else cos_rand_out),bin_size)
        c_shelf = shelve.open(c_shelf_name + ("binary.dat" if binary else ".dat"))
        conf_shelf_name = "%s_"%jc_out if cf_type == "jaccard" else "%s_"%cos_out+'%s'%bin_size
        confusion = shelve.open(conf_shelf_name + ("bin_conf1.dat" if binary else "conf1.dat"))
        #nbins = nbin()
     
        for fkey in self.fl_ubins.keys(): #flickr user names
            fbins,fbincounts = zip(*self.fl_ubins[fkey])

            for tkey in self.tw_ubins.keys():
                tbins,tbincounts = zip(*self.tw_ubins[tkey])
                nbins = set(fbins)|set(tbins)

                if binary:
                    fmap = map(lambda x: 1 if x in fbins else 0, nbins)
                    tmap = map(lambda x: 1 if x in tbins else 0, nbins)
                else:    
                    fmap = map(lambda x: fbincounts[fbins.index(x)] if x in fbins else 0, nbins)
                    tmap = map(lambda x: tbincounts[tbins.index(x)] if x in tbins else 0, nbins)

            c_index = jaccard(fmap,tmap) if cf_type=='jaccard' else cosine(fmap,tmap)
            c_shelf["%s|%s"%(fkey,tkey)] = c_index
     
        self.compute_confusion(c_shelf, confusion)
        c_shelf.close()
        confusion.close()
    
    def compute_confusion(self, c_shelf, confusion):

        true_p = []
        false_p = []
        true_n = []
        false_n = []
        for tau in 0.001*np.array(range(1,1000)):
            tp=0
            fp=0
            fn=0
            tn=0
            for key in c_shelf.keys():
                c_index = c_shelf[key]
                fname,tname = key.split('|')
                if c_index >= tau:
                    if fname == tname: tp = tp+1
                    else: fp = fp+1

                if c_index < tau:
                    if fname != tname: tn = tn+1 
                    else: fn = fn+1                        
            true_p.append(tp)            
            false_p.append(fp)
            true_n.append(tn)
            false_n.append(fn)
    
        confusion["tp"] = true_p
        confusion["fp"] = false_p
        confusion["tn"] = true_n
        confusion["fn"] = false_n

    """
    Input:
    correlation_type (cf_type) = jaccard | cosine, bin_size
    Action:
    For every user
    . compute bincouts
    . form vector maps only for bins in either flickr or twitter, vector contains bincounts
    . compute the jaccard or cosine similarity for each user
    
    """
    def correlate(self, cf_type, bin_size):
        c_shelf = shelve.open("%s_%s.dat"%((jc_out if cf_type=='jaccard' else cos_out),bin_size))
        #nbins = nbin()
        for key in self.fl_ubins.keys(): #flickr user names
            if key in self.tw_ubins:
                fbins,fbincounts = zip(*self.fl_ubins[key])
                tbins,tbincounts = zip(*self.tw_ubins[key])
                nbins = set(fbins)|set(tbins)
                fmap = map(lambda x: fbincounts[fbins.index(x)] if x in fbins else 0, nbins)
                tmap = map(lambda x: tbincounts[tbins.index(x)] if x in tbins else 0, nbins)
                c_index = jaccard(fmap,tmap) if cf_type=='jaccard' else cosine(fmap,tmap)
                c_shelf[key] = c_index
        c_shelf.close()
    
    def correlate_with_bins(self, cf_type,bin_size):
        c_shelf = shelve.open("%s_%s.dat"%((jc_bin_out if cf_type=='jaccard' else cos_bin_out),bin_size))
        #nbins = nbin()
        for key in self.fl_ubins.keys(): #flickr user names
            fbins,fbincounts = zip(*self.fl_ubins[key])
            if key in self.tw_ubins:
                tbins,tbincounts = zip(*self.tw_ubins[key])
            else: continue
            nbins = set(fbins)|set(tbins)
            fmap = map(lambda x: 1 if x in fbins else 0, nbins)
            tmap = map(lambda x: 1 if x in tbins else 0, nbins)
            c_index = jaccard(fmap,tmap) if cf_type=='jaccard' else cosine(fmap,tmap)
            c_shelf[key] = c_index
        c_shelf.close()
    

    def correlate_jaccard(self, bin_size):
        self.correlate('jaccard',bin_size)
        self.correlate_with_bins('jaccard',bin_size)
        self.correlate_random('jaccard',bin_size)
        self.correlate_random('jaccard',bin_size,binary=True)
        
    def correlate_cosine(self, bin_size):
        self.correlate('cosine',bin_size)
        self.correlate_with_bins('cosine',bin_size)
        self.correlate_random('cosine',bin_size)
        self.correlate_random('cosine',bin_size,binary=True)
    
def main():
    bins = ["4"]
    for bin_size in bins:
        try:
            form_tuples(bin_size)
            correlate_jaccard(bin_size)
            correlate_cosine(bin_size)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

if __name__ == "__main__":
    sys.exit(main())


"""
**random for corerlate**
ukeys = set(self.fl_ubins.keys())&set(self.tw_ubins.keys())
ukeys = list(ukeys)
import random
fkeys = random.sample(ukeys,len(ukeys))
random.seed()
tkeys = random.sample(ukeys,len(ukeys))
print fkeys
print
print tkeys
titer = iter(tkeys)
"""
