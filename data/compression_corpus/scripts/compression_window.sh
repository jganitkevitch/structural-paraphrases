
# slices an acceptably compressed portion out of the data

awk '{ if ($1 > 0.5 && $1 <= 0.8) { print $0 } }'

