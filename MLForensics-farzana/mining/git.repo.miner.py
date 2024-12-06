'''
Akond Rahman 
Nov 19, 2020 
Mine Git-based repos 
'''


import pandas as pd 
import csv 
import subprocess
import numpy as np
import shutil
from git import Repo
from git import exc 
from xml.dom import minidom
from xml.parsers.expat import ExpatError
import time 
import  datetime 
import os 
import logging

logger = None
def giveMeLoggingObject():
    global logger
    if logger == None:
        format_str = '%(asctime)s:%(message)s'
        file_name  = 'LOGGER.log'
        logging.basicConfig(format=format_str, filename=file_name, level=logging.INFO)
        logger = logging.getLogger('simple-logger')
    return logger

def deleteRepo(dirName, type_):
    print(':::' + type_ + ':::Deleting ', dirName)
    logger.info(':::' + type_ + ':::Deleting ', dirName)
    try:
        if os.path.exists(dirName):
            shutil.rmtree(dirName)
            logger.info(f"{dirName} deleted")
    except OSError:
        print('Failed deleting, will try manually')
        logger.info('Failed deleting, will try manually')


def makeChunks(the_list, size_):
    for i in range(0, len(the_list), size_):
        yield the_list[i:i+size_]

def cloneRepo(repo_name, target_dir):
    cmd_ = "git clone " + repo_name + " " + target_dir
    logger.info(f"cloning {repo_name} to {target_dir}")
    try:
       subprocess.check_output(['bash','-c', cmd_])
       logger.info("repo cloned")
    except subprocess.CalledProcessError:
       print('Skipping this repo ... trouble cloning repo:', repo_name )
       logger.info('Skipping this repo ... trouble cloning repo:', repo_name )

def dumpContentIntoFile(strP, fileP):
    logger.info(f"dumping {strP} into {fileP}")
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()
    logger.info("dumped")
    return str(os.stat(fileP).st_size)

def getPythonCount(path2dir): 
    usageCount = 0
    for root_, dirnames, filenames in os.walk(path2dir):
        for file_ in filenames:
            full_path_file = os.path.join(root_, file_) 
            if (file_.endswith('py') ):
                usageCount +=  1 
    return usageCount                         


def cloneRepos(repo_list): 
    counter = 0     
    str_ = ''
    for repo_batch in repo_list:
        for repo_ in repo_batch:
            counter += 1 
            print('Cloning ', repo_ )
            dirName = '/Users/arahman/FSE2021_ML_REPOS/GITHUB_REPOS/' + repo_.split('/')[-2] + '@' + repo_.split('/')[-1] 
            cloneRepo(repo_, dirName )
            ### get file count 
            all_fil_cnt = sum([len(files) for r_, d_, files in os.walk(dirName)])
            if (all_fil_cnt <= 0):
               deleteRepo(dirName, 'NO_FILES')
            else: 
               py_file_count = getPythonCount( dirName  )
               prop_py = float(py_file_count) / float(all_fil_cnt)
               if(prop_py < 0.25):
                   deleteRepo(dirName, 'LOW_PYTHON_' + str( round(prop_py, 5) ) )
            print("So far we have processed {} repos".format(counter) )
            if((counter % 10) == 0):
                dumpContentIntoFile(str_, 'tracker_completed_repos.csv')
            elif((counter % 100) == 0):
                print(str_)                
            print('#'*100)

def getMLStats(repo_path):
    repo_statLs = []
    repo_count  = 0 
    all_repos = [f.path for f in os.scandir(repo_path) if f.is_dir()]
    print('REPO_COUNT:', len(all_repos) )
    logger.info(f"getMLStats REPO_COUNT = {len(all_repos)}")
    for repo_ in all_repos:
        repo_count += 1 
        ml_lib_cnt = getMLLibraryUsage( repo_ ) 
        repo_statLs.append( (repo_, ml_lib_cnt ) )
        print(repo_count, ml_lib_cnt)
    return repo_statLs 


def getMLLibraryUsage(path2dir): 
    usageCount  = 0 
    for root_, dirnames, filenames in os.walk(path2dir):
        for file_ in filenames:
            full_path_file = os.path.join(root_, file_) 
            if(os.path.exists(full_path_file)):
                if (file_.endswith('py'))  :
                    f = open(full_path_file, 'r', encoding='latin-1')
                    fileContent  = f.read()
                    fileContent  = fileContent.split('\n') 
                    fileContents = [z_.lower() for z_ in fileContent if z_!='\n' ]
                    # print(fileContent) 
                    for fileContent in fileContents:
                        if('sklearn' in fileContent) or ('keras' in fileContent) or ('gym.' in fileContent) or ('pyqlearning' in fileContent) or ('tensorflow' in fileContent) or ('torch' in fileContent):
                                usageCount = usageCount + 1
                        elif('rl_coach' in fileContent) or ('tensorforce' in fileContent) or ('stable_baselines' in fileContent) or ('tf.' in fileContent) :
                                usageCount = usageCount + 1
                        # elif('rl_coach' in fileContent) or ('tensorforce' in fileContent) or ('stable_baselines' in fileContent) or ('keras' in fileContent) or ('tf' in fileContent):
                        #         usageCount = usageCount + 1
    return usageCount      


def deleteRepos():
    repos_df = pd.read_csv('DELETE_CANDIDATES_GITHUB_V2.csv')
    repos    = np.unique( repos_df['REPO'].tolist() ) 
    for x_ in repos:
        deleteRepo( x_, 'ML_LIBRARY_THRESHOLD' )
        logger.info(f"deleted repo {x_}")

if __name__=='__main__':
    # repos_df = pd.read_csv('PARTIAL_REMAINING_GITHUB.csv')
    # list_    = repos_df['URL'].tolist()
    # list_    = np.unique(list_)
    # # print('Repos to download:', len(list_)) 
    # ## need to create chunks as too many repos 
    # chunked_list = list(makeChunks(list_, 100))  ### list of lists, at each batch download 100 repos 
    # cloneRepos(chunked_list)
    giveMeLoggingObject()



    '''
    some utils  

    deleteRepos()     

    di_ = '/Users/arahman/FSE2021_ML_REPOS/GITHUB_REPOS/'
    ls_ = getMLStats(  di_  )
    df_ = pd.DataFrame( ls_ )
    df_.to_csv('LIB_BREAKDOWN_GITHUB_BATCH2.csv', header=['REPO', 'LIB_COUNT'] , index=False, encoding='utf-8')              
    '''


