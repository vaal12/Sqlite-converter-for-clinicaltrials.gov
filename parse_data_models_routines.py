
from sqlalchemy.orm.attributes import InstrumentedAttribute

def parseDataModels(datamodelsList):
    DataModels = []
    for dataModel in datamodelsList:
        theModel = {"name": str(dataModel), "class": dataModel}

        print("\n\n\n\n")
        print("have dataModel:{}".format(dataModel))
        studies_field_list = [col for col in dir(dataModel) if type(getattr(dataModel, col)) is (InstrumentedAttribute)]
        print("Data Field list: \n{}\n".format(studies_field_list))

        studies_field_doc_strs = [getattr(getattr(dataModel, col), "doc") for col in studies_field_list if getattr(getattr(dataModel, col), "doc") is not None ]

        print(" Data field List docs:\n{} \n".format(studies_field_doc_strs))

        # print(zip(studies_field_list, studies_field_doc_strs))

        theModel["fields"] = zip(studies_field_list, studies_field_doc_strs)

        DataModels.append(theModel)

    return DataModels
