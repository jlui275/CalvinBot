import gpt_2_simple as gpt2
import os

# The name of the pretrained GPT2 model we want to use it can be 117M, 124M, or 355M
# 124M is about as big as I can fit on my 1080Ti.
model_name = "124M"

# Download the model if it is not present
if not os.path.isdir(os.path.join("models", model_name)):
    print("Downloading {model_name} model...")
    gpt2.download_gpt2(model_name=model_name)

# Start a Tensorflow session to pass to gpt2_simple
sess = gpt2.start_tf_sess()

# Define the number of steps we want our model to take we want this to be such that
# we only pass over the data set 1-2 times to avoid overfitting.
num_steps = 25

# This is the path to the text file we want to use for training.
text_path = "cleanData/new_FakeKenty_tweets_clean.txt"

# Pass in the session and the tuning parameters
gpt2.finetune(sess,
              text_path,
              model_name=model_name,
              steps=num_steps
             )

gpt2.generate(sess)

