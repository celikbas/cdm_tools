#!/bin/bash
#
# for f in *.pdf; do pdfimages -j $f img/${f%.*}; done
# for f in *.pdf; do convert $f ${f%.*}.jpg; done
#

FILES="$@"
COUNT=0
for FILE in $FILES
do
    # if image file exists, skip next file.
    if [ -f ${FILE%.*}.jpg ]
    then
        echo "Skiping $FILE file..."
        continue  # process next file and skip converting this file.
    fi
    # converting pdf files to jpeg:
	let "COUNT++"
    echo $COUNT Converting $FILE
	convert $FILE ${FILE%.*}.jpg
done
echo $COUNT files converted.
