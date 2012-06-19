import shelve
import datetime as dt
import sys
import time
import pickle as pl
from util import util
from settings import *

class TweetData:
    delim = "|"

    def __init__(self,bin_size):
        self.maxpkl = open(maxtwit,'wb')
        self.minpkl = open(mintwit,'wb')
        try:
            self.infile = open(tw_fname,'rb')
            self.tmin = pl.load(self.minpkl)
            self.tmax = pl.load(self.maxpkl)
        except IOError:
            self.infile = open(tw_fname,'rw')
            self.tmin = 0.0
            self.tmax = 0.0
        self.twdict = shelve.open("%s_%s"%(tshelf, bin_size))
        self.user_map = shelve.open("user_map")
        self.user_keys = self.user_map.keys()
        
    def __update__(self):
        pass

    def __del__(self):
        self.maxpkl.close()
        self.minpkl.close()
        self.infile.close()
        self.twdict.close()

        """
        Function to update the user info -
        Input : 
        Cols read from the file - user, [lat lon], (tweet words), tim_bins 
        Action : 
        Check if the user time_bin exists, The dict format is {user : {bin : count, [lat lon], tags} }
        update the user bin with new data from [lat lon] and add tags to the dictionary

        """
    def update_user_info(self, user, laln, tags, bins):
        userDict = self.twdict[self.user_map[users]] # retrieve user records
        if bin in userDict.keys(): # if we have already created a bin for this user
            binDict = userDict[bins]
            binDict[0] = binDict[0]+1
            binDict[1].append(laln) # fetch the bin and update
            binDict[2].extend(tags)
            userDict[bins] = binDict
            self.twdict[self.user_map[user]] = userDict
        else:
            twit_log.debug("Bin : %s" % bins)
            count = 1
            list_laln = []
            list_tags = []
            list_laln.append(laln)
            list_tags.extend(tags)
            userDict[bins] = [count,list_laln,list_tags] # else just create the bin
            self.twdict[self.user_map[user]] = userDict

    def create_user_info(self, user, laln, tags, bins):
        twit_log.debug("User : %s" % user)
        count = 1
        list_laln = []
        list_tags = []
        list_laln.append(laln)
        list_tags.extend(tags)
        binDict = {bins : [count,list_laln,list_tags]}
        self.fldict[self.user_map[user]] = binDict


    def makebins(self, bin_size):
    
        for line in self.infile:
            cols = line.strip().split('|') # cols for the twitter data
            date = dt.datetime.fromtimestamp(int(cols[2])) # date when this tweet was uploaded
            bins = util.findbin(date,bin_size,delim) # find the bin to which this date belongs - the bins are 4 hrs apart
            user = cols[0]
            if len(cols) > 12:
                laln = (cols[12],cols[13]) # the latitude and longitude

            tweet = cols[3].split() # the tags attached with this picture upload

            if user in twdict: # if we have user data
                self.update_user_info(user, laln, tweet, bins)
            else: 
                self.create_user_info(user, laln, tweet, bins)

    def write_back(self, tmax, tmin):
        pl.dump(tmax, self.maxpkl)
        pl.dump(tmin, self.maxpkl)



def main():

    try:
        twit = TweetData(48)
        if twit.tmax == 0.0:
            tmax,tmin = util.findmin_max(twit.infile, twit.delim)
            twit.write_back(tmax, tmin)
        #makebins(0.5)
        #makebins(2)
        twit.makebins(48)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

if __name__ == "__main__":
    sys.exit(main())
