import os
import sys
from operator import itemgetter
import matplotlib
from echonest import audio
import numpy as np
import scipy.misc
from scipy.cluster.vq import vq, kmeans2, whiten, kmeans
import pylab
from BeautifulSoup import BeautifulSoup as BSS
import re
import urllib2
import random
import subprocess
audio_file = 'remix.wav'

def timbrecluster(segments,no_clusters):
	t_timbre = np.array([i.timbre for i in segments])	
	t_timbre = t_timbre.conj().transpose()
	#manipulations for making ent+delta --> 36 dim vector for each segment
	t_diff1 = np.diff(t_timbre, n=1)
	t_diff1.resize((12,len(segments)))
	t_diff2 = np.diff(t_timbre, n=2)
	t_diff2.resize((12,len(segments)))
	t_mat = np.concatenate((t_timbre, t_diff1,t_diff2), axis=0)
	features = t_mat.conj().transpose() #final matrix
	####################################
	#features = whiten(features)
	try:
		codebook = kmeans(features, no_clusters, iter=60)
		idx, dists = vq(features, codebook[0])
		clusters = [[] for cluster in range(no_clusters)]
		for i in range(len(idx)):
			#segments[i].dist = int((dists[i]-min(dists)) * 100.0 / (max(dists) - min(dists)))
			clusters[idx[i]].append(segments[i])
		#########map the clusters
		#colors = ([([0.4,1,0.4],[1,0.4,0.4],[0.1,0.8,1],[0.4,1,0.4],[1,0.4,0.4],[0.1,0.8,1],[0.4,1,0.4],[1,0.4,0.4],[0.1,0.8,1])[i] for i in idx])
		pylab.scatter(features[:,0],features[:,1])
		pylab.scatter(codebook[0][:,0],codebook[0][:,1], marker='o', s = 500, linewidths=2, c='none')
		pylab.scatter(codebook[0][:,0],codebook[0][:,1], marker='x', s = 500, linewidths=2)
		pylab.savefig('kmeans.png')
		return clusters
	except (TypeError,NameError,ValueError):
		print "error"
		
def pitchcluster(segments,no_clusters):
	features = np.array([i.pitches for i in segments])	
	try:
		codebook = kmeans(features, no_clusters, iter=60)
		idx, dists = vq(features, codebook[0])
		clusters = [[] for cluster in range(no_clusters)]
		for i in range(len(idx)):
			clusters[idx[i]].append(segments[i])
		return clusters
	except (TypeError,NameError,ValueError):
		print "error"
	####################################
	#features = whiten(features)
	
def output_clusters(file, remix):
	out = audio.getpieces(file,remix)
	filename = 'remix.wav'
	out.encode(filename)
	
def theparse(url):
	gotags = []
	webpage = urllib2.urlopen(url)
	code = webpage.read()
	codesoup = BSS(code)
	for child in codesoup.recursiveChildGenerator():
		name = getattr(child, "name", None)
		if name is not None:
			gotags.append(name)
	return gotags
	
def rankbrightness(clusters):
	brightness = {}
	fincluster = []
	for i, nclust in enumerate(clusters):
		tmp_brightness = -5000
		for j in range(len(nclust)):
			if tmp_brightness < (nclust[j].timbre[1]):
				tmp_brightness = nclust[j].timbre[1]
		brightness[i] = tmp_brightness
	brightness = sorted(brightness.items(),key=itemgetter(1), reverse = True)
	#inds = np.argsort(brightness.items)
	for tups in brightness:
		maxind = tups[0]
		fincluster.append(clusters[maxind])
	return fincluster
	
def htmlmapping(tclusters, gotags):
	current_tag = ''
	remixme = []
	current_clust = 0
	# print tclusters[9]
	# print tclusters[9][random.randint(0,len(tclusters[9]) - 1)]
	for tag in gotags:
		if current_tag == tag:
			remixme.append(tclusters[current_clust][random.randint(0,len(tclusters[current_clust]) - 1)])
		else:
			current_tag = tag
			if current_clust < len(tclusters) - 1:
				current_clust += 1
			else:
				current_clust = 0
			remixme.append(tclusters[current_clust][random.randint(0,len(tclusters[current_clust]) - 1)])
	# print len(gotags)
	# print len(remixme)
	return remixme
		
		
	
if __name__=='__main__':
	url = sys.argv[1]
	track = audio.LocalAudioFile(sys.argv[2])
	segments = track.analysis.segments
	tclusters = timbrecluster(segments,12)
	tclusters = rankbrightness(tclusters)
	
	pclusters = pitchcluster(segments,12)
	pclusters = rankbrightness(pclusters)
	
	gotags = theparse(url)
	remix = htmlmapping(tclusters,gotags)
	output_clusters(track, remix)
	return_code = subprocess.call(["afplay", audio_file])
	