#!/bin/bash
INSTRUCTION_FILE="/var/lib/docker/volumes/docker-compose-project_iptv-volume/_data/telegram_pi_instructions.txt"
if [ -e $INSTRUCTION_FILE ];then
   if [ -s $INSTRUCTION_FILE ];then   
     echo "File exist and not empty"
     command=`cat $INSTRUCTION_FILE`
     echo $command
     echo "Cached and Deleting instruction file!!"
     rm -rf $INSTRUCTION_FILE
     eval "$(echo $command)"
   else
     echo "File empty"
   fi
fi
