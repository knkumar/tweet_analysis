#Twitter and Flickr time Analysis#

This project contains parts to read data crawled from twitter and Flickr using the readFlickr and readtwitter files.
The data is stored in shelves which are essentially python dictionaries. 

The shelf is indexed in the following format: 
{#userID :{timeBin: [latlon, tags] }}

Once the shelves are formed, we compute the coefficients, using the jaccard and cosine similarity mesaures.

From the coefficients, then generate plots for the various visualizations using matplotlib.

