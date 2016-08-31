"""
Date: August 2016
Author: Ori Shadmon
Project: ScaleDB-Admin

Description: The following code allows users to communicate between the scaledb-admin.py script and tha YAML file.
Using this script, the scaledb-admin has the option of retrieving both general, and specific infromation from YAML file.
In addition it also has the option of updating information in the YAML file.

Over all the class is divided into either nodes (CAS,SLM,db) or non-nodes (ie general cluster descriptors).
    If working against a node then the script uses a corresponding node ID to drill down on which node
      to work against.

Each type has the option of:
- adding new information to the YAML file
- removing information from the YAML file
- update information in the YAML file
- check information in the YAML file

*Note for non-node related information the adding and updating cluster information is the same function

"""

import constant
import os
import yaml

class c_yamlReadWrite:

    #
    # initiate script
    # Status: 0
    #
    def __init__(self, yamlFile=""):
        self.status=0
        if yamlFile is not "":
            self.__get_value(yamlFile)
        self.status=self.read_yaml_file()

    #
    # check status
    #
    def status_check(self):
        return self.status

    #
    # set user defined YAML file
    #
    def __get_value(self, yamlFile):
        status=0
        if os.path.exists(yamlFile) is False:
            status+=1
        else:
            constant.yamlFile=yamlFile
        return status

    #
    # store yaml into dictionary for reading
    #
    def read_yaml_file(self):
        status=0
        with open(constant.yamlFile,'r') as stream:
            try:
                self.yamlData=yaml.load(stream)
            except yaml.YAMLError as e:
                print e
                status=1
        stream.close()
        return status

    #
    # write to yaml file
    #
    def write_yaml_file(self):
        status=0
        with open(constant.yamlFile,'w') as stream:
            try:
                yaml.dump(self.yamlData,stream)
            except yaml.YAMLError as e:
                print e
                status=1
            stream.close()
            return status

    #
    # read information about a non-node related parameters
    #   id
    #   name
    #   description
    #   environment
    #
    def read_yaml_param(self,key=""):
        status = 0
        if key not in self.yamlData['clusters'][0].keys():
            status=1
            return "", status
        return self.yamlData['clusters'][0][key], status

    #
    # remove information about non-node related parameters
    #   id
    #   name
    #   description
    #   environment
    #
    def remove_yaml_param(self,key):
        status=0
        if key not in self.yamlData['clusters'][0].keys():
            status=1
        del self.yamlData['clusters'][0][key]
        status=self.write_yaml_file()

    #
    # update/add non-node related values
    #   id
    #   name
    #   description
    #   environment
    #
    def write_yaml_param(self,key,value=""):
        status=0
        self.yamlData['clusters'][0][key]=value
        status=self.write_yaml_file()
        return status


    #
    # restive information about node(s)
    # if an ID is specified then it returns all all corresponding node(s) with the given ID
    #   cas
    #   slm
    #   db
    #
    def read_yaml_node_param(self,key,id=-1):
        status=1
        output=[]
        for node in self.yamlData['clusters'][0][key]:
            if id == -1:
                output.append(node)
                status=0
            else:
                if node['id'] == id:
                    output.append(node)
                    status=0
        return output,status

    #
    # remove a node from the yaml file
    #   cas
    #   slm
    #   db
    #
    def remove_yaml_node(self,key,id=-1):
        status=1
        for node in self.yamlData['clusters'][0][key]:
            if node['id'] == id:
                del self.yamlData['clusters'][0][key][self.yamlData['clusters'][0][key].index(node)]
                status = 0
        status=self.write_yaml_file()
        return status


    #
    # add a new node to the yaml file
    #   cas
    #   slm
    #   db
    #
    def add_yaml_node(self,key,newNode=None):
        status=0
        error=""
        # if newNode is empty then stop
        if newNode is None:
            status=1
            return status

        # if newNode already exists then stop
        for node in self.yamlData['clusters'][0][key]:
            if node["id"] == newNode["id"]:
                error+="ERROR: Identical Node ID\n"
                status+=1
            if node["name"] == newNode["name"]:
                error+="ERROR: Identical Node Name\n"
                status+=1
            if node["ip"] == newNode["ip"]:
                if node["server_port"] == newNode["server_port"]:
                    error+="ERROR: Identical Server Port\n"
                    status+=1
                if node["service_port"] == newNode["service_port"]:
                    error+="ERROR: Identical Service Port\n"
                    status+=1

        #if node doesn't already exist and the new node doesn't create conflict then create
        if status == 0:
            self.yamlData['clusters'][0][key].append(newNode)
            status=self.write_yaml_file()
        print error
        return status

    #
    # update a information regarding a specific node
    #   cas
    #   slm
    #   db
    #
    def update_yaml_node(self,key,id,param,new_vale):
        status=1
        for node in self.yamlData['clusters'][0][key]:
            if node["id"] == id:
                node[param] = new_vale
                status=0
        status=self.write_yaml_file()
        return status

    #
    # Get information about about - If the id=-1 then it shows information about all corresponding nodes
    #                               If the param is not empty then it returns only information about param
    #   cas
    #   slm
    #   db
    #
    def read_yaml_node(self,key,id=-1,nodeParam=""):
        status=1
        output=[]
        if key is "":
            return output, status
        for node in self.yamlData['clusters'][0][key]:
            if id == -1:
                output.append(node)
                status=0
            else:
                if node["id"] == id and param is not "":
                    output.append(node[param])
                    status=0
                elif node["id"] == id and param is "":
                    output.append(node)
                    status=0
                else:
                    pass

        return output,status





