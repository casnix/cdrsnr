#!/bin/sh

whichPython=$(which python)
echo -e "#!$whichPython\n\n" > ./cdrsnr

cat ./cdrsnr.py >> ./cdrsnr
