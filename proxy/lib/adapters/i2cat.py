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

import json
import requests

_headers = {
    'Content-type': 'application/json',
    "Accept": "application/json",
    'Cache-Control': 'no-cache'
}

class I2catController(object):
    """Integration with FlexRAN solution
    
    Arguments:
        Wireless {[type]} -- [description]
    """
    def __init__(self,
                 controller_id=None,
                 ip='127.0.0.1',
                 port=8080,
                 url=None):
        self.id = controller_id
        self._ip = ip
        self._port = port
        self._url = url.format(ip,port)


# chunkete-topology-controller implementation
    def getChunketeTopology(self):
        url = (self._url + "/chunkete/topology").format(self._ip, str(self._port))

        resp = requests.get(url)
        data = json.loads(resp.text)
        return data, resp.status_code

    def putInterfaceLTEConfig(self, phy_id, parameters):
        url = self._url + \
            "/chunkete/topology/physicalInterface/{}/LTEConfig".format(
            phy_id)
        resp = requests.put(
            url,
            data=parameters,
            headers=_headers
            )
        data = json.loads(resp.text)
        return data, resp.status_code

    def putInterfaceType(self, phy_id, phy_type):
        url = "http://{}:{}/chunkete/topology/physicalInterface/{}/type/{}".format(
            self._ip, str(self._port), phy_id, phy_type)
        resp = requests.put(
            url,
            headers=_headers
            )
        data = json.loads(resp.text)
        return data, resp.status_code

    def putInterfaceWiredConfig(self, phy_id, parameters):
        url = "http://{}:{}/chunkete/topology/physicalInterface/{}/wiredConfig".format(
            self._ip, str(self._port), phy_id)
        resp = requests.put(
            url,
            data=parameters,
            headers=_headers
            )
        data = json.loads(resp.text)
        return data, resp.status_code

    def putInterfaceWirelessConfig(self, phy_id, parameters):
        url = self._url + "/chunkete/topology/physicalInterface/{}/wirelessConfig".format(
            phy_id)
        resp = requests.put(
            url,
            data=parameters,
            headers=_headers
            )
        data = json.loads(resp.text)
        return data, resp.status_code


# chunkete-chunk-controller implementation
    def getAllChunks(self):
        url = "http://{}:{}/chunkete/chunk".format(
            self._ip,
            str(self._port))

        resp = requests.get(url)
        data = json.loads(resp.text)
        return data, resp.status_code

    def registerNewChunk(self, content):
        pre_chunk_list, code = self.getAllChunks()        
        pre_chunk_ids = [x["id"] for x in pre_chunk_list]

        url = "http://{}:{}/chunkete/chunk".format(
            self._ip, str(self._port))
        resp = requests.post(
            url,
            data=content,
            headers=_headers
            )

        post_chunk_list, code = self.getAllChunks()        
        post_chunk_ids = [x["id"] for x in post_chunk_list]

        chunk_id = [x for x in post_chunk_ids if x not in pre_chunk_ids][0]

        data = json.loads(resp.text)
        return data, resp.status_code            

    def getChunkById(self, chunk_id):
        url = "http://{}:{}/chunkete/chunk/{}".format(
            self._ip, str(self._port), chunk_id)
        resp = requests.get(
            url,
            headers=_headers
            )
        data = json.loads(resp.text)
        return data, resp.status_code

    def removeExistingChunk(self, chunk_id):
        url = "http://{}:{}/chunkete/chunk/{}".format(
            self._ip, str(self._port), chunk_id)
        resp = requests.delete(
            url,
            headers=_headers
            )
        if resp.status_code == 200:
            data = resp.text
        else:
            data = json.loads(resp.text)
        return data, resp.status_code


# chunkete-swam-controller implementation
    def getAllSWAMServices(self, chunk_id):
        url = "http://{}:{}/chunkete/chunk/{}/service/SWAM".format(
            self._ip, str(self._port), chunk_id)
        resp = requests.get(
            url,
            headers=_headers
            )
        data = json.loads(resp.text)
        return data, resp.status_code

    def registerNewSWAMService(self, chunk_id, content):
        url = "http://{}:{}/chunkete/chunk/{}/service/SWAM".format(
            self._ip, str(self._port), chunk_id)
        resp = requests.post(
            url,
            data=content,
            headers=_headers
            )
        data = json.loads(resp.text)
        return data, resp.status_code

    def getSWAMServiceById(self, chunk_id, service_id):
        url = "http://{}:{}/chunkete/chunk/{}/service/SWAM/{}".format(
            self._ip, str(self._port), chunk_id, service_id)
        resp = requests.get(
            url,
            headers=_headers
            )
        data = json.loads(resp.text)
        return data, resp.status_code

    def removeExistingSWAMService(self, chunk_id, service_id):
        url = "http://{}:{}/chunkete/chunk/{}/service/SWAM/{}".format(
            self._ip, str(self._port), chunk_id, service_id)
        resp = requests.delete(
            url,
            headers=_headers
            )
        if resp.text:
            data = json.loads(resp.text)
        else:
            data = ''
        return data, resp.status_code
