import logging

#https://docs.python.org/2/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET

#Works as CrossJoin on data: https://www.w3resource.com/sql/joins/cross-join.php
def parseXMLKeyBranchWithList(parentNode, childNodeBranchList):
    curr_tabStr = "\t"*(4-len(childNodeBranchList))
    # logging.debug(curr_tabStr+"parseXMLKeyBranchWithList parentNodeName:"+parentNode.tag)
    # logging.debug(curr_tabStr+"parseXMLKeyBranchWithList parsing list:"+str(childNodeBranchList))
    # logging.debug("Iterating over child tag:"+childNodeBranchList[0])
    currNodeBranchTag = childNodeBranchList[0]
    del childNodeBranchList[0]

    # retList = []

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
            # logging.debug(curr_tabStr+"This is Recursion.")
            for foundNode in parentNode.findall(currNodeBranchTag):

                foundTextsOfNodes.extend(parseXMLKeyBranchWithList(foundNode,
                                            list(childNodeBranchList)))
            return foundTextsOfNodes
        #END if len(childNodeBranchList)==0:
    else:
        #Not found the node - returning empty list
        # logging.debug(curr_tabStr+"Node not found. Returning empty list")
        return []
    #END if not (parentNode.find(currNodeBranchTag) is None):
#END def parseXMLKeyBranch(parentNode, childNodeBranchList):



def parseXMLToDataModel(dataModel):
    for field in dataModel["fields"]:
        print("Parsing field:{}".format(field))


def createEntitiesFromFieldValuesDict(field_values_dict, data_model_class):
    keys_list = field_values_dict.keys()
    # logging.debug("keys_list:{}".format(keys_list))
    # logging.debug("last key:{}".format(keys_list[-1]))
    # logging.debug("NUmber of keys:{}".format(len(keys_list)))
    fields_dict = dict((field, 0) for field in field_values_dict.keys())
    # logging.debug("fields_dict:{}".format(fields_dict))
    # logging.debug("field_values_dict:{}".format(field_values_dict))

    createdObjects = []
    
    # while fields_dict[keys_list[0]] < len(field_values_dict[keys_list[0]]):
    # logging.debug("fields_dict:{}".format(fields_dict))
    curr_iterating_field = 0
    while fields_dict[keys_list[curr_iterating_field]] < len(field_values_dict[keys_list[curr_iterating_field]]):
        # logging.debug("fields_dict:{}".format(fields_dict))
        # logging.debug("curr_iterating_field:{}".format(curr_iterating_field))

        if curr_iterating_field < (len(keys_list)-1):
            if fields_dict[keys_list[curr_iterating_field]] >= len(field_values_dict[keys_list[curr_iterating_field]]): 
                #This field is exhausted - should move to level below
                fields_dict[keys_list[curr_iterating_field]] = 0
                curr_iterating_field -=1
                if curr_iterating_field < 0:
                    curr_iterating_field = 0
                fields_dict[keys_list[curr_iterating_field]] +=1
            else:
                curr_iterating_field +=1
            continue
        else:
            i=0 #Iterate on last key
            # logging.debug("creating objects")
            while i < len(field_values_dict[keys_list[-1]]):#Iterate over last key values
                k=0
                objectList = []
                newObj = data_model_class()
                while k<len(keys_list): #Iterate over current key fields
                    # logging.debug("k={}".format(k))
                    # logging.debug("iterating field:{}".format(keys_list[k]))
                    # logging.debug("keys_list[k]:{}".format(keys_list[k]))
                    # logging.debug("fields_dict[k]:{}".format(fields_dict[keys_list[k]]))
                    # logging.debug("   Value:{}".format(field_values_dict[keys_list[k]][fields_dict[keys_list[k]]]))
                    setattr(newObj , 
                            keys_list[k], 
                            field_values_dict[keys_list[k]][fields_dict[keys_list[k]]])
                    objectList.append(
                        (keys_list[k], field_values_dict[keys_list[k]][fields_dict[keys_list[k]]])
                    )
                    k+=1
                # logging.debug("!!              OBJECT!!")
                # logging.debug(objectList)
                createdObjects.append(newObj)

                i+=1
            #Returning to level below
            #!!!!!!!!!!!!!!! TO BE TESTED WITH DATAMODEL WITH JUSt ONE FIELD!!
            curr_iterating_field -=1
            if curr_iterating_field < 0:
                    curr_iterating_field = 0
            fields_dict[keys_list[curr_iterating_field]] +=1 

            # logging.debug("CreatedObjects:{}".format(createdObjects))
    return  createdObjects

#END def createEntitiesFromFieldValuesDict(field_values_dict, data_model_class):



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
        # logging.debug("parsing datamodel:{}".format(dataModel["name"]))

        field_values_dict = {}

        #Create instance of the class
        # dataClass = dataModel["class"]()

        for key_tuple in (dataModel["fields"]):
            key = key_tuple[0]
            xml_path = key_tuple[1]
            # logging.debug( "Parsing for key:"+key)
            # logging.debug( "Key path:"+xml_path)

            field_values_dict[key] = []

            childNodeBranchList = xml_path.replace(" ", "").split('>')

            # keyBranchText = parseXMLKeyBranch(root, childNodeBranchList)
            keyBranchTextArray = parseXMLKeyBranchWithList(root, childNodeBranchList)



            if dataModel["name"] == "<class 'data_models.Study'>" and len(keyBranchTextArray)>1:#This is primary table - we do not need any duplicates - will put a warning to log file
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

            # logging.debug( "childNodeBranchList at the end:"+str(childNodeBranchList))
            
            if len(keyBranchTextArray) > 0:#field found
                keyBranchText = keyBranchTextArray[0]
                # logging.debug("keyBranchText:"+keyBranchText[:30])

                # logging.debug("Number of branch texts found:{}".format(len(keyBranchTextArray)))

                for keyValue in keyBranchTextArray:
                    field_values_dict[key].append(keyValue)

                # setattr(dataClass, key, keyBranchText)
                # print("Key:{}".format(key))
                # print("text:{}".format(keyBranchText))

            else:   #Field not found - putting NONE to datatable
                # logging.debug("keyBranchText IS NONE")
                field_values_dict[key].append("**None**")
                # setattr(dataClass, key, "**None**")
           
            # logging.debug("key values dict:{}".format(field_values_dict))

        #END for key_tuple in dataModel["fields"]:
        entitiesList = createEntitiesFromFieldValuesDict(field_values_dict, dataModel["class"])
        dataObjectsCreated.extend(entitiesList)
        # dataObjectsCreated.append(dataClass)
    #END for dataModel in dataModelsList:

    return dataObjectsCreated

#END def parserXMLNCTFile(fileName, dataModelsList):