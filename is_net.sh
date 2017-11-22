#!/bin/bash

start=$(date +%H:%M:%S)
ping -c 1 8.8.8.8 &>/dev/null
while [ $? -ne 0 ];
do
	time=$(date +%H:%M:%S)
	echo "[$time] Net failed."
	sleep 5

	ping -c 1 8.8.8.8 &>/dev/null
done

ping -c 1 google.com &>/dev/null
while [ $? -ne 0 ]
do
	time=$(date +%H:%M:%S)
	echo "[$time] DNS failed."
	sleep 5

	ping -c 1 google.com &>/dev/null
done
end=$(date +%H:%M:%S)

echo "[!] ($start -> $end)"
echo ""
echo "    _.._..,_,_   Welcome"
echo "   (          )    back!"
echo "    ]~,\"-.-~~["
echo "  .=])' (;  (["
echo "  | ]:: '    ["
echo "  '=]): .)  (["
echo "    |:: '    |"
echo "     ~~----~~ "
# ASCII figure created by: Paul Martin Howard

