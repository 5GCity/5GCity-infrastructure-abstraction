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

import json, requests
from urllib3.exceptions import InsecureRequestWarning
from copy import deepcopy

_headers = {
    'Content-type': 'application/json;charset=UTF-8',
}

EMPTY_TOPOLOGY = {
        "boxes": [],
        "links": []
    }


class RuckusWiFi(object):
    """Integration for Ruckus Controller
    Arguments:
        Wireless {[type]} -- [description]
    """
    def __init__(self,
                 controller_id=None,
                 ip='127.0.0.1',
                 port=8080,
                 url="http://{}:{}/",
                 topology=EMPTY_TOPOLOGY,
                 chunks=[],
                 phy_id_mapping=None,
                 username=None,
                 password=None):
        self.id = controller_id
        self._ip = ip
        self._port = port
        self._url = url.format(ip,port)
        self._topology = topology
        self._phy_id_mapping = phy_id_mapping 
        self._username = username
        self._password = password
        self._chunks = {}

        for chunk in chunks:
            self._chunks[chunk["id"]] = chunk

        # Disable Warnings about insecure SSL being used 
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)

        # GET WIRELESS CONFIG FROM RUCKUS CONTROLLER
        # {
        #     "channelNumber": 36,
        #     "channelBandwidth": 40,
        #     "txPower": 2000
        # }

        ticket = self.__login()

        # TODO: Implement GET tx Power, by default now is "Full"

        for box in self._topology["boxes"]:
            for phy in box["phys"]:
                if self._phy_id_mapping[phy["id"]]["type"] == "2.4GHZ":
                    u_path = '/v7_0/rkszones/{p[zone_id]}/'.format(
                        p=self._phy_id_mapping[phy["id"]])
                    u_path += 'apgroups/{p[apgroup_id]}'.format(
                        p=self._phy_id_mapping[phy["id"]])
                    u_path += '?serviceTicket={t}'.format(
                        t=ticket)
                    url = self._url + u_path
                    resp = requests.get(
                        url,
                        headers=_headers,
                        verify = False
                        )

                    self.__logoff(ticket)

                    if resp.status_code == 200:
                        ap_group = json.loads(resp.text)

                    phy["config"] = {
                        "channelNumber": ap_group["wifi24"]["channel"],
                        "channelBandwidth": ap_group["wifi24"]["channelWidth"],
                        "txPower": 3600
                    }

    # Find free chunk_ids
    def __next_chunk_id(self):
        if self._chunks.keys(): 
            max_id = max(self._chunks.keys())
            return max_id + 1
        else:
            return 1

    # chunkete-topology-controller implementation
    def getChunketeTopology(self):       
        return deepcopy(self._topology), 200

    def putInterfaceLTEConfig(self, phy_id, parameters):
        return '',401

    def putInterfaceType(self, phy_id, phy_type):
        for box in self._topology["boxes"]:
            for phy in box["phys"]:
                if phy["id"] == phy_id:      
                    if phy["type"] != phy_type:
                        return '', 401
                    else:
                        return '', 200

    def putInterfaceWiredConfig(self, phy_id, parameters):
        for box in self._topology["boxes"]:
            for phy in box["phys"]:
                if phy["id"] == phy_id:      
                    if phy["config"] != json.loads(parameters):
                        return '',401
                    else:
                        return '',200

    def putInterfaceWirelessConfig(self, phy_id, parameters):
        # Create a session on Ruckus controller
        ticket = self.__login()

        # TODO: Implement tx Power, by default now is "Full"

        for box in self._topology["boxes"]:
            for phy in box["phys"]:
                if phy["id"] == phy_id:
                    if self._phy_id_mapping[phy_id]["type"] == "2.4GHZ":
                        config = {
                            "wifi24": {
                                "channelWidth": json.loads(
                                    parameters)["channelBandwidth"],
                                "channel": json.loads(
                                    parameters)["channelNumber"],
                            }
                        }
                        u_path = '/v7_0/rkszones/{p[zone_id]}/'.format(
                            p=self._phy_id_mapping[phy_id])
                        u_path += '/apgroups/{p[apgroup_id]}'.format(
                            p=self._phy_id_mapping[phy_id])
                        u_path += '?serviceTicket={t}'.format(
                            p=self._phy_id_mapping[phy_id], t=ticket)
                        url = self._url + u_path
                        # f'/v7_0/rkszones/{self._phy_id_mapping[phy_id]["zone_id"]}
                        # /apgroups/{self._phy_id_mapping[phy_id]["apgroup_id"]}?serviceTicket={ticket}'
                        resp = requests.patch(
                            url,
                            data=json.dumps(config),
                            headers=_headers,
                            verify = False
                            )
                        
                        self.__logoff(ticket)
                        if resp.status_code == 204:
                            phy["config"] = json.loads(parameters)
                            return '', 201
                        else:
                            return '', 401
                    elif self._phy_id_mapping[phy_id]["type"] == "5GHZ":
                        # TODO: 5GHz Wireless networks support
                        return '', 401
                    elif self._phy_id_mapping[phy_id]["type"] == "WIRED":
                        # TODO: Wired interface config implied
                        return '', 201

    # chunkete-chunk-controller implementation
    def getAllChunks(self):
        return [self._chunks[key] for key in self._chunks.keys()], 200

    def registerNewChunk(self, content):
        chunk = json.loads(content)
        id = self.__next_chunk_id()
        self._chunks[id] = chunk
        self._chunks[id]["id"]=id
        data = {
                "id": id
            }
        return data, 201

    def getChunkById(self, chunk_id):
        """
            url = "http://{}:{}/chunkete/chunk/{}".format(
                self._ip, str(self._port), id)
            resp = requests.get()
                url,
                data=parameters,
                headers=_headers
                )
            print (url)
            return resp
        """
        return self._chunks[int(chunk_id)]
        
    def removeExistingChunk(self, chunk_id):
        """
            url = "http://{}:{}/chunkete/chunk/{}".format(
                self._ip, str(self._port), id)
            resp = requests.delete(
                url,
                data=parameters,
                headers=_headers
                )
            print (url)
            return resp
        """
        del self._chunks[int(chunk_id)]
        return '', 200

        
