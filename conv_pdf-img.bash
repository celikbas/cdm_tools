#!/bin/bash

# define usage function
usage()
{
	echo "usage: komut [-f file ] | [-c num] | [-d num] | [-q num] | [-x] | [-h]]"
	exit 1
}

# [[ $# -eq 0 ]] && usage

####### Main ########

while getopts "f:c:d:q:vxh" OPTION
do
      case $OPTION in
          h)
              usage
              exit 1
              ;;
          f)
              WATERMARK=$OPTARG
              ;;
          d)
              DENSITY=$OPTARG
              ;;
          q)
              QUALITY=$OPTARG
              ;;
          c)
              COUNTER=$OPTARG
              ;;
          x)
              OCR=$OPTARG
              ;;
          ?)
              usage
              exit
              ;;
      esac
done

# Test if the watermark file exist.
if [[ ${WATERMARK+x} ]]; then
	if [ -f $WATERMARK ]; then
		ANNOTATING=1
	else
        	ANNOTATING=0
		WATERMARK="No"
	fi
else 
        ANNOTATING=0
	WATERMARK="No"
fi

# Test if the loop defined 
if [ $COUNTER -gt 0 ]; then
	MAXATTEMPT=$COUNTER
else
        MAXATTEMPT=2
fi

# Test if the image density/resolution defined 
if [[ ! ${DENSITY+x} ]]; then
	DENSITY=96
fi

# Test if the image quality defined 
if [[ ! ${QUALITY+x} ]]; then
	QUALITY=75
fi

# Test if OCR enabled 
if [[ ${OCR+x} ]]; then
	OCR_ENABLED="true"
else
	OCR_ENABLED="false"
fi

echo -e "\n"
echo Watermark: $WATERMARK
echo Dizin Sayisi: $MAXATTEMPT
echo Density: $DENSITY
echo Quality: $QUALITY
echo OCR: $OCR_ENABLED
echo -e "\n"
echo "Press any key to continue. Press n to exit [Y/n]"
read -n1 -t10 ANSWER
if [$ANSWER="n"]; then
	exit
fi

COUNTER=1
echo ======================================================
for FILE in *.pdf 
do
	NEWDIR=$(basename "$FILE")
	extension="${NEWDIR##*.}"
	NEWDIR="${NEWDIR%.*}"

	if [ -d $NEWDIR ]
	then
		echo Dizin var: $NEWDIR
	else
		echo Çalışıyor : $NEWDIR "("$COUNTER / $MAXATTEMPT")"
		mkdir -p $NEWDIR/scans
		convert -density $DENSITY -quality $QUALITY $FILE $NEWDIR/scans/page_%03d.jpg

		# add a watermark to all images
		if [ $ANNOTATING -gt 0 ]
		then
			for IMAGE in $NEWDIR/scans/*
			do
				composite -dissolve 10 -gravity southeast $WATERMARK $IMAGE $IMAGE
			done
		fi

		# Start OCR images
		if ${OCR_ENABLED:=true} 
		then
			mkdir -p $NEWDIR/transcripts
			for IMAGE in $NEWDIR/scans/*
			do
				DEST=$(basename "$IMAGE")
				DEST="${DEST%.*}"
				tesseract $IMAGE $NEWDIR/transcripts/$DEST -l fra
			done
		fi

		COUNTER=$((COUNTER+1))
		if [ $COUNTER -gt $MAXATTEMPT ]
		then
			exit 0
		fi
	fi
done

