#!/usr/bin/python
import readFlickr as rf
import readtwitter as rt
import coefficients as cf
import sys
from util import util


def rflick(bin_size):
    try:
        flick = rf.FlickData(bin_size)
        if flick.fmax == 0.0:
            fmax,fmin = util.findmin_max(flick.infile , flick.delim)

        flick.write_back(fmax,fmin)
        #makebins(0.5)
        #makebins(2)
        #makebins(24)
        flick.makebins(bin_size)
        return flick.fldict
        
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def rtwit(bin_size):
    try:
        twit = rt.TweetData(bin_size)
        if twit.tmax == 0.0:
            tmax,tmin = util.findmin_max(twit.infile, twit.delim)
            twit.write_back(tmax, tmin)
        #makebins(0.5)
        #makebins(2)
        twit.makebins(bin_size)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return twit.twdict

def ft_coeff(bin_size):
    comp_coeff = cf.coeff(bin_size)
    comp_coeff.correlate_jaccard(bin_size)
    comp_coeff.correlate_cosine(bin_size)

def plot_data(bin_size):
    pass

def main():
    bin_size = "4"
    fdict = rflick(bin_size)
    tdict = rtwit(bin_size)
    ft_coeff(bin_size)

if __name__ == "__main__":
    sys.exit(main())
