import logging

#https://docs.python.org/2/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET

#Works as CrossJoin on data: https://www.w3resource.com/sql/joins/cross-join.php
def parseXMLKeyBranchWithList(parentNode, childNodeBranchList):
    logging.debug("")
    # logging.debug("")
    curr_tabStr = "\t"*(4-len(childNodeBranchList))
    logging.debug(curr_tabStr+"parseXMLKeyBranchWithList parentNodeName:"+parentNode.tag)
    logging.debug(curr_tabStr+"parseXMLKeyBranchWithList parsing list:"+str(childNodeBranchList))
    # logging.debug("Iterating over child tag:"+childNodeBranchList[0])
    currNodeBranchTag = childNodeBranchList[0]
    del childNodeBranchList[0]

    retList = []

    if not (parentNode.find(currNodeBranchTag) is None):
        foundTextsOfNodes = []
        #Found the child node
        if len(childNodeBranchList)==0:
            #THis is the last child in branch
            # logging.debug( "Found tag text:"+parentNode.find(currNodeBranchTag).text)
            for foundNode in parentNode.findall(currNodeBranchTag):
                foundTextsOfNodes.append(foundNode.text)
            return foundTextsOfNodes
        else:
            # This is not the last child in branch - recursing downs
            logging.debug(curr_tabStr+"This is Recursion.")
            for foundNode in parentNode.findall(currNodeBranchTag):

                foundTextsOfNodes.extend(parseXMLKeyBranchWithList(foundNode,
                                            list(childNodeBranchList)))
            return foundTextsOfNodes
        #END if len(childNodeBranchList)==0:

    else:
        #Not found the node - returning empty list
        logging.debug(curr_tabStr+"Node not found. Returning empty list")
        return []
    #END if not (parentNode.find(currNodeBranchTag) is None):
#END def parseXMLKeyBranch(parentNode, childNodeBranchList):



def parseXMLToDataModel(dataModel):

    for field in dataModel["fields"]:
        print("Parsing field:{}".format(field))



def parserXMLNCTFile(fileName, dataModelsList):
    logging.debug("")
    logging.debug("")
    logging.debug("")
    logging.debug("")
    logging.debug("")
    logging.debug("")
    logging.debug("*********************************************************")
    logging.debug("*********************************************************")
    logging.debug("*********************************************************")
    logging.debug( "parserXMLNCTFile. parsing file:"+fileName)
    logging.debug("*********************************************************")
    logging.debug("*********************************************************")
    logging.debug("*********************************************************")
    logging.debug("")
    logging.debug("")

    dataObjectsCreated = []

    tree = ET.parse(fileName)
    root = tree.getroot()

    for dataModel in dataModelsList:
        # print("parsing datamodel:{}".format(dataModel["name"]))
        # parseXMLToDataModel(dataModel)

        #Create instance of the class
        dataClass = dataModel["class"]()

        for key_tuple in (dataModel["fields"]):
            key = key_tuple[0]
            xml_path = key_tuple[1]
            logging.debug( "Parsing for key:"+key)
            logging.debug( "Key path:"+xml_path)
            childNodeBranchList = xml_path.replace(" ", "").split('>')

            # keyBranchText = parseXMLKeyBranch(root, childNodeBranchList)
            keyBranchTextArray = parseXMLKeyBranchWithList(root, childNodeBranchList)

            if len(keyBranchTextArray)>1:#This is primary table - we do not need any duplicates - will put a warning to log file
                logging.debug("")
                logging.debug("")
                logging.debug("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                logging.debug("     !!WARNING!!")
                logging.debug("File:"+fileName)
                logging.debug("Has duplicate XML key at path:"+xml_path)
                logging.debug("List returned by parseXMLKeyBranchWithList:"+str(keyBranchTextArray))
                logging.debug("Advised to review Main study table fields to remove this field.")
                logging.debug("So main table will only contain one record per XML file (nct_id will serve as primary key for secondary tables).")
                logging.debug("Move any data of interest, which can have multiple entries per XML file to secondary tables.")
                logging.debug("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                logging.debug("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                logging.debug("")
                logging.debug("")


            logging.debug( "childNodeBranchList at the end:"+str(childNodeBranchList))

            
            
            if len(keyBranchTextArray) > 0:#field found
                keyBranchText = keyBranchTextArray[0]
                logging.debug("keyBranchText:"+keyBranchText[:30])
                setattr(dataClass, key, keyBranchText)
                # print("Key:{}".format(key))
                # print("text:{}".format(keyBranchText))

                # StudyTableRec.append(keyBranchText.strip().encode("utf-8"))
                # StudyTableRec.append(keyBranchText)
            else:#Field not found - putting NONE to datatable
                logging.debug("keyBranchText IS NONE")
                setattr(dataClass, key, "**None**")
                # StudyTableRec.append("**None**")
            # print("DataObject:{}".format(dataClass))
            # print(dataClass.nct_id)
            # print(dataClass.overall_status)
           
        #END for key_tuple in dataModel["fields"]:
        dataObjectsCreated.append(dataClass)
    #END for dataModel in dataModelsList:

    return dataObjectsCreated






    # for field in studies_field_list:
        #         if field <> "id":
        #                 setattr(new_study, field, "I am a field:"+field)