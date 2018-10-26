
import logging

from sqlalchemy.orm.attributes import InstrumentedAttribute

def parseDataModels(datamodelsList):
    DataModels = []
    for dataModel in datamodelsList:
        theModel = {"name": str(dataModel), "class": dataModel}
        logging.debug("Creating data model. Name:{}".format(str(dataModel)))


        print("\n\n\n\n")
        print("have dataModel:{}".format(dataModel))
        studies_field_list = [col for col in dir(dataModel) if type(getattr(dataModel, col)) is (InstrumentedAttribute)]
        print("Data Field list (with ID fields): \n{}\n".format(studies_field_list))

        nonID_field_list = [col for col in studies_field_list if getattr(getattr(dataModel, col), "doc") is not None]

        print("None ID field list:{} \n\n\n".format(nonID_field_list))

        studies_field_doc_strs = [getattr(getattr(dataModel, col), "doc") for col in nonID_field_list]

        print(" Data field List docs:\n{} \n".format(studies_field_doc_strs))

        # print(zip(studies_field_list, studies_field_doc_strs))

        theModel["fields"] = zip(nonID_field_list, studies_field_doc_strs)
        logging.debug("Fields:{}".format(theModel["fields"]))

        DataModels.append(theModel)

    return DataModels
