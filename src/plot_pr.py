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

minflick = "mintwit_utc"
maxflick = "maxtwit_utc"
cos = "/l/vision/knkumar/withutc1/cos"
jaccard = "/l/vision/knkumar/withutc1/jaccard"
fig_save = "/l/vision/knkumar/withutc1"


def plot_prcurve(bin_size):
    jc = shelve.open("%s_%s_conf.dat"%(jaccard,bin_size))
    cosine = shelve.open("%s_%s_conf.dat"%(cos,bin_size))
    jc_precision = map(lambda tp,fp: tp/float(tp+fp) if (tp+fp)>0 else 0, jc['tp'],jc['fp'])
    jc_recall = map(lambda tp,fn: tp/float(tp+fn) if (tp+fn)>0 else 0, jc['tp'],jc['fn'])
    cos_recall = map(lambda tp,fn: tp/float(tp+fn) if (tp+fn)>0 else 0, cosine['tp'], cosine['fn'])
    cos_precision = map(lambda tp,fp: tp/float(tp+fp) if (tp+fp)>0 else 0, cosine['tp'],cosine['fp'])
    print jc_recall
    print jc_precision
    print cos_recall
    print cos_precision
    fig1 = plt.figure(figsize=(10,14))
    ax1 = fig1.add_subplot(211)
    ax1.plot(jc_recall, jc_precision, 'b--', cos_recall,cos_precision, 'k')
    #ax1.set_xscale('log')
    ax1.set_xlabel("Recall {%s hr bins}"%(bin_size))
    ax1.set_ylabel("Precision {%s hr bins}"%(bin_size))
    ax1.set_title("PR-curve for jaccard and cosine{%s hr bins}"%(bin_size))
    ax1.legend(('Jaccard','Cosine'),'upper right',shadow=True)
    fig1.savefig("%s/pr_curve_%s.pdf"%(fig_save,bin_size))
    jc.close()
    cosine.close()
    

def main():
    try:
        plot_prcurve('48')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

if __name__ == "__main__":
    sys.exit(main())
