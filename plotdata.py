import shelve
import matplotlib as mplot
mplot.use('PDF')
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import sys
import time
import pickle as pl
from setting.py import *
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
    minpkl = open(min_fame,'rb')
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
    bin_cnt = bin_count(bin_size)
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
    bin_cnt = bin_count(bin_size)
    x = np.array(range(int(bin_cnt)+1))
    random_params = pu.plotFigParams('Time bin %s hours'%bin_size, 'activity freqeuncy', 
                                     'Flickr twiter frequency scatter',xscale='log',yscale='log')
    pfig = pu.plotFigFunc()
    subplot = pfig.plot_scatter(params, np.array(x), np.array(fl_cnt_array))
    pfig.plot_scatter(params, np.array(x), np.array(tw_cnt_array), ax=subplot)
    pfig.save_fig("%s/scatter_freq"%(fig_path))
    

def plot_coeff_random(coeff_type,bin_size):
    if coeff_type == "jaccard": 
        shelf_name = "%s/jaccard_random_%s.dat"%(coeff_path,bin_size)
    else:
        shelf_name = "%s/cos_random_%s.dat"%(coeff_path,bin_size)
    fsave = shelf_name.rsplit("/",1)[1].rsplit(".",1)[0]
    shelf = shelve.open(shelf_name)
    random_params = pu.plotFigParams("User Names", "%s similarity {%s hour bins}" % (fsave,bin_size),
                                     "%s similarity of every user {%s hour bins}" % (fsave,bin_size))
    pfig = pu.plotFigFunc()
    pfig1 = pu.plotFigFunc()
    users = shelf.keys()
    coeff = np.array(shelf.values())
    ax.scatter(range(len(users)),coeff)
    ax.axhline(y=np.mean(coeff),color='r')
    #ax.legend(("mean"))
    ax.set_xlabel("Users names")
    ax.set_ylabel("%s similarity {%s hour bins}" % (fsave,bin_size))
    ax.set_title("%s similarity of every user {%s hour bins}" % (fsave,bin_size))
    ax.set_xticklabels(users,rotation='vertical')
    fig.savefig("%s/%s.pdf"%(fig_path,fsave))
    fig1.savefig("%s/%s_hist.pdf"%(fig_path,fsave))
    shelf.close()


def plot_coeff(coeff_type,with_bin,bin_size):
    if with_bin:
        shelf_name = "%s/jaccard_bin_%s.dat"%(coeff_path,bin_size) if coeff_type == "jaccard" else "%s/cosine_bin_%s.dat"%(coeff_path,bin_size)
    else:
        shelf_name = "%s/jaccard_%s.dat"%(coeff_path,bin_size) if coeff_type == "jaccard" else "%s/cos_%s.dat"%(coeff_path,bin_size)
    fsave = shelf_name.rsplit("/",1)[1].rsplit(".",1)[0]
    print shelf_name
    shelf = shelve.open(shelf_name)
    
    fig1 = plt.figure()
    
    ax1 = fig1.add_subplot(111)
    users = shelf.keys()
    coeff = np.array(shelf.values())
    ax.scatter(range(len(users)),coeff)
    ax.axhline(y=np.mean(coeff),color='r')
    #ax.legend(("mean"))
    ax.set_xlabel("Users names")
    ax.set_ylabel("%s similarity {%s hour bins}" % (fsave,bin_size))
    ax.set_title("%s similarity of every user {%s hour bins}" % (fsave,bin_size))
    ax.set_xticklabels(users,rotation='vertical')
    fig.savefig("%s/%s.pdf"%(fig_path,fsave))
    ax1.hist(coeff,np.unique(coeff),color='b',cumulative=-1)
    ax1.set_yscale('log')
    ax1.set_xlabel("%s similarity"%(fsave))
    ax1.set_ylabel("#users with %s similarity {%s hr bins}" % (fsave,bin_size))
    ax1.set_title("histogram of %s similarity {%s hour bins}" % (fsave,bin_size))
    fig1.savefig("%s/%s_hist.pdf"%(fig_path,fsave))
    shelf.close()

def plotdata_ftjaccard(bin_size):
    plot_coeff('jaccard',True,bin_size)
    plot_coeff('jaccard',False,bin_size)
    plot_coeff_random('jaccard',bin_size)

def plotdata_ftcosine(bin_size):
    plot_coeff('cosine',True,bin_size)
    plot_coeff('cosine',False,bin_size)
    plot_coeff_random('cosine',bin_size)

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
