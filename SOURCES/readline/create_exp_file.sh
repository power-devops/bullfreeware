`echo /usr/bin/nm -X32_64 | /usr/bin/sed -e 's/B\([^B]*\)$/P\1/'` -PCpgl $*  | \
/usr/bin/awk '{ if ((($ 2 == "T") || ($ 2 == "D") || ($ 2 == "B") || ($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) \
&& (substr($ 1,1,1) != ".")) { if (($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) { print $ 1 " weak" } \
else { print $ 1 } } }' | /usr/bin/sort -u

