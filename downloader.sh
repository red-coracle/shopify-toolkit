while read p; do
  echo "SAVING:  $p"
  filename=$(basename "$p")
  extension="${filename##*.}"
  filename="${filename%.*}"
  echo " -- Filename : $filename"
  curl -o "$filename.$extension" "$p"
done < urls
