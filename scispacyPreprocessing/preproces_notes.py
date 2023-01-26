import pandas as pd
import numpy as np

notes = pd.read_csv("/home/dtank/data/volume_2/eicu_csv/note.csv")
notes = notes.astype('string')
notes['notepath'] = notes['notepath'].replace("/", ", ", regex=True)
notes['notetext'] = notes['notetext'].replace(np.nan, "")

notes.to_csv("/home/dtank/data/volume_2/eicu_preprocessed/note.csv")