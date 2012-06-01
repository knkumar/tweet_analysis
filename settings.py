#all the settings are placed in here
import logging

#readFlickr.py settings
logging.basicConfig(filename='flick.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(name)-8s | %(levelname)-8s | %(message)s')
flick_log =  logging.getLogger('flick.py')

fl_fname = "flickr_may_28_2011.dat"

minflick = "minflick_utc"
maxflick = "maxflick_utc"

fshelf = "./shelf/fshelf"


#readtwitter.py settings

logging.basicConfig(filename='twit.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(name)-8s | %(levelname)-8s | %(message)s')
twit_log =  logging.getLogger('twit.py')

tw_fname = "ft_int.dat"
mintwit = "mintwit_utc"
maxtwit = "maxtwit_utc"
tshelf = "./shelf/tshelf"


root = "./shelf"
flickr_inp = fshelf
twitter_inp = tshelf
fupbin =  "%s/fupbin"%root
tupbin = "%s/tupbin"%root
jc_out = "%s/jaccard"%root
cos_out = "%s/cos"%root
jc_bin_out = "%s/jaccard_bin"%root
cos_bin_out = "%s/cosine_bin"%root
jc_rand_out = "%s/jaccard_random_all"%root
cos_rand_out = "%s/cos_random_all"%root


fig_save = "./images"
