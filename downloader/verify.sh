#!/bin/sh

for f in *.sha512; do
  # echo $f
  sha512sum -c $f
  [ $? = 0 ] && continue
  z=${f%.sha512}
  echo "$z baddie"
  # rm -f $z
done
