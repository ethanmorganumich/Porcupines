# NMF Model Creation
This repo contains all of the code used to test and train a model to tag notes for our application NoteSmart.

## `create_wiki_training_data.py`
Downloads wikipedia articles listed in `LIST_OF_PAGES.txt` into `training_set` folder

## `train_with_wiki.py`
Creates the NMF model using the downloaded wikipedia files. Includes cleaning + training.

## `train_lda_with_wiki.py`
Creates an LDA model using the downloaded wikipedia files. Includes cleaning and training.

## `models`
The directory containing our saved NMF models with various numbers of topics. We found that 50 topics was a good number. We came to this conclusion with qualitative analysis of the topics created.

## `cloud_function`
The directory containing the environment which was deployed to our `get_tags` Google Cloud Function. This cloud function is what we request to generate tags for a new note or an updated note.

## All other files
These are files used in the process of testing and creating the model. They are all iterations of various ideas and have been kept in the github repository to demonstrate our process and iterations. Feel free to disregard them. 

## Results of comparison between NMF and LDA
NMF and LDA seem quite comparable. Qualitative quality of tags seems quite similar.

**Future Work**

Perform a more rigorous test to compare NMF and LDA with various numbers of topics, quantitative data (coherance), and various relevant training sets.

## Quickstart Environment
```bash
python3 -m venv env
source env/bin/activate
pip -r requirements.txt
```
