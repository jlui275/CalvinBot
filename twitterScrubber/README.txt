This directory contains the two python scripts used to scrub a user's timeline and clean their tweets.

scrubber.py - This script with scrub all the existing tweets off of a user's timeline
	- To utilize this script, you will have to edit the twitter handle in the code. You will pass in the handle of the twitter timeline you want to scrub as the input parameter for get_all_tweets() in line 66.
	- The user's timeline will be outputted to the output directory and named "new_{screen_name}_tweets.txt" file with "\n==========\n" deliminating each tweet within the file
	
clean_tweet.py - This script will clean the tweets that are scrubbed using the scrubber.py script
	- This script can be run from the command line. python clean_tweet.py --path <path-to-directory> --file <file-name1> <file-name2> ...
		- path-to-directory is the path to the directory that contains all the file you want to clean
		- file-name are the names of files you that contains the tweets you want to clean
		- For example, we have a new_{screen_name}_tweets.txt file that gets generated and is put into a ./Data/ directory. The call would be "python clean_tweet.py --path ./Data/ --file new_{screen_name}_tweets.txt"
