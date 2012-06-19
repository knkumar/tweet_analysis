import shelve
import datetime as dt
import sys
import time
import pickle as pl
from settings import *
import math
from util import util

class FlickData:
    delim = " "
    def __init__(self,bin_size):
        self.maxpkl = open(maxflick,'wb')
        self.minpkl = open(minflick,'wb')
        try:
            self.infile = open(fl_fname,'rb')
            self.fmin = pl.load(self.minpkl)
            self.fmax = pl.load(self.maxpkl)
        except IOError:
            self.infile = open(fl_fname,'rw')
            self.fmin = 0.0
            self.fmax = 0.0
        self.fldict = shelve.open("%s_%s"%(fshelf,bin_size))
        self.user_map = shelve.open("user_map") #this contains the mapping from userid to username
        self.user_keys = self.user_map.keys()

    def __update__(self):
        pass

    def __del__(self):
        self.maxpkl.close()
        self.minpkl.close()
        self.infile.close()
        self.fldict.close()
        
    def update_user_info(self, user, laln, tags, bins):
        userDict = self.fldict[self.user_map[user]] # retrieve user records
        if bins in userDict.keys(): # if we have already created a bin for this user
            binDict = userDict[bins]
            binDict[0] = binDict[0]+1
            binDict[1].append(laln) # fetch the bin and update
            binDict[2].extend(tags)
            userDict[bins] = binDict
            self.fldict[self.user_map[user]] = userDict
        else:
            flick_log.debug("Bin : %s" % bins)
            count = 1
            list_laln = []
            list_tags = []
            list_laln.append(laln)
            list_tags.extend(tags)
            userDict[bins] = [count,list_laln,list_tags] # else just create the bin
            self.fldict[self.user_map[user]] = userDict
    

    def create_user_info(self, user, laln, tags, bins):
        flick_log.debug("User : %s" % user)
        count = 1
        list_laln = []
        list_tags = []
        list_laln.append(laln)
        list_tags.extend(tags)
        binDict = {bins : [count,list_laln,list_tags]}
        self.fldict[self.user_map[user]] = binDict

    def makebins(self, bin_size):
        # open the pickle files
        # open the shelve dictionary to store the data
        
        for line in self.infile:
            flick_log.debug(line)
            #strip the cols
            cols = line.strip('\n').split() # cols for the flickr data
            if cols[0] not in user_keys:
                continue
            if len(cols) < 21: # if the data is not the right format - this can be considered as noise
                continue

            try:
                date =  dt.datetime.fromtimestamp(int(cols[6])) # date when this photo was uploaded
            except:
                continue

            if date < fmin or date > fmax:
                continue

            #the columns look ok go ahead and extract the data

            laln = (cols[9],cols[10]) # the latitude and longitude where this picture was taken
            bins = util.findbin(date,bin_size,self.delim) # find the bin to which this date belongs - the bins are 4 hrs apart
            tags = cols[20].split(',') # the tags attached with this picture upload
            #print laln,bin,tags
            if self.user_map[cols[0]] in self.fldict: # if we have user data
                self.update_user_info(cols[0], laln, tags, bins)
            else: 
                self.create_user_info(cols)

    def write_back(self,fmax,fmin):
        pl.dump(fmax, self.maxpkl)
        pl.dump(fmin, self.minpkl)

def main():
    try:
        flick = FlickData(48)
        if flick.fmax == 0.0:
            fmax,fmin = util.findmin_max(flick.infile , flick.delim)

        flick.write_back(fmax,fmin)
        #makebins(0.5)
        #makebins(2)
        #makebins(24)
        makebins(48)
        
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

if __name__ == "__main__":
    sys.exit(main())
