## `create_wiki_training_data.py`
Downloads wikipedia articles into `training_set` folder

## `train_with_wiki.py`
Creates the NMF model using the downloaded wikipedia files. Includes cleaning + training.

## `train_lda_with_wiki.py`
Creates an LDA model using the downloaded wikipedia files. Includes cleaning and training.

## Results
NMF and LDA seem quite comparable. Quality of tags is still fairly low. Need to either throw more data at it or figure out how to tune it.

Thinking that for MVP we have a limited set of possible tags and demo it by creating notes with topics related to the tags we have trained it on. This might be around 10-12 tags to start.

## Quickstart Environment
```bash
python3 -m venv env
source env/bin/activate
pip -r requirements.txt
```
