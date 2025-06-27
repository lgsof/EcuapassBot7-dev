
SIZE=612x877
PDF=$1
PNG="`echo $1|cut -d. -f1`-$SIZE.png"
echo $PNG
convert -density 150 $PDF -resize $SIZE $PNG
