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


class c_convertYAML2CNF:
    #
    # initiate script
    # Status: 0
    #
    def __init__(self, yaml="",conf=""):
        self.status=0
        if yaml is "" and conf is "":
            pass
        else:
            self.status=self.__get_value(yaml,conf)
        self.status=self.read_yaml()

    #
    # return 0 or 1 if status is ok
    #   test is run in "main" after initiate
    #
    def status_check(self):
        return self.status

    #
    # Set YAML File and location of CNF (if not default)
    # Status: >0 - question regarding permissions for /usr/local/scaledb/etc/cluster
    '''
    due to permissions I'm currently unable to add/alter files inside '/usr/local/scaledb/etc/cluster';
    as such I tested against '/home/ori/cluster/', and found the method working. If this will change
    then the given script should work. However, if not then I would be adding another method that
    copies the data from a tmp directory ['/home/scaledb/tmp/cluster/'] to the active directory.
    '''
    #
    def __get_value(self, yaml,conf):
        status=1
        if yaml is not "":
            if os.path.exists(yaml) is True:
                constant.yamlFile=yaml
                status=0
        if conf is not "":
            if os.path.exists(conf) is True:
                constant.confDir=conf
                status=0
        return status

    #
    # Retrieve data from YAML file
    # Status: 0
    #
    def read_yaml(self):
        status=0
        with open(constant.yamlFile, 'r') as stream:
            try:
                self.yamlData = yaml.load(stream)
            except yaml.YAMLError as e:
                print e
                status=1
        stream.close()
        return status

    #
    # open conf files to write
    # Status 0
    #
    def write_to_conf(self,dirName,fileName):
        dName = "%s/%s" % (constant.confDir, dirName)
        if not os.path.isdir(dName):
            os.system("mkdir %s " % dName)

        fName = "%s/%s" % (dName, fileName)
        if not os.path.isfile(fName):
            os.system("touch %s" % fName)
        open(fName,'w').close()
        return open(fName,'w')

    #
    # create cluster.conf
    #   dataValues = self.yamlData['clusters'][0]
    #   paramName = groups of self.yamlData['clusters'][0]
    # Status: 0 - Other than question this part is DONE
    # Status: >0 - Question in how cluster.conf should look
    #
    # Question:
    '''
    There is a substantial difference between a test user cluster.conf and the wiki version of cluster.conf.
    Which one should my output look like? (As of now it is the same as the wiki version"
    '''
    #
    def cluster_conf_create(self, dataValues):
        self.casIP=[]
        self.slmIP=[]
        self.dbIP=[]
        f=self.write_to_conf("","cluster.cnf")
        for paramName in dataValues['cas']:
            f.write("CAS = " + str(paramName['ip'])+"\n")
            self.casIP.append(paramName['ip'])
        for paramName in dataValues['slm']:
            f.write("SLM = " + str(paramName['ip'])+"\n")
            self.slmIP.append(paramName['ip'])
        for paramName in dataValues['db']:
            f.write("DB = " + str(paramName['ip'])+"\n")
            self.dbIP.append(paramName['ip'])
        f.close()

    #
    # create cluster.conf
    #   dataValues = self.yamlData['clusters'][0]['cas']
    #   casSet = group of dataValues
    #   casParam specific key from casDefaultParams
    # If the yaml files does not contain required data/log/debug params then we use the defaults
    # Status: 0
    #
    def cas_conf_create(self,dataValues):
        for casSet in dataValues:
            new_line=''
            f=self.write_to_conf(casSet['ip'],"cas.cnf")
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

    #
    # specify the grouping of CAS Host and port for cas.conf
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
    # create db.conf
    #   dataValues = self.yamlData['clusters'][0]['db']
    #   dbSet = dict group inside dataValue
    #   dbParam = specific key from dbSet
    # If the yaml files does not contain required data/log/debug params then we use the defaults
    # Status: 0
    #
    def db_conf_create(self, dataValues):
        for dbSet in dataValues:
            new_line=""
            f=self.write_to_conf(dbSet['ip'],"db.cnf")
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

    #
    # create slm.conf
    #   dataValues = self.yamlData['clusters'][0]['slm']
    #   slmSet = dict group inside dataValues
    #   slmParam = specific key from slmSet
    # If the yaml files does not contain required data/log/debug params then we use the defaults
    # Status: 0
    #
    def slm_conf_create(self, dataValues):
        for slmSet in dataValues:
            f=self.write_to_conf(slmSet['ip'],"slm.cnf")
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

    #
    # specify scaledb_cas_config_ips and scaledb_cas_config_ports for slm.conf and db.conf
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
    # check that the creation of the files and subdirectories was successful
    #
    def create_file_check(self):
        status=0
        error="Errors: "
        errors=error
        #check cluster.cnf
        if os.path.exists(constant.confDir+"/cluster.cnf") is False:
            status+=1
            errors+="\n\t%s/cluster.cnf does not exists" % constant.confDir

        #check cas.cnf
        for ip in self.casIP:
            dir=("%s/%s" % (constant.confDir, ip))
            file=("%s/%s/cas.cnf" % (constant.confDir, ip))
            if os.path.exists(dir) is False:
                status+=1
                errors+="\n\t%s directory was not created" % dir
            elif os.path.exists(file) is False:
                status+=1
                errors+="\n\t%s file was not created" % file

        #check slm.cnf
        for ip in self.slmIP:
            dir=("%s/%s" % (constant.confDir, ip))
            file=("%s/%s/slm.cnf" % (constant.confDir, ip))
            if os.path.exists(dir) is False:
                status+=1
                errors+="\n\t%s directory was not created" % dir
            elif os.path.exists(file) is False:
                status+=1
                errors+="\n\t%s file was not created" % file

        #check db.cnf
        for ip in self.dbIP:
            dir=("%s/%s" % (constant.confDir, ip))
            file=("%s/%s/db.cnf" % (constant.confDir, ip))
            if os.path.exists(dir) is False:
                status+=1
                errors+="\n\t%s directory was not created" % dir
            elif os.path.exists(file) is False:
                status+=1
                errors+="\n\t%s file was not created" % file

        if errors is error:
            pass
        else:
            print errors
        return status




    #
    # distinguish which file to use based on key
    # Status : 0
    #
    def select_sub_process(self):
        status=0
        for key in self.yamlData['clusters'][0].keys():
            if key == 'cluster':
                self.cluster_conf_create(self.yamlData['clusters'][0])
            elif key == 'cas':
                self.cas_conf_create(self.yamlData['clusters'][0]['cas'])
            elif key == 'slm':
                self.slm_conf_create(self.yamlData['clusters'][0]['slm'])
            elif key == 'db':
                self.db_conf_create(self.yamlData['clusters'][0]['db'])
        status=self.create_file_check()
        return status 
'''
if __name__ == "__main__":
    convYAML2CNF = c_convertYAML2CNF(yaml="ScaleDB-ONE_name.yaml",conf="conf")
    convYAML2CNF.select_sub_process()
'''
