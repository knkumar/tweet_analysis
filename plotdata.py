import shelve
import numpy as np
import sys
import time
import pickle as pl
from settings import *
import plotUtils as pu

fin = fshelf
tin = tshelf
coeff_path = "./shelf"


"""
    @input
    bin_size - define the bin size for the calculation
    MaxPkl - The pickle file containing the max time bin
    MinPkl - The pickle file containing the min time bin
    @output:
    bins - returns the total number of bins based on the bin_size specified

"""
def bin_count(bin_size, max_fname, min_fname):
    maxpkl = open(max_fname,'rb')
    minpkl = open(min_fname,'rb')
    fmin = pl.load(minpkl)
    fmax = pl.load(maxpkl)
    import math
    bins = math.floor((time.mktime(fmax.timetuple()) - time.mktime(fmin.timetuple()))/(float(bin_size)*60*60))
    maxpkl.close()
    minpkl.close()
    return bins


"""
    @input:
    bin_size - define the bin size for the calculation
    fldict - flickr shelf input
    twitdict - twitter shelf input
    @output:
    fl_cnt_array - the number of entries per bin in the flickr dataset
    tw_cnt_array - the number of etries per bin in the twitter dataset
    @calls:
    bin_count
"""
def get_counts(bin_size):
    fldict = shelve.open("%s_%s"%(flickr_inp,bin_size))
    twitdict = shelve.open("%s_%s"%(twitter_inp,bin_size))
    flkeys = fldict.keys()
    twkeys = twitdict.keys()
    print "number of flickr users : %s" % len(flkeys)
    print "number of twitter users : %s" % len(twkeys)
    bin_cnt = bin_count(bin_size,maxtwit,mintwit)
    fl_cnt_array = np.zeros(int(bin_cnt)+1)
    tw_cnt_array = np.zeros(int(bin_cnt)+1)
    unames = set(flkeys)&set(twkeys)
    for name in unames:
        for bin in fldict[name].keys():
            fl_cnt_array[int(bin)] += fldict[name][bin][0]
    for name in unames:
        for bin in twitdict[name].keys():
            tw_cnt_array[int(bin)] += twitdict[name][bin][0]
    fldict.close()
    twitdict.close()
    return fl_cnt_array, tw_cnt_array

    

def plot_coeff_random(coeff_type,bin_size):
    if coeff_type == "jaccard": 
        shelf_name = "%s/jaccard_random_%s.dat"%(coeff_path,bin_size)
    else:
        shelf_name = "%s/cos_random_%s.dat"%(coeff_path,bin_size)
    fsave = shelf_name.rsplit("/",1)[1].rsplit(".",1)[0]
    shelf = shelve.open(shelf_name)
    users = shelf.keys()
    coeff = np.array(shelf.values())
    random_params = pu.plotFigParams("User Names", "%s similarity {%s hour bins}" % (fsave,bin_size),
                                     "%s similarity of every user {%s hour bins}" % (fsave,bin_size),
                                     xticks=users, axhline=np.mean(coeff))
    pfig = pu.plotFigFunc()
    pfig.plot_scatter(params, range(len(users)), coeff)
    pfig.save_fig("%s/%s"%(fig_path,fsave))    
    shelf.close()


def plot_coeff(coeff_type,with_bin,bin_size):
    if with_bin:
        suffix = "_bin.dat"
    else:
        suffix = ".dat"
        
    shelf_name = "%s/jaccard_%s%s"%(coeff_path,bin_size,suffix) if coeff_type == "jaccard" else "%s/cosine_%s.dat"%(coeff_path,bin_size,suffix)
    
    fsave = shelf_name.rsplit("/",1)[1].rsplit(".",1)[0]
    print shelf_name
    shelf = shelve.open(shelf_name)
    users = shelf.keys()
    coeff = np.array(shelf.values())
    scatter_params = pu.plotFigParams("User Names", "%s similarity {%s hour bins}" % (fsave,bin_size),
                                     "%s similarity of every user {%s hour bins}" % (fsave,bin_size),
                                     xticks=users, axhline=np.mean(coeff))
    pfig = pu.plotFigFunc()
    pfig.plot_scatter(scatter_params, range(len(users)), coeff)
    pfig.save_fig("%s/%s.pdf"%(fig_path,fsave))
    hist_params = pu.plotFigParams("User Names", "%s similarity {%s hour bins}" % (fsave,bin_size),
                                   "histogram of %s similarity {%s hour bins}" % (fsave,bin_size),
                                     yscale='log', cumulative=-1)
    pfig1 = pu.plotFigFunc()
    pfig1.plot_hist(hist_params, coeff, np.unique(coeff))
    pfig1.save_fig("%s/%s_hist.pdf"%(fig_path,fsave))
    shelf.close()

def plotdata_ftjaccard(bin_size):
    plot_coeff('jaccard',True,bin_size)
    plot_coeff('jaccard',False,bin_size)
    plot_coeff_random('jaccard',bin_size)

def plotdata_ftcosine(bin_size):
    plot_coeff('cosine',True,bin_size)
    plot_coeff('cosine',False,bin_size)
    plot_coeff_random('cosine',bin_size)


"""
    @input:
    bin_size - define the bin size for the calculation
    fl_cnt_array, tw_cnt_array
    @output:
    PDF figure of scatter plot - 
        x axis: Time Bins
        y axis: Bin counts for flickr and twitter
    
"""
def plotdata_ftscatter(bin_size):
    fl_cnt_array, tw_cnt_array = get_counts(bin_size)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bin_cnt = bin_count(bin_size,maxtwit,mintwit)
    x = np.array(range(int(bin_cnt)+1))
    random_params = pu.plotFigParams('Time bin %s hours'%bin_size, 'activity freqeuncy', 
                                     'Flickr twiter frequency scatter',xscale='log',yscale='log')
    pfig = pu.plotFigFunc()
    subplot = pfig.plot_scatter(params, np.array(x), np.array(fl_cnt_array))
    pfig.plot_scatter(params, np.array(x), np.array(tw_cnt_array), ax=subplot)
    pfig.save_fig("%s/scatter_freq"%(fig_path))



def main():
    bins = ["4","24","48"]
    for bin_size in bins:
        try:
            plotdata_ftscatter(bin_size)
            plotdata_ftjaccard(bin_size)
            plotdata_ftcosine(bin_size)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

if __name__ == "__main__":
    sys.exit(main())
