import argparse
import spacy
import scispacy
from scispacy.abbreviation import AbbreviationDetector
from scispacy.linking import EntityLinker
import en_ner_bc5cdr_md
import pandas as pd

def create_nlp_pipeline():
    nlp = en_ner_bc5cdr_md.load()
    nlp.add_pipe("abbreviation_detector")
    config = {
        "k": 10,
        "resolve_abbreviations": True,
        "linker_name": "umls",
        "max_entities_per_mention": 1
    }
    nlp.add_pipe("scispacy_linker", config=config)
    return nlp

def create_new_scispacy_df():
    new_df = pd.DataFrame(columns=['Full note', 'Extracted entities', 'Entity labels', 'CUIs', 'UMLs linked entity names'])
    return new_df

def get_data_name(data_file):
    return data_file.split("/")[-1].split(".")[0]

def perform_entity_linking(data, note_column, nlp):
    linked_entity_df = create_new_scispacy_df()
    linker =  nlp.get_pipe("scispacy_linker")

    for sentence in data[note_column]:
        ents = []
        labels = []
        cuis = []
        linked_ent_names = []

        note = nlp(sentence)

        for entity in note.ents:
            ents.append(entity.text)
            labels.append(entity.label_)

            for linker_ent in entity._.kb_ents:
                cui = linker.kb.cui_to_entity[linker_ent[0]][0]
                linked_entity_name = linker.kb.cui_to_entity[linker_ent[0]][1]

                cuis.append(cui)
                linked_ent_names.append(linked_entity_name)

                linked_entity_df = linked_entity_df.append({'Full note' : sentence, 'Extracted entities' : ents, 
                'Entity labels' : labels, 'CUIs' : cuis, 'UMLs linked entity names' : linked_ent_names}, ignore_index=True)

    return linked_entity_df

def save_linked_entity_df(linked_df, data_name):
    linked_df.to_csv(f'/home/dtank/TempData/scispacyLinked/entityLinked-{data_name}.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_file", help="The .csv file that will be linked using scispacy")
    parser.add_argument("--note_column", help="The column name of the text that will be linked using scispacy")
    args = parser.parse_args()

    nlp = create_nlp_pipeline()
    data = pd.read_csv(args.data_file)
    data_name = get_data_name(args.data_file)
    print(data_name)

    linked_entity_df = perform_entity_linking(data, args.note_column, nlp)
    save_linked_entity_df(linked_entity_df, data_name)