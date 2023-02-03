import pandas as pd

notes = pd.read_csv("/home/dtank/TempData/scispacyRaw/features.csv") #dataset from kaggle (nbme score clinical patient notes)
notes['feature_text'] = notes['feature_text'].replace("-", " ", regex=True)
notes["feature_text"] = notes["feature_text"].replace("OR", ",", regex=True)

notes.to_csv("/home/dtank/data/volume_2/scispacyPreprocessed/preprocessedFeatures.csv")