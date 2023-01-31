import pandas as pd

# csv extraction from within notebook
# extract_csv(saveto='/home/dtank/data/volume_2/eicu_csv/nurseAssessment.csv', variablestring="patient.PatientUnitStayID, patient.uniquepid, patient.hospitaldischargestatus, patient.unitdischargestatus, nurseassessment.cellattributepath, nurseassessment.cellattributevalue", table="patient, nurseassessment")

nurseAssessment = pd.read_csv('/home/dtank/data/volume_2/eicu_csv/nurseAssessment.csv')
nurseAssessment['nurseAssessmentNote'] = nurseAssessment['cellattributepath'] + "|" + nurseAssessment['cellattributevalue']
nurseAssessment['nurseAssessmentNote'] = nurseAssessment.nurseAssessmentNote.str.replace('|', ', ', regex=True)
nurseAssessment.to_csv("/home/dtank/data/volume_2/eicu_preprocessed/nurseAssessment.csv")