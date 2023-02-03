# eICU data exploration: internship I MSc MIK 2023
This repository includes code for the purpose of data exploration of the eICU database. 

## dataExploration
- Contains helpercode ```dataExtraction.py``` and ```datavisualization.py``` which both contain helper functions for the purpose of data extraction from the eiCU database, and data visualization plots. 
- Contains two jupyter notebooks where the acutal data exploration is done, divided in hospital mortality and icu mortality

## scispacyEntityLinking
- Contains code that can be run to perform entity linking on a pandas dataframe
- Contains a notebook that checks the scispacy entity linking time for a dataframe and a concatenated string

## scispacyPreprocessing
- Contains code to preprocess certain datasets so that they can be used for the entity linking