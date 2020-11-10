"""
This script is a quick and dirty implementation which takes in a file path and cleans up the text by:
1.  Converting all capitals to lower case
2. removing all numerals
3. removing all special characters except ,."'

It will save a file in the same path with the addition of _clean to the file name.

To run the script on an example file type
python clean_text.py --path /path/to/file/ --files file_name_1 file_name_2
"""

import argparse
import os
import preprocessor as p


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Reads in txt file and cleans the text')
    parser.add_argument('--path', type=str, help='Path to where all files are located')
    parser.add_argument('--files', metavar='N', type=str, nargs='+', help='list of files that we want to clean')
    args = parser.parse_args()

    os.system('rmdir cleanData')
    os.system('mkdir cleanData')

    for file_name in args.files:
        # Load in Raw Text
        path_to_file = "{path}{file_name}".format(path=args.path, file_name=file_name)
        
        # store all tweets in an array
        tweet_database = []
        with open(path_to_file, encoding="utf-8") as fp:
            tweet = fp.readline()
            line_cnt = 0
            while tweet:
                # Looks for actual tweets
                if tweet.strip() != "==========":
                    # Clean with the twitter preprocessor to remove url, mentions, and RT & FAV
                    p.set_options(p.OPT.MENTION, p.OPT.RESERVED, p.OPT.URL)
                    cleaned_tweet = p.clean(tweet)

                    # Checks for solo semi-colons
                    if cleaned_tweet.strip() == ":":
                        cleaned_tweet = ""
                    
                    if cleaned_tweet != "":
                        if cleaned_tweet[0] == ":":
                            cleaned_tweet = cleaned_tweet[2:]
                    
                    # If the tweet is not empty, store in database
                    if cleaned_tweet != "":
                        tweet_database.append(cleaned_tweet.strip()+'\n==========\n')

                tweet = fp.readline()
                line_cnt += 1
                if line_cnt % 100 == 0:
                    print("...Cleaned {} lines".format(line_cnt))
        
        # Extract the name from the file name
        name = file_name.split('.')[0]

        print("Finished parsing {}!".format(name))
        fp.close()

        # save the file if we feel like it
        temp_file = open('./twitterScrubber/cleanData/{file_name}_clean.txt'.format(file_name=name), 'w', encoding="utf-8")
        for tweet in tweet_database:
            temp_file.write(tweet)
        temp_file.close()

