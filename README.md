# TechCrunch Disrupt NYC 2011 Hackathon Hacking!
### Still lots & lots of work to be done
**Lots of kmeans, ENT help from Ben Lacker and the ENT section [here](http://web.cs.swarthmore.edu/~turnbull/Papers/Tingle_Autotag_MIR10.pdf)**

**Get an [Echo Nest Dev. Key](http://developer.echonest.com/docs/v4/) and [Echo Nest Remix API](http://code.google.com/p/echo-nest-remix/)**

*Description*:
WebRemix! is a url-page audio remixer (currently, only available as script, will eventually be a chrome extension). It parses the html tags in a webpage and then attributes changes in the page's patterns (i.e. if 4 p tags are followed by a div tag, then a music shift will occurr) to specific segments/samples in a musical track, segments that have been reorganized (clustered) by timbre or pitch (up to the user). The music part of the project uses the echonest api (specifically, the remix api) to extract timbre and pitch features (more info can be found [here](http://developer.echonest.com/docs/v4/_static/AnalyzeDocumentation_2.2.pdf). From the api, one receives the track in song segments (500ms or so). These segments are then clustered by a kmeans algorithm in order to group segments related by their pitches and timbres. When reading the html in a given webpage, each pattern is assigned a cluster and then a random segment from that cluster. When the pattern changes, a new cluster will be used. This is how the remix occurs. 

Call it like this: `python echocluster.py {pick a url} {pick an mp3}, more explicitly --> python echocluster.py http://www.google.com test.mp3`

#### Sound samples
[original file](http://dl.dropbox.com/u/13241544/canon.mp3)

[remixed google.com - timbre clusters](http://dl.dropbox.com/u/13241544/remix.wav)

##### I apologize ahead of time for any chaotic or bad code!


