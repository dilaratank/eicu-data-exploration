import argparse
import spacy
import scispacy
from scispacy.abbreviation import AbbreviationDetector
from scispacy.linking import EntityLinker
import en_ner_bc5cdr_md # make sure you download the model with pip install pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bc5cdr_md-0.5.1.tar.gz
import pandas as pd
import warnings
import gc
from tqdm import tqdm

def set_environment():     
    """Sets the CUDA environment and ignores warnings that cloud useful output"""

    spacy.require_gpu()
    print('gpu enabled')
    warnings.filterwarnings("ignore")
    print('warnings ignored')

def create_nlp_pipeline():
    """Creates the NLP pipeline according to standard configurations of previous projects"""

    nlp = en_ner_bc5cdr_md.load()
    nlp.add_pipe("abbreviation_detector")
    config = {
        "k": 10,
        "resolve_abbreviations": True,
        "linker_name": "umls",
        "max_entities_per_mention": 1
    }
    nlp.add_pipe("scispacy_linker", config=config)
    print('nlp environment set')
    return nlp

def create_new_scispacy_df():
    """Creates a dataframe to store the extracted information"""

    new_df = pd.DataFrame(columns=['ID', 'Full note', 'Extracted entities', 'Entity labels', 'CUIs', 'UMLs linked entity names'])
    return new_df

def get_data_name(data_file):
    """Gets data name from original filename, used for naming conventions"""
    return data_file.split("/")[-1].split(".")[0]

def perform_entity_linking(data, note_column, nlp, data_name):
    """Performs the entity linking, returns the dataframe filled with extracted information"""

    linked_entity_df = create_new_scispacy_df()
    linker =  nlp.get_pipe("scispacy_linker")

    # loop over all the sentences in the dataframe column
    for i, sentence in enumerate(tqdm(data[note_column])):

        # save and garbage collect every 10000 iterations
        if i % 10000 == 0:
            save_linked_entity_df(linked_entity_df, data_name)
            gc.collect()

        # for each sentence, store the collected entities, lables, cuis, and linked entity names
        ents = []
        labels = []
        cuis = []
        linked_ent_names = []

        try:
            note = nlp(sentence)
        except:
            continue

        # go over all entities found in a sentence, and link it against the UMLS knowledge base
        for entity in note.ents:
            ents.append(entity.text)
            labels.append(entity.label_)

            for linker_ent in entity._.kb_ents:
                cui = linker.kb.cui_to_entity[linker_ent[0]][0]
                linked_entity_name = linker.kb.cui_to_entity[linker_ent[0]][1]

                cuis.append(cui)
                linked_ent_names.append(linked_entity_name)

                linked_entity_df = linked_entity_df.append({'ID' : data['patientunitstayid'][i], 'Full note' : sentence, 'Extracted entities' : ents, 
                'Entity labels' : labels, 'CUIs' : cuis, 'UMLs linked entity names' : linked_ent_names}, ignore_index=True)

    return linked_entity_df

def save_linked_entity_df(linked_df, data_name):
    """Save the extracted data to a fixed location"""
    linked_df.to_csv(f'/home/dtank/data/volume_2/scispacyLinked/entityLinked-{data_name}.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_file", help="The .csv file that will be linked using scispacy")
    parser.add_argument("--note_column", help="The column name of the text that will be linked using scispacy")
    args = parser.parse_args()

    # Set up the GPU, SciSpacy nlp pipeline, and read data
    set_environment()
    nlp = create_nlp_pipeline()
    data = pd.read_csv(args.data_file)
    data_name = get_data_name(args.data_file)

    # perform entity linking and save final linked file
    linked_entity_df = perform_entity_linking(data, args.note_column, nlp, data_name)
    save_linked_entity_df(linked_entity_df, data_name)
