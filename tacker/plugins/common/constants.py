# Copyright 2012 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# service type constants:
CORE = "CORE"
DUMMY = "DUMMY"
VNFM = "VNFM"
NFVO = "NFVO"

COMMON_PREFIXES = {
    CORE: "",
    DUMMY: "/dummy_svc",
    VNFM: "",
    NFVO: ""
}

# Service operation status constants
ACTIVE = "ACTIVE"
DOWN = "DOWN"

PENDING_CREATE = "PENDING_CREATE"
PENDING_UPDATE = "PENDING_UPDATE"
PENDING_DELETE = "PENDING_DELETE"
PENDING_SCALE_IN = "PENDING_SCALE_IN"
PENDING_SCALE_OUT = "PENDING_SCALE_OUT"

INACTIVE = "INACTIVE"
DEAD = "DEAD"
ERROR = "ERROR"

ACTIVE_PENDING_STATUSES = (
    ACTIVE,
    PENDING_CREATE,
    PENDING_UPDATE
)

POLICY_SCALING = 'tosca.policy.tacker.Scaling'
POLICY_SCALING_ACTIONS = (ACTION_SCALE_OUT,
                          ACTION_SCALE_IN) = ('out', 'in')
POLICY_ACTIONS = {POLICY_SCALING: POLICY_SCALING_ACTIONS}
