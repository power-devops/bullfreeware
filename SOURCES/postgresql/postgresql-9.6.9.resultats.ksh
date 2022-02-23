#!/bin/ksh

# Analyse des résultats poutr posgresql

f=$1

[ "$f" == "" ] && {
    export f=$(ls -lrtd $F.*|tail -1|awk '{print $NF}')
}

f1=$(echo $f| grep -e '/' || echo $SPECS/$f )

echo $f| grep -e '/' || f=$SPECS/$f;
					
echo $f1;

[ -e "$f" ] || { echo argument invalide;exit 1; }
ls -lrtd $f || { echo argument invalide;exit 1; }


rm -f  RESULTATS.txt RESULTATS_ERR.txt "RESULTATS_32.txt" "RESULTATS_64.txt" "BUILD.txt" "INSTALL.txt"

echo "ok      :" $(grep -e '^ok ' $f |wc -l)
echo "     ok :" $(grep -e ' ok' $f| grep -v checking |wc -l)
echo "passed  :" $(grep -e passed $f|wc -l)
echo "Failed  :" $(grep -e Failed $f|wc -l)
echo "failed  :" $(grep -e failed $f|wc -l)
echo "FAIL    :" $(grep -e FAIL $f|wc -l)
echo "ERROR   :" $(grep -e ERROR $f|wc -l)
echo "errors: :" $(grep -e errors: $f|wc -l)
echo "(E)     :" $(grep -e '(E)' $f|wc -l)
echo "could   :" $(grep -i -e 'could' $f|wc -l)


grep -e Executing -e '^+ cd'  -e '^+ gm' -e '^ok ' -e ' ok'  -e passed   -e Failed  -e failed  -e FAIL  -e ERROR -e 'File listed twice' -e 'File must b' \
     -e '^============== creating'  -e '^============== running'   \
     <$f | grep -v -e 'g temporary i'  | grep -v checking > RESULTATS.txt


grep -e Executing -e '^+ cd'  -e '^+ gm'  \
     -e '([WIE])'  \
     <$f  | grep -v checking > RESULTATS_WARN.txt


grep -e Executing -e '^+ cd'  -e '^+ gm' -e Failed  -e failed  -e FAIL  -e ERROR \
     -e '([S])' -e 'could' -e errors: -e 'Permission' -e denied \
     <$f  | grep -v checking > RESULTATS_ERR.txt



awk 'BEGIN{R="DEBUT.txt";PH="P"} 
 {
         if ($1=="Executing(%build):"  )     {PH="B";R="BUILD.txt";       }
    else if ($1=="Executing(%install):")     {PH="I";R="INSTALL.txt";     }
    else if ($0=="+ cd ../32bit" && PH=="B") {       R="RESULTATS_32.txt";}
    else if ($0=="+ cd 64bit"    && PH=="B") {       R="RESULTATS_64.txt";}
    else if ($0=="+ cd ../32bit" && PH=="I") {       R="INSTALL_32.txt";}
    else if ($0=="+ cd 64bit"    && PH=="I") {       R="INSTALL_64.txt";}
    print $0 >R;
 }'  RESULTATS.txt 





for f in 64 32;
do
    awk '{
        if ($1=="+") {
            L=$0;
            if (OK==0 && OKCUM==0 && OK2==0) next;
            if (OK2>0) {printf " OK2:%4d Cumul:%4d\n",OK2,OKCUM;OK2=0;}
            printf " OK :%4d Cumul :%4d\n \n",OK,OKCUM;
            printf " %s\n",$0;
            OK=0;OKCUM=0;next
        }
        if ($1=="ok" || $NF=="ok") {
            if (F!=1) {print L;F=1}
            if ($3=="-") {OK2++;OKCUM++;Total++;next;}
#            else if (OK2>0) {printf " OK2:%4d Cumul:%4d\n",OK2,OKCUM;OK2=0;}
            OK++; OKCUM++;Total++;next
        }
        if ($1=="All") {
            if (OK2>0) {printf " OK2:%4d Cumul:%4d\n",OK2,OKCUM;OK2=0;}
            printf " OK :%4d Cumul :%4d\n",OK,OKCUM;
            OK=0;
            print $0;
            next;
        }
        printf " %s\n",$0;
}
END{
    if (OK2>0) {printf " OK2:%4d Cumul:%4d\n",OK2,OKCUM;OK2=0;}
    printf " OK :%4d Cumul :%4d\n",OK,OKCUM;
    printf " \n     Total:%4d\n",Total;
    
}' <RESULTATS_"$f".txt   >RESULTATS_awk_"$f".txt


done