# chunkete-swam-controller implementation
    def getAllSWAMServices(self, chunk_id):
        return [
            service for service in self._chunks[chunk_id]["serviceList"]
        ]

    def registerNewSWAMService(self, chunk_id, content):
        """
            {
            "lteConfig": {
                "cellReserved": "not-reserved",
                "mmeAddress": "192.168.50.2",
                "mmePort": 333,
                "plmnId": "00101"
            },
            "selectedPhys": [
            (interfaces type of SUB6_ACCESS, LTE_PRIMARY_PLMN and WIRED_TUNNEL)
                14, 23
            ],
            "vlanId": 201, (1-4095)
            "wirelessConfig": {
                "encryption": "WPA", (NONE, WPA, WPA2, WEP s)
                "password": "secret",
                "ssid": "Test"
            }
            }
        """
        service = json.loads(content)
        ticket = self.__login()

        if service["wirelessConfig"]["encryption"] == "NONE":
            encryption = {
                "method": "None",
            }
        elif service["wirelessConfig"]["encryption"] == "WPA":
            encryption = {
                "method": "WPA_Mixed",
                "algorithm": "TKIP_AES",
                "passphrase": service["wirelessConfig"]["password"],
            }
        elif service["wirelessConfig"]["encryption"] == "WPA2":
            encryption = {
                "method": "WPA2",
                "algorithm": "AES",
                "mfp": "disabled",
                "passphrase": service["wirelessConfig"]["password"],
            }
        elif service["wirelessConfig"]["encryption"] == "WEP":
            encryption = {
                "method": "WEP_64",
                "keyIndex": 1,
                "keyInHex": service["wirelessConfig"]["password"],
            }
        else:
            return '',401

        # Create WLAN
        u_path = '/v7_0/rkszones/{p[zone_id]}/wlans?serviceTicket={t}'.format(
            p=self._phy_id_mapping, t=ticket)
        url = self._url + u_path
        # f'/v7_0/rkszones/{self._phy_id_mapping["zone_id"]}/wlans?serviceTicket={ticket}'
        wlan = {
            "name": service["wirelessConfig"]["ssid"],
            "ssid": service["wirelessConfig"]["ssid"],
            "description": "Created by 5GCity Slice Manager",
            "encryption": encryption,
            "vlan": {
                "accessVlan": service["vlanId"],
            }
        }
        resp = requests.post(
            url,
            data= json.dumps(wlan),
            headers=_headers,
            verify= False
        )

        # If WLAN Created OK, raise it up on each of the interfaces      
        if resp.status_code == 201:
            service["id"] = int(json.loads(resp.text)["id"])
            return_data = {
                "id": service["id"]
            }
            data = {
                "id": str(service["id"])
            }
            for phy in service["selectedPhys"]:
                if self._phy_id_mapping[phy]["type"] in ["2.4GHZ","5GHZ"]:
                    u_path = '/v7_0/rkszones/{p[zone_id]}/'.format(
                        p=self._phy_id_mapping[phy])
                    u_path += 'wlangroups/{p[wlangroup_id]}/'.format(
                        p=self._phy_id_mapping[phy]
                    )
                    u_path += 'members?serviceTicket={t}'.format(
                        t=ticket)
                    url = self._url + u_path
                    # f'/v7_0/rkszones/{self._phy_id_mapping[phy]["zone_id"]}/wlangroups/
                    # {self._phy_id_mapping[phy]["wlangroup_id"]}/members?serviceTicket={ticket}'
                    resp = requests.post(
                        url,
                        data= json.dumps(data),
                        headers=_headers,
                        verify= False
                    )    

                    if resp.status_code != 201:
                        u_path = '/v7_0/rkszones/{}/wlangroups/{}/members?serviceTicket={}'.format(
                            self._phy_id_mapping["zone_id"], data["id"],ticket)
                        url = self._url + u_path
                        # f'/v7_0/rkszones/{self._phy_id_mapping["zone_id"]}/wlans/{data["id"]}?
                        # serviceTicket={ticket}'
                        resp = requests.delete(
                            url,
                            headers=_headers,
                            verify = False
                        )
                        return resp.text, 401

            self._chunks[int(chunk_id)]["serviceList"].append(service)
            self.__logoff(ticket)
            return return_data, 201
        else:
            return resp.text, 401

    def getSWAMServiceById(self, chunk_id, service_id):
        """
            url = "http://{}:{}/chunkete/chunk/{}/service/SWAM/{}".format(
                self._ip, str(self._port), chunk_id, service_id)
            resp = requests.get()
                url,
                data=parameters,
                headers=_headers
                )
            print (url)
            return resp
        """
        for service in self._chunks[chunk_id]["serviceList"]:
            if service["id"] == service_id:
                return service
        return '', 404

    def removeExistingSWAMService(self, chunk_id, service_id):
        service_list = self._chunks[int(chunk_id)]["serviceList"]

        for index in range(len(service_list)):
            if service_list[index]["id"] == service_id:
                ticket = self.__login()

                # Remove WLAN
                u_path = '/v7_0/rkszones/{}/wlans/{}?serviceTicket={}'.format(
                    self._phy_id_mapping["zone_id"], service_id, ticket)
                url = self._url + u_path
                # f'/v7_0/rkszones/{self._phy_id_mapping["zone_id"]}/wlans/{service_id}?
                # serviceTicket={ticket}'
                resp = requests.delete(
                    url,
                    headers=_headers,
                    verify= False
                )

                if resp.status_code == 204:
                    self._chunks[int(chunk_id)]["serviceList"].pop(index)
                    self.__logoff(ticket)
                    return '', 200
                else:
                    self.__logoff(ticket)
                    return resp.text, 401
        return resp.text, 404


# Session management on Ruckus controller
    def __login(self):
        url = (self._url + "/v7_0/serviceTicket")
        ticket_request = {
            "username": self._username,
            "password": self._password,
        }

        resp = requests.post(
            url,
            data= json.dumps(ticket_request),
            headers=_headers,
            verify=False
        )
        return json.loads(resp.text)["serviceTicket"]

    def __logoff(self, ticket):
        url = self._url
        url += "/v7_0/serviceTicket?serviceTicket={}".format(ticket)

        requests.delete(
            url,
            headers=_headers,
            verify=False)
