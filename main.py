import logging


# PATH_TO_XML_FILES = r"c:\\Dev\\06. Data\\1. XML from FDA\\03.1 test XML data from FDA\\"
XML_FILE_DIR = "c:\\Dev\\06. Data\\1. XML from FDA\\04. NCT FULL set 20Oct\\"
XML_FILE_DIR = "c:\\Dev\\06. Data\\1. XML from FDA\\03.1 test XML data from FDA\\" 



from sqlalchemy_base import Base,  engine, Session
import sqlalchemy.orm.attributes

from data_models import Study, LocationCountry
from datetime import date

import os

from xml_parsing_routines import parserXMLNCTFile


def parseXMLFilesInDir(fileDirPath, totalFileNumberInDir, tables_writers_list, session):
        fileCounter = 0
        objects_created = []
        for dirName, subdirList, fileList in os.walk(fileDirPath):
                print('Found directory: %s' % dirName)
                for fname in fileList:
                #     print(colorama.ansi.clear_screen())
                        fileCounter +=1
                        print("DIR:"+dirName)
                        print("  FILE:"+fname)
                        # print('\t\t\t\t\t%s' % fname)
                        logging.debug(dirName)
                        logging.debug('\t\t\t\t\t%s' % fname)
                        print("\n\nCurrent file number:%i of %i  (%2.1f %%)"%(fileCounter,
                                                totalFileNumberInDir,
                                                (fileCounter*100/totalFileNumberInDir)))
                        logging.debug("Current file number:%i"%(fileCounter))
                        # print("\t\t Total number of files:%i"%(totalFileNumberInDir))
                        objs_created = parserXMLNCTFile(dirName+"\\\\"+fname,
                                                tables_writers_list)
                        # print("Objs created:{}".format(objs_created))
                        print("Number of objs created:{}".format(len(objs_created)))
                        objects_created.extend(objs_created)
                        if len(objects_created) > 800:
                                for obj in objects_created:
                                        session.add(obj)
                                del objects_created[:]
                        session.commit()
        return None
#END def parseXMLFilesInDir(fileDirPath, totalFileNumberInDir, tables_writers_list):    

import datetime

from parse_data_models_routines import parseDataModels

if __name__ == "__main__":
        curr_time_str = datetime.datetime.now().strftime("%d-%b-%Y")
        logging.basicConfig(filename=curr_time_str+'.log',level=logging.DEBUG)
        logging.debug('This message should go to the log file')

       

        print("Everything is OK. Finished.")

        models_list = parseDataModels([Study, LocationCountry])

        print(models_list)

        

        # 2 - generate database schema
        Base.metadata.create_all(engine)

        # 3 - create a new session
        session = Session()


        # new_study = Study()

        # 

        # session.add(new_study)

        created_objects = parseXMLFilesInDir(XML_FILE_DIR, 1000, models_list, session)

       

        # 10 - commit and close session
        session.commit()
        session.close()
