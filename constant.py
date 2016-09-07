#!/usr/bin/env python
#
# Copyright 2015-2016 ScaleDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# Configuration file for scaledb
#

#
# Imports
#
# Python imports
# import logging
import yaml_read_write
import yaml_to_cnf
# Project imports


#
# Environments - {docker|linux|juju}]
#
ENV_DOCKER     = "DOCKER"
ENV_LINUX      = "LINUX"
ENV_JUJU       = "JUJU"
ENV_UNDEFINED  = ""


#
# Docker - constants
#
DOCKER_NODE_STATE_BOOTED      =  1
DOCKER_NODE_STATE_STOPPED     =  0
DOCKER_NODE_STATE_UNDEFINED   = -1
DOCKER_INFO_UNDEFINED         = "?"


#
# scaledb-admin.cnf - sections
#
CONFIG_SA_SECTION_NODE = "nodes"
CONFIG_SA_SECTION_SLM  = "slm"
CONFIG_SA_SECTION_CAS  = "cas"

#
# scaledb-admin.cnf - states
#
CONFIG_SA_INFO_UNDEFINED  = "?"
CONFIG_SA_STATE_PRP       = "PRP"
CONFIG_SA_STATE_READY     = "RDY"
CONFIG_SA_STATE_RUN       = "RUN"
CONFIG_SA_STATE_MNT       = "MNT"

CONFIG_SA_CAS_PRIMARY  = "0"
CONFIG_SA_CAS_MIRROR   = "1"

#
# Host server constants
#
SERVER_STATE_RUUNING        =  1
SERVER_STATE_NOT_RESPONDING =  0
SERVER_STATE_UNDEFINED      = -1

SERVER_TIME_OUT             = 5 # seconds, used with the SSH command - ssh -o ServerAliveInterval=SERVER_TIME_OUT

#
# Node constants
#
NODE_STATE_RUNNING   =  1
NODE_STATE_STOPPED   =  0
NODE_STATE_UNDEFINED = -1

#
# Node Type
#
NODE_TYPE_CAS          = "CAS"
NODE_TYPE_SLM          = "SLM"
NODE_TYPE_DB           = "DB"
NODE_TYPE_UNDEFINED    = "?"

NODE_CAS_TYPE_PRIMARY  = "primary"
NODE_CAS_TYPE_MIRROR   = "mirror"

NODE_SLM_TYPE_ACTIVE   = "active"
NODE_SLM_TYPE_STANDBY  = "standby"

NODE_NOT_APPLICABLE    = -1

#
# Cluster constants
#
CLUSTER_MAX_SIZE = 100  # in number of nodes

#
# LOG severities
#
CRITICAL = 50
ERROR	 = 40
WARNING	 = 30
INFO	 = 20
DEBUG	 = 10
NOTSET	 = 0

logSeverity  = {
    'NOTSET'   : 'NOTSET',
    'DEBUG'    : 'DEBUG',
    'INFO'     : 'INFO',
    'WARNING'  : 'WARNING',
    'ERROR'    : 'ERROR',
    'CRITICAL' : 'CRITICAL',
    }

# YAML to CNF constants
# For list sets (such as casDefaultParam): 
#   the left value is the name in the YAML configuration and the right is the corresponding name in *.cnf

#yaml2cnf=yaml_to_cnf.c_convertYAML2ClusterConfig()
yamlFile = "/home/ori/yaml2cnf/yaml-files/ScaleDB-RA_name.yaml"
confDir = "/usr/local/scaledb/etc"

slmDefaultParams = [
    ['ip', 'slm_ip'],
    ['server_port', 'slm_port'],
    ['service_port', 'scaledb_slm_service_port'],
    ['slm_debug_file', 'slm_debug_file']
]
slm_debug_file = '/usr/local/scaledb/tmp/slm.log'

casDefaultParams = [
    ['volume', 'cas_id'],
    ['storage', 'cas_type'],
    ['ip', 'cas_ip'],
    ['server_port', 'cas_port'],
    #other ("less" required) parameters
    ['force_system_key','stream_with_user_time_stamp'],
    ['max_file_size','scaledb_max_file_size'],
    ['file_extent_size','scaledb_file_extent_size'],
    ['cas_data_directory', 'scaledb_data_directory'],
    ['cas_log_directory', 'scaledb_log_directory'],
    ['cas_debug_file', 'scaledb_debug_file'],
    ['disable_varchar', 'scaledb_disable_varchar_check'],
    ['async', 'scaledb_streaming_autocommit'],
    ['cas_recovery_mode', 'scaledb_recovery_mode'],

]
cas_data_directory = '/usr/local/scaledb/data'
cas_log_directory = '/usr/local/scaledb/logs'
cas_debug_directory = '/usr/local/scaledb/tmp/cas.log'

dbDefaultParams = [
    ['name', 'scaledb_node_name'],
    ['service_port','scaledb_service_port'],
    ['db_debug_file', 'scaledb_debug_file'],
    ['scaledb_buffer_size_index', 'scaledb_buffer_size_index'],
    ['scaledb_buffer_size_data', 'scaledb_buffer_size_data'],
    ['scaledb_buffer_size_blob', 'scaledb_buffer_size_blob']
]
db_debug_file = '/usr/local/scaledb/tmp/db.log'

# YAML I/O Parameter
yamlReadWrite = yaml_read_write.c_yamlReadWrite()
