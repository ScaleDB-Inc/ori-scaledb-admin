"""
Date: August 2016
Author: Ori Shadmon
Project: ScaleDB-Admin

Description: The following are the methods for utilizing the code I wrote for read/write against YAML file.
The functions bellow are based on SDB-245 (https://scaledb.atlassian.net/browse/SDB-245), and are intended to replace
the ones in scaledb-admin.
"""
import constant
import yaml_to_cnf
import yaml_read_write

#
# Ori - update the location of the YAML file and conf directory
# This is necessary to call only when wanting to update either parameter.
# The actual call to the the classes is stored in constant.py deceleration
#
def yamlFile_confDir_deceleration(yamlFile="", confDir=""):
    status = 0
    constant.yaml2cnf = yaml_to_cnf.c_convertYAML2ClusterConfig(yamlFile, confDir)
    if constant.yaml2cnf.status_check() != 0:
        status += constant.yaml2cnf.status_check()
    constant.yamlReadWrite = yaml_read_write.c_yamlReadWrite(yamlFile)
    if constant.yamlReadWrite.status_check() != 0:
        status += constant.yamlReadWrite.status_check()
    return status


#
# Ori - retrieve information regarding environment
#
def yaml_environment_retrieve():
    status = 0
    environment = ""
    if constant.yamlReadWrite.status_check() != 0:
        status = constant.yamlReadWrite.status_check()
    else:
        environment, status = constant.yamlReadWrite.read_yaml_param("Environment")
    return environment, status


#
# Ori - set environment information
#
def yaml_environment_set(environment):
    if constant.yamlReadWrite.status_check() != 0:
        status = constant.yamlReadWrite.status_check()
    else:
        environment, status = constant.yamlReadWrite.write_yaml_param("Environment", environment)
    return environment, status


#
# Ori - generate the configuration sub-directories and files
#
def yaml_cluster_conf_update(yamlFile="", confDir=""):
    status = 0
    if constant.yaml2cnf.check_status() == 1:
        status = constant.yaml2cnf.check_status()
    else:
        status = constant.yaml2cnf.select_sub_process()
    return status


#
# Ori - adding a new node to the yaml file
#	To add a new node state the type of node (CAS/SLM/db) and corresponding parameters
#		as if they are in a dictionary
# Example: {description: Database node 0, id: 0, ip: 192.168.0.11, name: db0, node: null, server_port: 3306, service_port: 33307}
#
def yaml_node_info_add(nodeType="", nodeParams=None):
    status = 0
    if constant.yamlReadWrite.check_status != 0:
        status = constant.yamlReadWrite.check_status()
    else:
        status = constant.yamlReadWrite.add_yaml_node(nodeType, nodeParams)
    return status


#
# Ori - removing a node based on type and specified ID in the YAML file
#
def yaml_remove_node(nodeType="", nodeID=-1)
    status = 0
    if constant.yamlReadWrite.check_status() != 0:
        status += constant.yamlReadWrite.check_status()
    else:
        status = constant.yamlReadWrite.remove_yaml_node(nodeType)
    return status


#
# Ori - Retrieve node information
#
def node_info_retrieve(nodeType="", nodeID=-1, nodeParam=""):
    status = 0
    output=None
    if constant.yamlReadWrite.check_status() != 0:
        status += constant.yamlReadWrite.check_status()
    else:
        output, status = constant.yamlReadWrite.read_yaml_node(nodeType, nodeID, nodeParam)
    """
    right now I'm printing the result set from read_yaml_node, but could change it
    to behave in different ways, depending on type/size
    """
    for value in output:
        print value + "\n"
    return status
