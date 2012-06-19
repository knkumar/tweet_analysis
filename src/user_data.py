import shelve
import sys

inp_file = "twitter_intersection_2010-05-01_2010-08-30.tweets.dat"
out_shelve = "twit_user_map" 
twit_shelf = "twit_user_map" 
fl_shelf = "user_map" 
twitfile = "/l/vision/knkumar/twitshelf_utc"
twitout = "/l/vision/knkumar/ttshelf_utc"

def map_users():
    fuser = open(inp_file,"rb")
    fumap = shelve.open(out_shelve)
    for line in fuser:
        cols = line.strip('\n').split('|')
        if len(cols) < 10:
            continue
        userid = cols[0]
        name = cols[9]
        if userid in fumap:
            continue
        else:
            fumap[userid] = name
    fumap.close()

def main():
    tumap = shelve.open("twit_user_map")
    torigin = shelve.open("%s_%s"%(twitfile,"48"))
    tdest = shelve.open("%s_%s"%(twitout,"48"))
    miss = 0
    for key in torigin.keys():
        if key not in tumap:
            miss += 1
            continue
        new_key = tumap[key]
        tdest[new_key] = torigin[key]
    print "twitter miss: ",miss
    tumap.close()
    torigin.close()
    tdest.close()

if __name__ == "__main__":
    sys.exit(main())
