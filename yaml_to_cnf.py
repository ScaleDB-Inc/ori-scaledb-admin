"""
Date: August 2016
Author: Ori Shadmon
Project: ScaleDB-Admin

Description: Using the YAML file the script can generate corresponding cnf files. For all the files that are not,
    cluster.cnf, the script also puts them in appropriate sub-directories, under the used config directory. Since we
    the script utilizes the YAML file, there is no "human" intervention needed, unless the location of the YAML or cnf
    files changes.

The script also has a"main" like component called "select_sub_process"
"""

import constant
import os
import yaml

class c_convertYAML2ClusterConfig:
    #
    # initiate script
    # Status: 0
    #
    def __init__(self, yamlFile="",confDir=""):
        self.status=0
        if yamlFile is "" and confDir is "":
            pass
        else:
            self.__get_value(yamlFile,confDir)
        self.status = self.read_yaml()

    #
    # return 0 or 1 if status is ok
    #   test is run in "main" after initiate
    #
    def status_check(self):
        return self.status

    #
    # Set YAML File and location of CNF (if not default)
    # Status: >0 - question regarding premissions for /usr/local/scaledb/etc/cluster
    '''
    due to permissions I'm currently unable to add/alter files inside '/usr/local/scaledb/etc/cluster';
    as such I tested against '/home/ori/cluster/', and found the method working. If this will change
    then the given script should work. However, if not then I would be adding another method that
    copies the data from a tmp directory ['/home/scaledb/tmp/cluster/'] to the active directory.
    '''
    #
    def __get_value(self, yamlFile,confDir):
        status = 0
        if yamlFile is not "":
            if os.path.exists(yamlFile) is False:
                status+=1
            else:
                constant.yamlFile = yamlFile
        if confDir is not "":
            if os.path.exists(confDir) is False:
                status+=1
            else:
                constant.confDir = confDir
        return status

    #
    # Retrieve data from YAML file
    # Status: 0
    #
    def read_yaml(self):
        status = 0
        with open(constant.yamlFile, 'r') as stream:
            try:
                self.yamlData = yaml.load(stream)
            except yaml.YAMLError as e:
                print e
                return 1
        return status

    #
    # create cnf directory if not exists
    # Note: there is no need to put base directory since it is stored under self.confDir
    #
    def create_directory(self,dirName):
        status = 0
        dName = "%s/%s" % (constant.confDir, dirName)

        try:
            os.path.isdir(dName)
        except OSError as e:
            print e
            return 1

        if not os.path.isdir(dName):
            try:
                os.system("mkdir %s " % dName)
            except OSError as e:
                status = 1
                print e
        return status

    #
    # open cnf files if not exists, and open to run
    # Note: there is no need to put base directory since it is stored under self.confDir
    # Status 0
    #
    def create_write_cnf(self,dirName,fileName):
        status = 0
        dName = "%s/%s" % (constant.confDir, dirName)
        if not os.path.isdir(dName):
            status = self.create_directory(dirName)
        fName = "%s/%s" % (dName, fileName)
        if not os.path.isfile(fName):
            try:
                os.system("touch %s" % fName)
            except OSError as e:
                print e
                return 1
        open(fName,'w').close()
        return status,open(fName,'w')

    #
    # create cluster.cnf
    #   dataValues = self.yamlData['clusters'][0]
    #   paramName = groups of self.yamlData['clusters'][0]
    # Status: 0 - Other than question this part is DONE
    # Status: >0 - Question in how cluster.cnf should look
    #
    # Question:
    '''
    There is a substantial difference between a test user cluster.cnf and the wiki version of cluster.cnf.
    Which one should my output look like? (As of now it is the same as the wiki version"
    '''
    #
    def cluster_cnf_create(self, dataValues):
        status = 0
        status,f=self.create_write_cnf("","cluster.cnf")
        if status == 0:
            for paramName in dataValues['cas']:
                f.write("CAS = " + str(paramName['ip'])+"\n")
                self.create_directory(str(paramName['ip']))
            for paramName in dataValues['slm']:
                f.write("SLM = " + str(paramName['ip'])+"\n")
                self.create_directory(str(paramName['ip']))
            for paramName in dataValues['db']:
                f.write("DB = " + str(paramName['ip'])+"\n")
                self.create_directory(str(paramName['ip']))
        f.close()
        return status

    #
    # create cluster.cnf
    #   dataValues = self.yamlData['clusters'][0]['cas']
    #   casSet = group of dataValues
    #   casParam specific key from casDefaultParams
    # If the yaml files does not contain required data/log/debug params then we use the defaults
    # Status: 0
    #
    def cas_cnf_create(self,dataValues):
        status = 0
        for casSet in dataValues:
            new_line=''
            status,f=self.create_write_cnf(casSet['ip'],"cas.cnf")
            if status == 0:
                for casParam in constant.casDefaultParams:
                    if casParam[0] in casSet.keys():
                        if casParam[0] is "storage" and casSet[casParam[0]] == 0:
                            f.write(new_line+casParam[1]+" = primary")
                        elif casParam[0] is "storage" and casSet[casParam[0]] == 1:
                            f.write(new_line+casParam[1]+" = mirror")
                        else:
                            f.write(new_line+casParam[1] + " = "+str(casSet[casParam[0]]))

                        if new_line == '':
                            new_line="\n"

                self.cas_hostPort_create(f)
                for casParam in constant.casDefaultParams:
                    if "data_directory" in casParam[0]:
                        f.write(new_line+casParam[1]+" = "+constant.cas_data_directory)
                    elif "log_directory" in casParam[0]:
                        f.write(new_line+casParam[1]+" = "+constant.cas_log_directory)
                    elif "file" in casParam[0]:
                        f.write(new_line+casParam[1]+" = "+constant.cas_debug_directory)
            f.close()
            return status

    #
    # specify the grouping of CAS Host and port for cas.cnf
    # Status: 0
    #
    def cas_hostPort_create(self,f):
        primary_ips = ''
        primary_ports = ''
        mirror_ports = ''
        mirror_ips = ''

        for casSet in self.yamlData['clusters'][0]['cas']:
            if casSet['storage'] == 0 and primary_ips is '':
                primary_ips = casSet['ip']
                primary_ports = str(casSet['server_port'])

            elif casSet['storage'] == 0 and primary_ips is not '':
                primary_ips = primary_ips+","+casSet['ip']
                primary_ports = primary_ports+","+str(casSet['server_port'])

            elif casSet['storage'] == 1 and mirror_ips is '':
                mirror_ips = casSet['ip']
                mirror_ports = str(casSet['server_port'])
            else:
                mirror_ips = mirror_ips+","+str(casSet['ip'])
                mirror_ports = mirror_ports+","+str(casSet['server_port'])

        f.write("\n\nscaledb_cas_server_ips = "+primary_ips)
        f.write("\nscaledb_cas_server_ports = "+primary_ports)
        f.write("\nscaledb_cas_mirror_ips = " + mirror_ips)
        f.write("\nscaledb_cas_mirror_ports = " + mirror_ports+"\n")


    #
    # create db.cnf
    #   dataValues = self.yamlData['clusters'][0]['db']
    #   dbSet = dict group inside dataValue
    #   dbParam = specific key from dbSet
    # If the yaml files does not contain required data/log/debug params then we use the defaults
    # Status: 0
    #
    def db_cnf_create(self, dataValues):
        status=0
        for dbSet in dataValues:
            new_line=""
            status,f=self.create_write_cnf(dbSet['ip'],"db.cnf")
            if status == 0:
                for dbParam in constant.dbDefaultParams:
                    if dbParam[0] in dbSet.keys():
                        f.write(new_line+dbParam[1]+" = "+dbSet[dbParam[0]])
                    if new_line is "":
                        new_line="\n"
                self.cas_other_config(f)
                for dbParam in constant.dbDefaultParams:
                    if "file" in dbParam[0]:
                        f.write(new_line+dbParam[1]+" = "+constant.db_debug_file)
            f.close()
        return status

    #
    # create slm.cnf
    #   dataValues = self.yamlData['clusters'][0]['slm']
    #   slmSet = dict group inside dataValues
    #   slmParam = specific key from slmSet
    # If the yaml files does not contain required data/log/debug params then we use the defaults
    # Status: 0
    #
    def slm_cnf_create(self, dataValues):
        status=0
        for slmSet in dataValues:
            status,f=self.create_write_cnf(slmSet['ip'],"slm.cnf")
            if status == 0:
                new_line=""
                for slmParam in constant.slmDefaultParams:
                    if slmParam[0] in slmSet.keys():
                        f.write(new_line+ slmParam[1] + " = " + str(slmSet[slmParam[0]]))
                    if new_line is "":
                        new_line="\n"
                self.cas_other_config(f)
                for slmParam in constant.slmDefaultParams:
                    if "file" in slmParam[0]:
                        f.write(new_line+slmParam[1]+" = "+constant.slm_debug_file)
            f.close()
            return status
    #
    # specify scaledb_cas_config_ips and scaledb_cas_config_ports for slm.cnf and db.cnf
    # Status:0
    #
    def cas_other_config(self,f):
        ips = ''
        ports = ''
        for casSet in self.yamlData['clusters'][0]['cas']:
            if casSet['volume'] == 0:
                if ips is '':
                    ips = casSet['ip']
                    ports = str(casSet['server_port'])
                else:
                    ips = ips+','+casSet['ip']
                    ports = ports+','+str(casSet['server_port'])
        f.write("\n\nscaledb_cas_config_ips = " + ips)
        f.write("\nscaledb_cas_config_ports = " + ports+"\n")

    #
    # distinguish which file to use based on key
    # Status : 0
    #
    def select_sub_process(self):
        status = 0
        for key in self.yamlData['clusters'][0].keys():
            if key == 'cluster':
                status = self.cluster_cnf_create(self.yamlData['clusters'][0])
                if status == 1:
                    return status
            elif key == 'cas':
                status = self.cas_cnf_create(self.yamlData['clusters'][0]['cas'])
                if status == 1:
                    return status
            elif key == 'slm':
                status = self.slm_cnf_create(self.yamlData['clusters'][0]['slm'])
                if status == 1:
                    return status
            elif key == 'db':
                status = self.db_cnf_create(self.yamlData['clusters'][0]['db'])
                if status == 1:
                    return status


#
