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
# Imports
#
# Python imports
import logging

# Project imports

#
# Program configurations
#
PRG_TEXT        = ", for Linux (x86_64)"
PRG_COMPANY     = "Copyright (c) 2016, ScaleDB, Inc."


#
# Input parameters handling
#
MAX_INPUT_PARAM      =   20



#
# Scaledb configurations
#
SCALEDB_USER          = 'scaledb'
SCALEDB_HOME          = '/usr/local/scaledb'
SCALEDB_CUSTER        = SCALEDB_HOME + "/scripts/scaledb-cluster"

#SCALEDB_ADMIN_HOME   = SCALEDB_HOME + "/scripts/scaledb-admin"
SCALEDB_ADMIN_HOME    = "."
SCALEDB_ADMIN_CMD     = "python  "   + SCALEDB_ADMIN_HOME + "/scaledb-admin.py "


TEMPLATE_CAS   = SCALEDB_HOME + "/etc/templates/cas.cnf"
TEMPLATE_DB    = SCALEDB_HOME + "/etc/templates/scaledb.cnf"
TEMPLATE_SLM   = SCALEDB_HOME + "/etc/templates/slm.cnf"

CLUSTER_DIRECTORY_STRUCTURE   = SCALEDB_HOME + "/etc/cluster"
CLUSTER_CONFIG                = SCALEDB_HOME + "/etc/cluster.cnf"
SCALEDB_CONFIG                = SCALEDB_HOME + "/etc/scaledb-admin.cnf"

#
# scaledb-configuration
#
SDBADM_VOLUME_ENABLE           = True   # True = container using volumes
SDBADM_CONTAINER_ENABLE        = True   # True = scaledb-admin executed in the container, False = scaledb-admin executed in the server


#
# MariaDb configurations
#
MARIADB_HOME    = ' /usr/local/mysql'
MARIADB_SERVICE = MARIADB_HOME + "/support-files/mysql.server"


#
# PORTS
#
SCALEDB_CAS_SERVER_PORTS         = "13306"
SCALEDB_CAS_MIRROR_PORTS         = "13306"
SCALEDB_CAS_SERVER_SERVICE_PORTS = "13307"
SCALEDB_CAS_MIRROR_SERVICE_PORTS = "13307"

SCALEDB_SLM_PORT                 = "23306"
SCALEDB_SLM_PORT_SERVICE         = "23307"

SCALEDB_DB_PORT_SERVICE          = "33307"


#
# Log configurations
#
LOG_MESSAGE_FORMAT = '%(asctime)s - [%(levelname)s] - (%(threadName)-10s) - %(message)s'
LOG_SEVERITY_LEVEL = logging.DEBUG

#
# Ssh configurations
#
SSH_CMD           = " ssh     "
SSH_CMD_SCP       = " scp -rp "
SSH_CMD_MKDIR     = " mkdir -p "
SSH_USER          = "scaledb"
SSH_ALIVE_MESSAGE = "alive"



#
# rsync command/options
#

RSYNC_CMD           = " rsync --archive --verbose --recursive --compress --human-readable --progress --partial  --partial-dir=.rsync-partial --delete  "
RSYNC_RETRY_COUNT   = 3
RSYNC_RETRY_SLEEP   = 30  # seconds

#
# timeout command/options
#
CMD_TIMEOUT          = " timeout --signal=9  "
CMD_TIMEOUT_STD      =  120
CMD_TIMEOUT_FAST     =   15


#
# Docker configuration
#
DOCKER_USER                  = "scaledb"
DOCKER_SSH_CMD               = "ssh "
DOCKER_CONTAINERID_SHORT_LEN = 12

DOCKER_DIR_SCALEDB           = "/usr/local/docker-scaledb"
#DOCKER_DIR_SCALEDB_TEMPLATE = DOCKER_DIR_SCALEDB + "/template"       # for using mariadb 10.1.13
DOCKER_DIR_SCALEDB_TEMPLATE  = DOCKER_DIR_SCALEDB + "/template_1_14"  # for using mariadb 10.1.14
DOCKER_DIR_SCALEDB_NODES     = DOCKER_DIR_SCALEDB + "/nodes"

DOCKER_DIR_MARIADB           = "/usr/local/docker-mariadb"
DOCKER_DIR_MARIADB_TEMPLATE  = DOCKER_DIR_MARIADB + "/template"
DOCKER_DIR_MARIADB_NODES     = DOCKER_DIR_MARIADB + "/nodes"

#
# Directories mapped into the container
#
DOCKER_DIR_CONT_SCALEDB_DATA       = "/usr/local/scaledb/data"
DOCKER_DIR_CONT_SCALEDB_ETC        = "/usr/local/scaledb/etc"
DOCKER_DIR_CONT_SCALEDB_LOCKS      = "/usr/local/scaledb/locks"
DOCKER_DIR_CONT_SCALEDB_LOGS       = "/usr/local/scaledb/logs"
DOCKER_DIR_CONT_SCALEDB_TMP        = "/usr/local/scaledb/tmp"

DOCKER_DIR_CONT_MARIADB_DATA       = "/usr/local/mysql/data"

#
# Env - Linux
#
LINUX_SCALEDB_DATA     = SCALEDB_HOME + "/data"
LINUX_MARIADB_DATA     = MARIADB_HOME + "/data"


#
# Images
#
DOCKER_IMAGE_CAS  = "scaledb/node"
DOCKER_IMAGE_SLM  = "scaledb/node"
DOCKER_IMAGE_DB   = "scaledb/node"
#DOCKER_IMAGE_CAS  = "scaledb/node-new"
#DOCKER_IMAGE_SLM  = "scaledb/node-new"
#DOCKER_IMAGE_DB   = "scaledb/node-new"






