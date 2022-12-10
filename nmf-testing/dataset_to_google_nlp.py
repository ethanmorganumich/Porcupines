from datasets import load_dataset

# load_dataset("wikipedia", language="sw", date="20220120", beam_runner=...)

x = load_dataset("wikipedia", "20221101.simple")



print(x)