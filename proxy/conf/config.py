#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2017-2022 Univertity of Bristol - High Performance Networks Group
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


# Topology of Ruckus Controller
RUCKUS_INIT_TOPOLOGY = {
    "boxes": [
        {
            "id": "72a5e214-48e8-48b1-9cf4-adcd0a58c61e",
            "name": "ruckus-east-roof",
            "location": {
                "longitude": -2.597035,
                "latitude": 51.448181,
                "info": "ruckus-east-roof"
            },
            "phys": [
                {
                    "id": "fb93d9cf-93f6-4380-a1d3-2161eba2e871",
                    "name": "eth0",
                    "type": "WIRED_TUNNEL",
                    "config": None
                },
                {
                    "id": "804cec3f-4262-4c94-b988-b4ae40fdb10e",
                    "name": "phy0",
                    "type": "SUB6_ACCESS",
                    "config": None
                }]
        },
        {
            "id": "ea6c790a-2060-4db1-94c8-b957631c9937",
            "name": "ruckus-middle-roof",
            "location": {
                "longitude": -2.598227,
                "latitude": 51.447858,
                "info": "ruckus-middle-roof"
            },
            "phys": [
                {
                    "id": "8a13fdd3-58cc-4030-8370-bf5013977732",
                    "name": "eth0",
                    "type": "WIRED_TUNNEL",
                    "config": None
                },
                {
                    "id": "a04ecb81-4e91-4509-bc74-18ca44263943",
                    "name": "phy0",
                    "type": "SUB6_ACCESS",
                    "config": None
                }]
        }, {
            "id": "73f2c8b7-4a24-4bc6-8188-b3cd2668b1dd",
            "name": "ruckus-west-roof",
            "location": {
                "longitude": -2.599009,
                "latitude": 51.447500,
                "info": "ruckus-west-roof"
            },
            "phys": [
                {
                    "id": "210e1929-aa92-4e12-97cf-74090a0a257c",
                    "name": "eth0",
                    "type": "WIRED_TUNNEL",
                    "config": None
                },
                {
                    "id": "0b3d057b-c5da-4b14-a102-0edd51caada5",
                    "name": "phy0",
                    "type": "SUB6_ACCESS",
                    "config": None
                }]
        }
    ],
    "links": []
}

# Mapping between AP ids in Ruckus and AP ids in topology
RUCKUS_ID_MAPPING = {
    "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
    "fb93d9cf-93f6-4380-a1d3-2161eba2e871": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "68b00bbb-f400-462d-b4f4-3e9160013155",
        "wlangroup_id": "bd690a30-bab7-11e9-91f9-22d1e8e61ae8",
        "type": "WIRED_TUNNEL"
    },
    "804cec3f-4262-4c94-b988-b4ae40fdb10e": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "68b00bbb-f400-462d-b4f4-3e9160013155",
        "wlangroup_id": "bd690a30-bab7-11e9-91f9-22d1e8e61ae8",
        "type": "2.4GHZ"
    },
    "8a13fdd3-58cc-4030-8370-bf5013977732": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "6c9ee78e-0928-4526-b461-2ca45acf769b",
        "wlangroup_id": "ca8beca2-bab7-11e9-91f9-22d1e8e61ae8",
        "type": "WIRED_TUNNEL"
    },
    "a04ecb81-4e91-4509-bc74-18ca44263943": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "6c9ee78e-0928-4526-b461-2ca45acf769b",
        "wlangroup_id": "ca8beca2-bab7-11e9-91f9-22d1e8e61ae8",
        "type": "2.4GHZ"
    },
    "210e1929-aa92-4e12-97cf-74090a0a257c": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "5aa9383e-ca82-41da-bb4f-e804f48de9bf",
        "wlangroup_id": "a631da42-771e-11e9-91f9-22d1e8e61ae8",
        "type": "WIRED_TUNNEL"
    },
    "0b3d057b-c5da-4b14-a102-0edd51caada5": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "5aa9383e-ca82-41da-bb4f-e804f48de9bf",
        "wlangroup_id": "a631da42-771e-11e9-91f9-22d1e8e61ae8",
        "type": "2.4GHZ"
    }
}

# Controller Id's need to match the position in the list
CONTROLLERS = [
    {
        'id': 0,
        'type': 'ruckus',
        'ip': '10.68.20.250',
        'port': 8443,
        'url': 'https://{}:{}/wsg/api/public',
        'topology': RUCKUS_INIT_TOPOLOGY,
        'username': 'admin',
        'password': <PASSWORD>
    },
    {
        'id': 1,
        'type': 'i2cat',
        'ip': '10.68.34.16',
        'port': 8008,
        'url': 'http://{}:{}'
    }
]
