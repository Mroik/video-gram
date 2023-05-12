#!/bin/bash
for link in $(cat $1)
do
	videogram -c $2 $link  # videogram is the script to pull manifests (main.py, in my system it's in path as videogram)
done

for ff in $(ls *.mpd)
do
	yt-dlp $(litterbox -t $ff)
done
