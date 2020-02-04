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
                },
                {
                    "id": "36026150-f479-4d42-9eb6-79797edfbf0a",
                    "name": "phy1",
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
                },
                {
                    "id": "2f6ad75a-627c-40b3-86b3-cb23795e8c4a",
                    "name": "phy1",
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
                },
                {
                    "id": "0c430198-8998-4b50-b90e-133a5c5629e2",
                    "name": "phy1",
                    "type": "SUB6_ACCESS",
                    "config": None
                }]
        }, {
            "id": "7fbe90cc-e9f4-4668-b761-a1bb9af34c90",
            "name": "ruckus-Tower-3",
            "location": {
                "longitude": -2.600066,
                "latitude": 51.449464,
                "info": "ruckus-Tower-3"
            },
            "phys": [
                {
                    "id": "e0e229de-1a7d-4b92-9f63-5150614556a0",
                    "name": "eth0",
                    "type": "WIRED_TUNNEL",
                    "config": None
                },
                {
                    "id": "fceab632-e40e-44ef-9506-cafa52bc5b99",
                    "name": "phy0",
                    "type": "SUB6_ACCESS",
                    "config": None
                },
                {
                    "id": "31cc9565-27ff-437a-95e5-9b731cdae934",
                    "name": "phy1",
                    "type": "SUB6_ACCESS",
                    "config": None
                }]
        }, {
            "id": "07faa48a-5138-438f-9342-ce0f3767970c",
            "name": "ruckus-Tower-6",
            "location": {
                "longitude": -2.600975,
                "latitude": 51.449928,
                "info": "ruckus-Tower-6"
            },
            "phys": [
                {
                    "id": "0c171899-6961-4fe3-ab81-a97fbf8d4cf2",
                    "name": "eth0",
                    "type": "WIRED_TUNNEL",
                    "config": None
                },
                {
                    "id": "24226d2a-fae0-44c2-a9cb-841335fd0c62",
                    "name": "phy0",
                    "type": "SUB6_ACCESS",
                    "config": None
                },
                {
                    "id": "c0dcccd7-4842-41e4-ac7f-ed7a6474ea10",
                    "name": "phy1",
                    "type": "SUB6_ACCESS",
                    "config": None
                }]
        }, {
            "id": "8f0b7d33-ae7d-4c93-ba1b-49b96b88d82a",
            "name": "ruckus-5g-room",
            "location": {
                "longitude": -2.602312,
                "latitude": 51.455507,
                "info": "ruckus-5g-room"
            },
            "phys": [
                {
                    "id": "bfdac826-ea41-48c9-a621-d429cba21c21",
                    "name": "eth0",
                    "type": "WIRED_TUNNEL",
                    "config": None
                },
                {
                    "id": "4ab42ddb-75d6-4888-b78b-0a28a7422e25",
                    "name": "phy0",
                    "type": "SUB6_ACCESS",
                    "config": None
                },
                {
                    "id": "13c93e6d-4efa-4e79-88d5-51fc70fc3c80",
                    "name": "phy1",
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
        "apgroup_name": "M-SHED East",
        "wlangrop_name": "MSHED-East 2.4Ghz",
        "wlangroup_id": "bd690a30-bab7-11e9-91f9-22d1e8e61ae8",
        "type": "WIRED_TUNNEL"
    },
    "804cec3f-4262-4c94-b988-b4ae40fdb10e": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "68b00bbb-f400-462d-b4f4-3e9160013155",
        "apgroup_name": "M-SHED East",
        "wlangrop_name": "MSHED-East 2.4Ghz",
        "wlangroup_id": "bd690a30-bab7-11e9-91f9-22d1e8e61ae8",
        "type": "2.4GHZ"
    },
    "36026150-f479-4d42-9eb6-79797edfbf0a": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "68b00bbb-f400-462d-b4f4-3e9160013155",
        "apgroup_name": "M-SHED East",
        "wlangrop_name": "MSHED-East 5Ghz",
        "wlangroup_id": "664fc201-77c0-11e9-91f9-22d1e8e61ae8",
        "type": "5GHZ"
    },
    "8a13fdd3-58cc-4030-8370-bf5013977732": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "6c9ee78e-0928-4526-b461-2ca45acf769b",
        "apgroup_name": "M-SHED Middle",
        "wlangrop_name": "MSHED-Middle 2.4Ghz",
        "wlangroup_id": "ca8beca2-bab7-11e9-91f9-22d1e8e61ae8",
        "type": "WIRED_TUNNEL"
    },
    "a04ecb81-4e91-4509-bc74-18ca44263943": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "6c9ee78e-0928-4526-b461-2ca45acf769b",
        "apgroup_name": "M-SHED Middle",
        "wlangrop_name": "MSHED-Middle 2.4Ghz",
        "wlangroup_id": "ca8beca2-bab7-11e9-91f9-22d1e8e61ae8",
        "type": "2.4GHZ"
    },
    "2f6ad75a-627c-40b3-86b3-cb23795e8c4a": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "6c9ee78e-0928-4526-b461-2ca45acf769b",
        "apgroup_name": "M-SHED Middle",
        "wlangrop_name": "MSHED-Middle 5Ghz",
        "wlangroup_id": "deeb0151-7c72-11e9-91f9-22d1e8e61ae8",
        "type": "5GHZ"
    },
    "210e1929-aa92-4e12-97cf-74090a0a257c": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "5aa9383e-ca82-41da-bb4f-e804f48de9bf",
        "apgroup_name": "M-SHED West",
        "wlangrop_name": "MSHED-West 2.4Ghz",
        "wlangroup_id": "a631da42-771e-11e9-91f9-22d1e8e61ae8",
        "type": "WIRED_TUNNEL"
    },
    "0b3d057b-c5da-4b14-a102-0edd51caada5": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "5aa9383e-ca82-41da-bb4f-e804f48de9bf",
        "apgroup_name": "M-SHED West",
        "wlangrop_name": "MSHED-West 2.4Ghz",
        "wlangroup_id": "a631da42-771e-11e9-91f9-22d1e8e61ae8",
        "type": "2.4GHZ"
    },
    "0c430198-8998-4b50-b90e-133a5c5629e2": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "5aa9383e-ca82-41da-bb4f-e804f48de9bf",
        "apgroup_name": "M-SHED West",
        "wlangrop_name": "MSHED-West 5Ghz",
        "wlangroup_id": "b2b34c91-771e-11e9-91f9-22d1e8e61ae8",
        "type": "5GHZ"
    },
    "fceab632-e40e-44ef-9506-cafa52bc5b99": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "5e716b79-6cba-48c1-9458-2f24699a1f68",
        "apgroup_name": "TOWER 3",
        "wlangrop_name": "Tower 3 2.4Ghz",
        "wlangroup_id": "9aacddb2-ce17-11e8-88ed-000000402400",
        "type": "2.4GHZ"
    },
    "e0e229de-1a7d-4b92-9f63-5150614556a0": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "5e716b79-6cba-48c1-9458-2f24699a1f68",
        "apgroup_name": "TOWER 3",
        "wlangroup_name": "Tower 3 2.4Ghz",
        "wlangroup_id": "9aacddb2-ce17-11e8-88ed-000000402400",
        "type": "WIRED_TUNNEL"
    },
    "31cc9565-27ff-437a-95e5-9b731cdae934": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "5e716b79-6cba-48c1-9458-2f24699a1f68",
        "apgroup_name": "TOWER 3",
        "wlangrop_name": "Tower 3 5Ghz",
        "wlangroup_id": "93659d82-ce17-11e8-88ed-000000402400",
        "type": "5GHZ"
    },
    "24226d2a-fae0-44c2-a9cb-841335fd0c62": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "f0154e80-d6c8-4f72-a768-3b94a6254150",
        "apgroup_name": "TOWER 6",
        "wlangrop_name": "Tower 6 2.4Ghz",
        "wlangroup_id": "e41485c2-ce17-11e8-88ed-000000402400",
        "type": "2.4GHZ"
    },
    "0c171899-6961-4fe3-ab81-a97fbf8d4cf2": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "f0154e80-d6c8-4f72-a768-3b94a6254150",
        "apgroup_name": "TOWER 6",
        "wlangroup_name": "Tower 6 2.4Ghz",
        "wlangroup_id": "e41485c2-ce17-11e8-88ed-000000402400",
        "type": "WIRED_TUNNEL"
    },
    "c0dcccd7-4842-41e4-ac7f-ed7a6474ea10": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "f0154e80-d6c8-4f72-a768-3b94a6254150",
        "apgroup_name": "TOWER 6",
        "wlangrop_name": "Tower 6 5Ghz",
        "wlangroup_id": "dc0b2e12-ce17-11e8-88ed-000000402400",
        "type": "5GHZ"
    },	
    "4ab42ddb-75d6-4888-b78b-0a28a7422e25": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "26ea12e7-34f4-4ff2-8703-134ad2740576",
        "apgroup_name": "5G Room",
        "wlangrop_name": "5G Room 2.4Ghz",
        "wlangroup_id": "761e6302-ce18-11e8-88ed-000000402400",
        "type": "2.4GHZ"
    },
    "bfdac826-ea41-48c9-a621-d429cba21c21": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "26ea12e7-34f4-4ff2-8703-134ad2740576",
        "apgroup_name": "5G Room",
        "wlangroup_name": "5G Room 2.4Ghz",
        "wlangroup_id": "761e6302-ce18-11e8-88ed-000000402400",
        "type": "WIRED_TUNNEL"
    },
    "13c93e6d-4efa-4e79-88d5-51fc70fc3c80": {
        "zone_id": "f77a8816-3049-40cd-8484-82919275ddc3",
        "apgroup_id": "26ea12e7-34f4-4ff2-8703-134ad2740576",
        "apgroup_name": "5G Room",
        "wlangrop_name": "5G Room 5Ghz",
        "wlangroup_id": "6f308d72-ce18-11e8-88ed-000000402400",
        "type": "5GHZ"
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
        'password': 'SevenGW1-F1'
     },
     {
         'id': 1,
         'type': 'i2cat',
         'ip': '10.68.34.16',
         'port': 8008,
         'url': 'http://{}:{}'
    }
]
