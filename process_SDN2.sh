# This bash script runs a mininst python-based application (./simpleNet2.py) for 10 times. The goal is to evaluate the Stats of latency (meand and median) for data trafic from h1 to h2
# the description of this network is given in (./simpleNet2.py)
# to compute the latency, we use the timestamp of reply's receiver - time stamps of request's sender
# The special thing in this version is that the average is taken over each set of ping (i.e., in every iteration) ===> packet-based latency
# This version process_SDN2.sh deals with only the ping command of h1 (the sender/the client).
# Author: Yaser Al Mtawa
# This code is for ilustrating purposes for Western Univserity, Course 4457. The students of this course can freely re-use it as long as they keep this description. 


#!/bin/bash

_numberOfIterations=$(seq 1 1 10)

_homedir=/home/yaser/mininet/ToStudents
_savedir_=/home/yaser/mininet/ToStudents/simpleNet/out








_savedir=$_savedir_"/try1"


_savedir_level2=$_savedir"/level2"
output=$_savedir_"/SDN_Stats"

function function_0 {
                mkdir -p $_savedir
                mkdir -p $_savedir_level2
                mkdir -p $output
                sudo chmod 777 $output
}

function function_A {

for _numberOfIteration in ${_numberOfIterations[@]} 
do

                cd $_homedir
                
		
	
                 sudo python ./simpleNet2.py

               
                cd $_savedir_
                sudo chmod 777 $_savedir_
                cp h1.out $_savedir"/h1_"$_numberOfIteration".out"

                sudo chmod 777 $_savedir

                sudo mn -c
                cd $_savedir
                
                strings "h1_"$_numberOfIteration".out" | grep -i time= | awk '{print $7}' | cut -d= -f2 > $_savedir_level2"/h1_"$_numberOfIteration".out"
            
                cd $_savedir_level2
               

done
} # end function A

function function_B {

count=1
one=1
average=0.0
median=0.0
f=0.0
cd $_savedir_level2
stop=`cat h1_1.out | wc -l`

    echo "STOP ="
    echo "$stop"

while true; do
total=0.0

  for _numberOfIteration in ${_numberOfIterations[@]} 
  do      

                strings "h1_"$_numberOfIteration".out" | perl -ne "$count..$count and print" >> "Final_h1_"$count".out"
                echo "Inside for loop 1"
                f=`strings "h1_"$_numberOfIteration".out" | perl -ne "$count..$count and print"`
                echo "f"
                echo "$f"
               
                total=$(awk '{print $1+$2}' <<<"$total $f")

                echo "total = "
                echo "$total"

  done

  median=`sort -n "Final_h1_"$count".out" | awk -f $_homedir"/"median.awk`
  echo "$median" >> $output"/median_latency.out"
  average=`echo "scale=6;$total/$_numberOfIteration" | bc`

  echo "_numberOfIteration = "
  echo "$_numberOfIteration"
  echo "$average" >> $output"/mean_latency.out"
  count=`echo "scale=3;$count+$one" | bc`

  if [ "$count" -gt "$stop" ]; then
    echo "$count"
    echo "$stop"
    echo "count > stop"
    break
  fi
           
done

} # end function B

function function_C {

for _numberOfIteration in ${_numberOfIterations[@]} 
do
         
   function_B $_numberOfIteration
    
 
done

} # end function C

function_0
function_A
function_B 
#function_C


