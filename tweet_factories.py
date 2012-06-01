
from datetime import datetime, timedelta
import gzip
import os
from common.tweet import Tweet
from mdcutils.simple_progress import ProgressMeter, SimpleProgressMeter

def convert_str_to_date(datestr):
    year = int(datestr[0:4])
    month = int(datestr[5:7])
    day = int(datestr[8:10])
    
    return datetime(year = year, month = month, day = day)
    
    

class GardenhoseDiskTweetFactory(object):
    '''
    This reads data from gzipped Bruno-formatted Tweet dumps of gardenhose tweet data.
    '''


    def __init__(self, hosedir, since, until):
        # Since & Until are YYYY-MM-DD
        self.hosedir = hosedir
        self.since = since
        self.until = until
        
    
    def get_tweets(self):
        # Takes YYYY-MM-DD formatted date string and returns all tweets between
        since = convert_str_to_date(self.since)
        until = convert_str_to_date(self.until)
        
        span = until - since
        dates = []
        tick = since
        for i in range(span.days + 1):
            dates.append(tick)
            tick += timedelta(days=1)
        
        
        for date in dates:
            monthstr = date.month
            daystr = date.day
            if date.month < 10:
                monthstr = "0%s" % date.month
            if date.day < 10:
                daystr = "0%s" % date.day            
            datestr = "%s-%s-%s" % (date.year, monthstr, daystr)
            
            gz_file = "%s%s.tweets.dat.gz" % (self.hosedir, datestr)
            dat_file = "%s%s.tweets.dat" % (self.hosedir, datestr)         
            
            fin = None
            if os.path.isfile(gz_file):                
                fin = gzip.open(gz_file)
            elif os.path.isfile(dat_file):                
                fin = open(dat_file)
            else:
                print "Missing File: %s" % datestr  
                continue
                
            print "Parsing Tweets From: %s" % datestr
            numtweets = 0
            for line in fin:
                try:
                    yield Tweet(line.strip(), quiet=True)
                    numtweets += 1
                except(ValueError, IndexError):
                    yield None
            print "Total Tweets: %s" % numtweets

class UserTimelinesDiskTweetFactory(object):
    '''
    This reads data from gzipped Bruno-formatted Tweet dumps of tweet timelines for individual users.
    '''


    def __init__(self, timelinesdir, users=[], verbose=False):
        self.timelinesdir = timelinesdir    
        self.verbose = verbose
        self.users = users
        
        
        if users == []:
            self.pm = ProgressMeter(len([1 for fname in os.listdir(timelinesdir) if fname.endswith('tweet.dat.gz')]))
        else:
            self.pm = ProgressMeter(len(users))
        
    def get_tweets(self):
        filenames = os.listdir(self.timelinesdir)
        if len(self.users) > 0:
            filenames = ["%s.tweets.dat.gz" % (user) for user in self.users]
            
        for fname in filenames:        
            fpath = "%s%s" % (self.timelinesdir, fname)
            fin = None
            if fname.endswith("tweet.dat.gz"):         
                tf = BasicDiskTweetFactory(fpath)
                for t in tf.get_tweets():
                    yield t
                if self.verbose: self.pm.update()

class BasicDiskTweetFactory(object):
    '''
    This reads data from a single gzipped Bruno-formatted tweet file.
    '''

    def __init__(self, tweetfile):
        self.tweetfile = tweetfile 
        
    def get_tweets(self):       
        fin = gzip.open(self.tweetfile)
        
        numtweets = 0
        for line in fin:
            try:
                yield Tweet(line.strip(), quiet=True)
                numtweets += 1
            except(ValueError, IndexError):
                yield None
               
        fin.close()
                