#! /bin/sh
echo $@ | awk 'BEGIN {
Wn=0;
W[Wn++]="-Wstrict-prototypes";
W[Wn++]="-Wall";
W[Wn++]="-Werror=declaration-after-statement";
W[Wn++]="-Werror=format-security";
W[Wn++]="-Werror=format=2";
W[Wn++]="-Werror=implicit-function-declaration";
W[Wn++]="-Werror=init-self";
W[Wn++]="-Werror=missing-include-dirs";
W[Wn++]="-Werror=missing-prototypes";
W[Wn++]="-Werror=pointer-arith";
W[Wn++]="-pthreads";
W[Wn++]="-pthread";
}
{
for(i=1;i<=NF;i++) { for(j=0;j<Wn;j++) { if($i == W[j]) exit(1); } }
exit(0);
}'
if [ $? -eq 1 ]
then
exit 1
else
echo $@
$@
fi
