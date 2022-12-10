# Training Data for NMF model

## Set 1
Manually created using GPT-3. We found that this method of training data generation would be expensive and due to rate limits would not be able to create the quantity of data we would like.

## Set 2
Manually generated wikipedia article titles which would be create interesting topics. Then, the articles were downloaded from wikipedia into a format which we could use to train.

## Set 3
This is our most curated data set which was used to train our current model.

1. Manually generated an ideal list of 30 tags we wanted to create.
2. Scraped the wikipedia index using [webscraper.io](https://webscraper.io) for each of the tags we wanted to create. This led us to a set of over 20,000 wikipedia article titles.
3. Downloaded the list of article titles we had scraped into a format which was easy to understand and used this to train the model.
