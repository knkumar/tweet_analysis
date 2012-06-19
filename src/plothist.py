import shelve
import matplotlib as mplot
mplot.use('PDF')
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pylab as P
import sys
import time
import pickle as pl
from setting import *

def bin_count(bin_size):
    maxpkl = open(maxflick,'rb')
    minpkl = open(minflick,'rb')
    fmin = pl.load(minpkl)
    fmax = pl.load(maxpkl)
    import math
    bin = math.floor((time.mktime(fmax.timetuple()) - time.mktime(fmin.timetuple()))/(float(bin_size)*60*60))
    return bin

def plot_userbins(bin_size):
    f = shelve.open("%s_%s.dat"%(fupbin,bin_size))
    t = shelve.open("%s_%s.dat"%(tupbin,bin_size))
    bin_array = []
    bin_key = []
    for uname in f.keys():
        if uname in t:
            fbincount = len(f[uname])
            tbincount = len(t[uname])
            bincount = [fbincount,tbincount]
            bin_array.append(bincount)
            bin_key.append(uname)
        else:
            continue
    bins_plot = np.array(bin_array)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    print bins_plot
    ax.plot(bins_plot[:,0],bins_plot[:,1],'b.')
    #ax.set_xscale('log')
    #ax.set_yscale('log')
    ax.set_xlabel("# of active Flickr bins {%s hr bins}"%(bin_size))
    ax.set_ylabel("# of active twitter bins {%s hr bins}"%(bin_size))
    #ax.set_xticklabels(users,rotation='vertical')
    ax.set_title("Flickr Bins versus Twitter Bins {%s hr bins}"%(bin_size))
    fig.savefig("%s/ft-bins_%s.pdf"%(fig_save,bin_size))
    f.close()
    t.close()

def plot_userfreq(bin_size):
    f = shelve.open("%s_%s.dat"%(fupbin,bin_size))
    t = shelve.open("%s_%s.dat"%(tupbin,bin_size))
    event_array = []
    event_plot = []
    def add(x,y): return x+y
    for uname in f.keys():
        if uname in t:
            feventcount = reduce(add, map(lambda bflist: bflist[1], f[uname]))
            teventcount = reduce(add, map(lambda bflist: bflist[1], t[uname]))
            eventcount = [feventcount,teventcount]
            event_array.append(eventcount)
            event_plot.append(uname)
        else:
            continue
    event_points = np.array(event_array)
    event_plot = np.array(event_plot)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    print event_points[:,0]
    print event_points[:,1]
    ax.plot(event_points[:,0],event_points[:,1],'b.')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("# of Flickr Events {%s hr bins}"%(bin_size))
    ax.set_ylabel("# of Twitter Events {%s hr bins}"%(bin_size))
    ax.set_title("Flickr EVents Vesus Twitter Events {%s hr bins}"%(bin_size))
    #ax.set_xticklabels(users,rotation='vertical')
    fig.savefig("%s/ft-freq_%s.pdf"%(fig_save,bin_size))
    f.close()
    t.close()

def plot_hist_events(bin_size):
    f = shelve.open("%s_%s.dat"%(fupbin,bin_size))
    t = shelve.open("%s_%s.dat"%(tupbin,bin_size))
    fevents = [] # a list of events for every flcikr user per bin
    tevents = [] # a list of events for every twitter user per bin
    def add(x,y): return x+y
    map(lambda uname: fevents.append(reduce(add, map(lambda y: y[1],f[uname])) ), f.keys())
    map(lambda uname: tevents.append(reduce(add, map(lambda y: y[1],t[uname])) ), t.keys())
    fig1 = plt.figure(figsize=(10,14))
    fevents = np.array(fevents)
    tevents = np.array(tevents)
    ax1 = fig1.add_subplot(211)
    ax1.hist(fevents,np.unique(fevents),cumulative=-1)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel("# of flickr events {%s hr bins}"%(bin_size))
    ax1.set_ylabel("# of users {%s hr bins}"%(bin_size))
    ax1.set_title("flickr events frequencies {%s hr bins}"%(bin_size))
    ax2 = fig1.add_subplot(212)
    ax2.hist(tevents,np.unique(tevents),cumulative=-1)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel("# of twitter events {%s hr bins}"%(bin_size))
    ax2.set_ylabel("# of users {%s hr bins}"%(bin_size))
    ax2.set_title("Twitter events frequencies {%s hr bins}"%(bin_size))
    fig1.savefig("%s/flick-events-hist_%s.pdf"%(fig_save,bin_size))
    f.close()
    t.close()

def plot_hist_bins(bin_size):
    f = shelve.open("%s_%s.dat"%(fupbin,bin_size))
    t = shelve.open("%s_%s.dat"%(tupbin,bin_size))
    fbins = []
    tbins = []
    map(lambda uname: fbins.extend(map (lambda y: y[0],f[uname])), f.keys())
    map(lambda uname: tbins.extend(map (lambda y: y[0],t[uname])), t.keys())
    fbins = np.array(fbins)
    tbins = np.array(tbins)
    fig1 = plt.figure(figsize=(10,14))
    ax1 = fig1.add_subplot(211)
    ax1.hist(fbins, bins=np.unique(fbins),cumulative=True)
    #ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel("flickr bins {%s hr bins}"%(bin_size))
    ax1.set_ylabel("# users active in bin {%s hr bins}"%(bin_size))
    ax2 = fig1.add_subplot(212)
    ax2.hist(tbins, bins=np.unique(tbins),cumulative=True)
    #ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel("twitter bins {%s hr bins}"%(bin_size))
    ax2.set_ylabel("#users active in bin {%s hr bins}"%(bin_size))
    ax2.set_title("flickr and twitter bins histograms {%s hr bins}"%(bin_size))
    fig1.savefig("%s/ft-bins-hist_%s.pdf"%(fig_save,bin_size))
    f.close()
    t.close()
    

def main():
    bins = ["4","24","48"]
    for bin_size in bins:
        try:
            plot_userbins(bin_size)
            plot_userfreq(bin_size)
            plot_hist_events(bin_size)
            plot_hist_bins(bin_size)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

if __name__ == "__main__":
    sys.exit(main())
