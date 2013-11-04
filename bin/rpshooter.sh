#!/bin/bash

shoot_pic () {
	for shoot in {1..${numberofpics}}; do
		sleep ${delay}
		${RP_EXEC} ${@}
	done
}

record_vid () {
	sleep ${delay}
	${RP_EXEC} ${@}
}

if [ ${1} == 'still' ]; then
	RP_EXEC="/usr/bin/raspistill"
	shift
	numberofpics=${1}
	shift
	delay=${1}
	shift
	shoot_pic &

elif [ ${1} == 'video' ]; then
	RP_EXEC="/usr/bin/raspivid"
	shift
	delay=${1}
	shift
	record_vid &
else
	exit 2
fi

