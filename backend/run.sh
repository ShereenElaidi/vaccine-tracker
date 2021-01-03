#!/bin/bash

# check if the code is down 
echo "=================RUNNING SCRIPT==================="

# run the script forever
while true;
do 
	# put the output of the docker ps command into a text file
	$(sudo docker ps > docker.txt)
	lines_in_docker_output=$(wc -l docker.txt)
	lines_in_docker_down_output=$(wc -l docker_output.txt)

	echo "Current date: $(date)"

	line_output="${lines_in_docker_output:0:1}"
	line_down="${lines_in_docker_down_output:0:1}"

	# check if they are equal
	if [ $line_output == $line_down ];
	then
		echo "Docker status: Docker stopped running :("
		# re-run the script
		$(sudo docker run -p 80:56666 baebf19f8046)
		echo "Running script..."
	else 
		echo "Docker status: Docker is up and running"
	fi 

	# sleep for one minute
	sleep 60
done 