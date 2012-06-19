import datetime as dt
import pickle as pl
import math

class util:
    @staticmethod                                                        
    def findmin_max(file_handle, delim=" "):
        fmax = dt.datetime(1,1,dt.MINYEAR)
        fmin = dt.datetime.today()

        for line in file_handle:
            cols = line.strip('\n').split(delim)
            try:
                date = dt.datetime.fromtimestamp(int(cols[6]))
            except:
                print(cols);print(line);print("\nunexpected error\n")

            if(date < fmin):
                fmin = date
            if(date > fmax):
                fmax = date

        return fmax,fmin

    @staticmethod
    def findbin(udate,bin_size, fmin):
        tbin = math.floor((time.mktime(udate.timetuple()) - time.mktime(fmin.timetuple()))/(float(bin_size)*60*60))
        return tbin
