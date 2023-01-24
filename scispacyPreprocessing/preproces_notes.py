import pandas as pd

notes = pd.read_csv("/home/dtank/data/volume_2/eicu_csv/note.csv")
notes['notepath'] = notes['notepath'].replace("/", ", ", regex=True)

notes.to_csv("/home/dtank/data/volume_2/eicu_preprocessed/note.csv")