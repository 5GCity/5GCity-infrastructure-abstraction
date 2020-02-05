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

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, Response, jsonify, render_template, request
import logging
import os
import sys
import json
import uuid
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.adapters.ruckus import RuckusWiFi
from lib.adapters.i2cat import I2catController
from conf.config import CONTROLLERS, RUCKUS_ID_MAPPING, RUCKUS_INIT_TOPOLOGY

# Logger configuration
log_filename = "logs/output.log"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(funcName)s %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S', filename=log_filename, level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)
logger = logging.getLogger()

log_base = "{}:{}:{}"  # INTERFACE,endpoint,REQ/RESP,content


# Flask app
app = Flask(__name__)
app.config.from_object(__name__)


# Define database
Base = declarative_base()
engine = create_engine('sqlite:///file.db', echo=False)


def generate_uuid():
    return str(uuid.uuid4())


class Chunk(Base):
    __tablename__ = 'chunks'
    id = Column(String, primary_key=True, default=generate_uuid)
    # controllers_chunk is a dictionary where the keys are the ids of the
    # controller and the value is a list of the chunk in that controller
    # in the form "{controllerid1:[chunkid,...],controllerid2:...}"
    controllers_chunk = Column(String)
    # controllers_phys is a dictionary where the keys are the ids of the
    # controller and the value is a list of the chunk in that controller
    # in the form "{controllerid1:[chunkid,...],controllerid2:...}"
    controllers_phys = Column(String)
    phyList = Column(String)
    name = Column(String)
    assignedQuota = Column(String)
    serviceList = Column(String)
    linkList = Column(String)
    chunk_json = Column(String)

    def __repr__(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}".format(
            self.id,
            self._controllers_chunk,
            self.controllers_phys,
            self.phyList,
            self.name,
            self.assignedQuota,
            self.serviceList,
            self.linkList,
            self.chunk_json
        )


class Box(Base):
    __tablename__ = 'boxes'
    id = Column(String, primary_key=True, default=generate_uuid)
    controller_id = Column(Integer)
    box_id_controller = Column(String)
    name = Column(String)
    location = Column(String)
    phys = Column(String)
    box_json = Column(String)

    def __repr__(self):
        return "{}, {}, {}, {}, {}, {}, {}".format(
            self.id,
            self.controller_id,
            self.box_id_controller,
            self.name,
            self.location,
            self.phys,
            self.box_json
        )


class Phy(Base):
    __tablename__ = 'phys'
    id = Column(String, primary_key=True, default=generate_uuid)
    controller_id = Column(Integer)
    phy_id_controller = Column(String)
    type = Column(String)
    name = Column(String)
    config = Column(String)
    virtualInterfaceList = Column(String)
    phy_json = Column(String)

    def __repr__(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}".format(
            self.id,
            self.controller_id,
            self.phy_id_controller,
            self.type, self.name,
            self.config,
            self.virtualInterfaceList,
            self.phy_json
        )


class Vif(Base):
    __tablename__ = 'vifs'
    id = Column(String, primary_key=True, default=generate_uuid)
    service_id = Column(String)
    controller_id = Column(Integer)
    phy_id = Column(String)
    name = Column(String)
    vif_json = Column(String)

    def __repr__(self):
        return "{}, {}, {}, {}, {}, {}".format(
            self.id,
            self.service_id,
            self.controller_id,
            self.phy_id,
            self.name,
            self.vif_json
        )


class Vlan(Base):
    __tablename__ = 'vlans'
    id = Column(String, primary_key=True, default=generate_uuid)
    service_id = Column(String)
    tag = Column(Integer)
    controllers_vlans_id = Column(String)

    def __repr__(self):
        return "{}, {}, {}".format(
            self.id,
            self.service_id,
            self.tag,
            self.controller_vlans_id,
        )


class Service(Base):
    __tablename__ = 'services'
    id = Column(String, primary_key=True, default=generate_uuid)
    # controllers_services is a dictionary where the keys are the ids of the
    # controller and the value is a list of the chunk in that controller
    # in the form "{controllerid1:[serviceid,...],controllerid2:...}"
    controllers_services = Column(String)
    # controllers_phys is a dictionary where the keys are the ids of the
    # controller and the value is a list of the chunk in that controller
    # in the form "{controllerid1:[chunkid,...],controllerid2:...}"
    controllers_phys = Column(String)
    lteConfigCellReserved = Column(String)
    lteConfigMMEAddress = Column(String)
    lteConfigMMEPort = Column(Integer)
    lteConfigPLMNId = Column(String)
    selectedPhys = Column(String)
    selectedVifs = Column(String)
    wirelessConfigEncryption = Column(String)
    wirelessConfigPassword = Column(String)
    wirelessConfigSSID = Column(String)
    vlanId = Column(String)
    service_json = Column(String)

    def __repr__(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
            self.id,
            self.controllers_services,
            self.controllers_phys,
            self.lteConfigCellReserved,
            self.lteConfigMMEAddress,
            self.lteConfigMMEPort,
            self.lteConfigPLMNId,
            self.selectedPhys,
            self.selectedVifs,
            self.wirelessConfigSSID,
            self.wirelessConfigEncryption,
            self.wirelessConfigPassword,
            self.vlanId,
            self.service_json
        )

# helpers to translate dabatase type class objects into dictionaries


def _dictService(service):
    vlan = session.query(Vlan).filter(Vlan.service_id == service.id).one()

    if service.wirelessConfigSSID:
        wirelessConfig = {
            "ssid": service.wirelessConfigSSID,
            "encryption": service.wirelessConfigEncryption,
            "password": service.wirelessConfigPassword
        }
    else:
        wirelessConfig = None

    if service.lteConfigPLMNId:
        lteConfig = {
            "plmnId": service.lteConfigPLMNId,
            "cellReserved": service.lteConfigCellReserved,
            "mmeAddress": service.lteConfigMMEAddress,
            "mmePort": service.lteConfigMMEPort
        }
    else:
        lteConfig = None

    response_data = {
        "id": service.id,
        "serviceType": "SWAM_SERVICE",
        "selectedRoot": 0,
        "vlanId": {
            "id": vlan.id,
            "vlanId": vlan.tag
        },
        "selectedVifs": [{"id": x} for x in eval(service.selectedVifs)],
        "wirelessConfig": wirelessConfig,
        "lteConfig": lteConfig
    }

    return response_data


def _dictChunk(chunk):
    services = session.query(Service).filter(
        Service.id.in_(eval(chunk.serviceList))).all()
    phys = session.query(Phy).filter(Phy.id.in_(eval(chunk.phyList))).all()

    response_data = {
        "id": chunk.id,
        "name": chunk.name,
        "assignedQuota": 0,
        "serviceList": [_dictService(service) for service in services],
        "physicalInterfaceList": [_dictPhy(phy) for phy in phys],
        "linkList": []
    }

    return response_data


def _dictPhy(phy):
    vifs = session.query(Vif).filter(
        Vif.id.in_(eval(phy.virtualInterfaceList))).all()

    if phy.config:
        config = eval(phy.config)
    else:
        config = phy.config

    response_data = {
        "id": phy.id,
        "name": phy.name,
        "type": phy.type,
        "virtualInterfaceList": [_dictVif(vif) for vif in vifs],
        "config": config
    }

    return response_data


def _dictVif(vif):
    response_data = {
        "id": vif.id,
        "name": vif.name,
        "toRootVlan": 0,
        "toAccessVlan": 0,
        "toAccessPort": 0,
        "toRootPort": 0,
        "openFlowPortList": []
    }

    return response_data


# Create database session
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Initialize controller list
controllers = []
# controllers = {}

# formatter for the returned errors
API_RESPONSE = {
    "OK": {
        "content": '',
        "code": 200
    },
    "CREATED": {
        "content": '',
        "code": 201
    },
    "CONTROLLER": {
        "content": 'Controller Error',
        "code": 503
    },
    "NOTFOUND": {
        "content": 'Not Found',
        "code": 404
    },
    "DB_INTEGRITY": {
        "content": 'DB Integrity',
        "code": 401
    },
    "VERIFICATION_ERROR": {
        "content": 'Verification Error',
        "code": 401
    }
}


def errorResponder(error, message):
    # TODO: implement timestamp
    dt = datetime.today()

    return json.dumps({
        "timestamp": dt.isoformat(sep='T'),
        "status": API_RESPONSE[error]["code"],
        "error": API_RESPONSE[error]["content"],
        "message": message,
        "path": request.path
    }), API_RESPONSE[error]["code"]


NORTHBOUND = "NORTHBOUND"
SOUTHBOUND = "SOUTHBOUND"
INTERNAL = "INTERNAL"

REQUEST = "REQUEST"
RESPONSE = "RESPONSE"
REQRESP = "REQ/RESP"
ROLLBACK = "ROLLBACK"


# Load controllers info from config.py and register topologies
# Look for first phy_id free in database
db_id_phy_id_list = session.query(Phy.id, Phy.phy_id_controller).all()
# db_id_list = [r for (r, a) in db_id_phy_id_list]
# db_id_list.sort()
# if len(db_id_list) == 0:
#     new_phy_id = 1
# else:
#     new_phy_id = db_id_list[len(db_id_list)-1]+1

#     # Look for first box_id free in database
db_id_box_id_list = session.query(Box.id, Box.box_id_controller).all()
# db_id_list = [r for (r, a) in db_id_box_id_list]
# db_id_list.sort()
# if len(db_id_list) == 0:
#     new_box_id = 1
# else:
#     new_box_id = db_id_list[len(db_id_list)-1]+1

new_box_id = str(uuid.uuid4())
# *******************************
# Initialize proxy runtime status
# *******************************
#
# INITIAL TOPOLOGY RECOVERY (Boxes, Phys):
# =========================
# -RUCKUS type controller initial topology recovered from config.py
# -I2CAT type controller initial topology recovered from live
#   SOUTHBOUND REQUEST to controller
#
# CURRENT STATE (Chunks, Services, VirtualInterfaces):
# ==============
# -RUCKUS type controller current state recovered from database and
#   controllers runtime status
# -I2CAT type controller current state kept on controller
#
for item in CONTROLLERS:
    if item['type'] == 'ruckus':
        # Recover the list of chunks from the database
        db_chunks = session.query(Chunk).all()

        chunks = []

        for db_chunk in db_chunks:
            if eval(db_chunk.controllers_chunk)[len(controllers)]:
                chunk = _dictChunk(db_chunk)
                phys_to_pop = []
                services_to_pop = []
                for service in chunk["serviceList"]:
                    db_service = session.query(Service).filter(
                        Service.id == service["id"]).one()
                    if len(controllers) in \
                            eval(db_service.controllers_services).keys():
                        service["id"] = eval(db_service.controllers_services)[
                            len(controllers)]
                    else:
                        services_to_pop.append(service)
                [chunk["serviceList"].remove(service)
                 for service in services_to_pop]

                for phy in chunk["physicalInterfaceList"]:
                    try:
                        db_phy = session.query(Phy).filter(
                            Phy.id == phy["id"],
                            Phy.controller_id == len(controllers)).one()
                        phy = db_phy.phy_id_controller
                    except NoResultFound:
                        phys_to_pop.append(phy)
                [chunk["physicalInterfaceList"].remove(
                    phy) for phy in phys_to_pop]

                chunk["id"] = eval(db_chunk.controllers_chunk)[
                    len(controllers)]
                chunks.append(chunk)

        phy_id_mapping = RUCKUS_ID_MAPPING
        controller = RuckusWiFi(
            controller_id=item['id'],
            ip=item['ip'],
            port=item['port'],
            url=item['url'],
            topology=item['topology'],
            chunks=chunks,
            phy_id_mapping=phy_id_mapping,
            username=item['username'],
            password=item['password']
        )
        controllers.append(controller)
        # controllers[controller.controller_id] = controller

    elif item['type'] == 'i2cat':
        controller = I2catController(
            controller_id=item['id'],
            ip=item['ip'],
            port=item['port'],
            url=item['url']
        )
        controllers.append(controller)
        # controllers[controller.controller_id] = controller

    for box in controller.getChunketeTopology()[0]["boxes"]:
        if box['id'] not in [r for (a, r) in db_id_box_id_list]:
            try:
                # initial_topology["boxes"].append(box)
                new_box = Box(
                    name=box["name"],
                    location=json.dumps(box["location"]),
                    controller_id=item['id'],
                    box_id_controller=box['id'],
                    phys=json.dumps(box["phys"]),
                    box_json=json.dumps(box))
                session.add(new_box)
                # count_phys = 0
                for phy in box["phys"]:
                    if phy['id'] not in [r for (a, r) in db_id_phy_id_list]:
                        new_phy = Phy(
                            name=phy["name"], type=phy["type"],
                            controller_id=item['id'],
                            phy_id_controller=phy['id'],
                            config=str(phy["config"]),
                            virtualInterfaceList=json.dumps([]),
                            phy_json=json.dumps(phy))
                        session.add(new_phy)

                        # count_phys += 1
                session.commit()
                # new_phy_id += count_phys
                # new_box_id += 1
            except IntegrityError as ex:
                session.rollback()

session.close()


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        logger.error("Impossible to read file", exc_info=True)
        return str(exc)


@app.route('/')
def root_page():
    # return render_template('proxy.html')
    return API_RESPONSE["OK"]["content"], API_RESPONSE["OK"]["code"]


@app.after_request
def flaskResponse(response):
    body = ""
    if response.get_data():
        response.headers["Content-Type"] = "application/json;charset=UTF-8"
        body = json.loads(response.get_data())
    log_content = " '{}' {} :code:{}:body:{}".format(
        request.method, request.path, response.status_code, body)
    logger.info(log_base.format(NORTHBOUND, RESPONSE, log_content))
    return response


@app.before_request
def before():
    # todo with request
    # e.g. print request.headers
    pass


# Topology API implementation
@app.route('/chunkete/topology', methods=['GET'])
def getChunketeTopology():
    resp = {
        "boxes": [],
        "links": []
    }
    log_content = ""
    logger.info(log_base.format(NORTHBOUND, REQUEST, log_content))
    for index_controller in range(len(controllers)):
        try:
            boxes = session.query(Box).filter(
                Box.controller_id == index_controller).all()
            (controller_resp,
             code) = controllers[index_controller].getChunketeTopology()
            log_content = "controller:{}:response:{}/{}".format(
                index_controller, code, controller_resp)
            logger.info(log_base.format(SOUTHBOUND, REQRESP, log_content))
            if code == API_RESPONSE["OK"]["code"]:
                for box in controller_resp["boxes"]:
                    for index_phy in range(len(box["phys"])):
                        phy = session.query(Phy).filter(
                            Phy.controller_id == index_controller).filter(
                                    Phy.phy_id_controller ==
                                    box["phys"][index_phy]["id"]
                                ).one()
                        box["phys"][index_phy]["id"] = phy.id
                        for db_box in boxes:
                            if db_box.box_id_controller == box["id"]:
                                box["id"] = db_box.id
                                break
                    resp["boxes"].append(box)
            else:
                return controller_resp, code
        except NoResultFound:
            return json.dumps({
                "timestamp": "2019-09-10T14:18:24.866+0000",
                "status": API_RESPONSE["NOTFOUND"]["code"],
                "error": API_RESPONSE["NOTFOUND"]["content"],
                "message": "No Result Found for the request",
                "path": request.path
            }), API_RESPONSE["NOTFOUND"]["code"]
        except IntegrityError:
            return errorResponder(
                "DB_INTEGRITY", "Database integrity error")
        finally:
            session.close()

    response = jsonify(resp)
    return response, API_RESPONSE["OK"]["code"]


@app.route(
    '/chunkete/topology/physicalInterface/<phy_id>/LTEConfig',
    methods=['PUT'])
def putInterfaceLTEConfig(phy_id):
    # {
    # "cellIdentity": 256,
    # "earfcndl": 41690,
    # "phyCellId": 5,
    # "prachrootseqindex": 100,
    # "primaryMMEAddress": "192.168.100.25",
    # "primaryMMEPort": 333,
    # "primaryPlmnId": "00101",
    # "refSignalPower": -40,
    # "reservedForOperatorUse": "not-reserved",
    # "trackingAreaCode": 67
    # }
    try:
        content = request.data
        content_dict = json.loads(content)
        log_content = "phy_id:{}:content:{}".format(phy_id, content_dict)
        logger.info(log_base.format(NORTHBOUND, REQUEST, log_content))

        if 0 > content_dict["cellIdentity"] > 256:
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        if content_dict["earfcndl"] not in [i for j in (
                range(2750, 3449),
                range(41690, 43489),
                range(37750, 38249)) for i in j]:
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        if 0 > content_dict["phyCellId"] > 500:
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        if 0 > content_dict["prachrootseqindex"] > 1023:
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        if "primaryMMEAddress" not in content_dict.keys():
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        if "primaryMMEPort" not in content_dict.keys():
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        if "primaryPlmnId" not in content_dict.keys():
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        if -40 > content_dict["refSignalPower"] > -10:
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        if content_dict["reservedForOperatorUse"] != "not-reserved":
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        if 0 > content_dict["trackingAreaCode"] > 65535:
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")

        if content:
            phy = session.query(Phy).filter(Phy.id == phy_id).one()
            response, code = controllers[phy.controller_id].\
                putInterfaceLTEConfig(
                    phy.phy_id_controller, content)
            log_content = "controller:{}:phy_id_controller:{}:phy_id:{}"
            log_content += ":content:{}:response:{}/{}".\
                format(
                    phy.controller_id, phy.phy_id_controller,
                    phy_id, content, code, response)
            logger.info(log_base.format(SOUTHBOUND, REQRESP, log_content))
            return jsonify(response), code
        else:
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")

    except KeyError:
        return errorResponder(
            "VERIFICATION_ERROR", "Malformed request")
    except NoResultFound:
        return errorResponder(
            "NOTFOUND", "Item not found")
    except IntegrityError:
        return errorResponder(
            "DB_INTEGRITY", "Database integrity error")
    finally:
        session.close()


@app.route(
    '/chunkete/topology/physicalInterface/<phy_id>/type/<phy_type>',
    methods=['PUT'])
def putInterfaceType(phy_id, phy_type):
    try:
        log_content = "phy_id:{}:phy_type:{}".format(phy_id, phy_type)
        logger.info(log_base.format(NORTHBOUND, REQUEST, log_content))
        phy = session.query(Phy).filter(Phy.id == phy_id).one()
        response, code = controllers[phy.controller_id].putInterfaceType(
            phy.phy_id_controller, phy_type)
        log_content = "controller:{}:phy_id_controller:{}:phy_id:{}"
        log_content += ":phy_type:{}:response:{}/{}".\
            format(
                phy.controller_id, phy.phyid_controller,
                phy_id, phy_type, code, response)
        logger.info(
            log_base.format(SOUTHBOUND, REQRESP, log_content))
        return response, code
    except NoResultFound:
        return errorResponder(
            "NOTFOUND", "Item not found")
    except IntegrityError:
        return errorResponder(
            "DB_INTEGRITY", "Database integrity error")
    finally:
        session.close()


@app.route(
    '/chunkete/topology/physicalInterface/<phy_id>/wiredConfig',
    methods=['PUT'])
def putInterfaceWiredConfig(phy_id):
    try:
        content = request.data
        log_content = "phy_id:{}:content:{}".format(
            phy_id, json.loads(content))
        logger.info(
            log_base.format(NORTHBOUND, REQUEST, log_content))
        if content:

            phy = session.query(Phy).filter(Phy.id == phy_id).one()
            response, code = controllers[phy.controller_id].\
                putInterfaceWiredConfig(
                    phy.phy_id_controller, content)
            log_content = "controller:{}:phy_id_controller:{}:phy_id:{}"
            log_content += ":response:{}/{}".\
                format(
                    phy.controller_id, phy.phy_id_controller,
                    phy_id, code, response)
            logger.info(
                log_base.format(SOUTHBOUND, REQRESP, log_content))
            return response, code
    except KeyError:
        return errorResponder(
            "VERIFICATION_ERROR", "Malformed request")
    except NoResultFound:
        return errorResponder(
            "NOTFOUND", "Item not found")
    except IntegrityError:
        return errorResponder(
            "DB_INTEGRITY", "Database integrity error")
    finally:
        session.close()


@app.route(
    '/chunkete/topology/physicalInterface/<phy_id>/wirelessConfig',
    methods=['PUT'])
def putInterfaceWirelessConfig(phy_id):
    # Verify content
    # {
    #     "channelBandwidth": 20,
    # (Se aceptan 20, 40 y 80)
    #     "channelNumber": 36,
    # (Se acepta cualquier canal de la banda de 2.4 y/o de la banda de 5GHz;
    # según el nodo puede o no sopotar DFS así que no está restringido
    # a canales "normales")
    #     "txPower": 2000
    # (Valor en mBm; se acepta desde 0 hasta 3500 aunque lo
    # normal suelen ser 2300)
    # }
    try:
        content = request.data
        log_content = "phy_id:{}:content:{}".format(
            phy_id, json.loads(content))
        logger.info(log_base.format(NORTHBOUND, REQUEST, log_content))

        content_dict = json.loads(content)

        if content_dict["channelBandwidth"] not in [20, 40, 80]:
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        if content_dict["channelNumber"] not in [i for j in (
                range(1, 11),
                range(36, 68, 4),
                range(100, 140, 4)) for i in j]:
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        if 0 >= content_dict["txPower"] > 3500:
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")

        if content:
            phy = session.query(Phy).filter(Phy.id == phy_id).one()
            response, code = controllers[phy.controller_id].\
                putInterfaceWirelessConfig(phy.phy_id_controller, content)
            log_content = "controller:{}:phy_id_controller:{}:phy_id:{}"
            log_content += ":content:{}:response:{}/{}".\
                format(
                    phy.controller_id, phy.phy_id_controller,
                    phy_id, content, code, response)
            logger.info(
                log_base.format(SOUTHBOUND, REQRESP, log_content))
            return jsonify(response), code
        else:
            return errorResponder(
                "VERIFICATION_ERROR", "Malformed request")
        return (API_RESPONSE["CREATED"]["content"],
                API_RESPONSE["CREATED"]["code"])
    except KeyError:
        logger.error("Malformed request")
        return errorResponder(
            "VERIFICATION_ERROR", "Malformed request")
    except NoResultFound:
        return errorResponder(
            "NOTFOUND", "Item not found")
    except IntegrityError:
        return errorResponder(
            "DB_INTEGRITY", "Database integrity error")
    finally:
        session.close()


# Chunk API implementation
@app.route('/chunkete/chunk', methods=['GET'])
def getAllChunks():
    log_content = ""
    logger.info(
        log_base.format(NORTHBOUND, REQUEST, log_content))
    # chunks = {}
    # chunk_id_list =[]
    response = []

    try:
        db_chunks = session.query(Chunk).all()

        for db_chunk in db_chunks:
            response.append(_dictChunk(db_chunk))

        return jsonify(response), API_RESPONSE["OK"]["code"]
    except NoResultFound:
        return errorResponder(
            "NOTFOUND", "Item not found")
    except IntegrityError:
        return errorResponder(
            "DB_INTEGRITY", "Database integrity error")
    finally:
        session.close()


@app.route('/chunkete/chunk', methods=['POST'])
def registerNewChunk():
    try:
        content = request.data
        log_content = "content:{}".format(json.loads(content))
        logger.info(log_base.format(NORTHBOUND, REQUEST, log_content))
        if content:
            chunk_dict = json.loads(content)
            controllers_phys = {}
            controllers_content = {}

        # Split the phys included in the chunk per controller
        for phy in chunk_dict["physicalInterfaceList"]:
            phy = session.query(Phy).filter(Phy.id == phy["id"]).one()
            phy_dict = json.loads(phy.phy_json)
            phy_id_dict = {"id": phy_dict["id"]}

            if phy.controller_id in controllers_phys.keys():
                controllers_phys[phy.controller_id].append(
                    phy.phy_id_controller)
                controllers_content[
                    phy.controller_id][
                        "physicalInterfaceList"].append(phy_id_dict)
            else:
                controllers_phys[phy.controller_id] = [phy.phy_id_controller]
                controllers_content[phy.controller_id] = {
                    "name": chunk_dict["name"],
                    "physicalInterfaceList": [phy_id_dict],
                }
                if "assignedQuota" in chunk_dict.keys():
                    controllers_content[phy.controller_id]["assignedQuota"] = \
                        chunk_dict["assignedQuota"]
                else:
                    chunk_dict["assignedQuota"] = 0
                    controllers_content[phy.controller_id]["assignedQuota"] = 0
                if "linkList" in chunk_dict.keys():
                    controllers_content[phy.controller_id]["linkList"] = \
                        chunk_dict["linkList"]
                else:
                    chunk_dict["linkList"] = []
                    controllers_content[phy.controller_id]["linkList"] = []
                if "serviceList" in chunk_dict.keys():
                    controllers_content[phy.controller_id]["serviceList"] = \
                        chunk_dict["serviceList"]
                else:
                    chunk_dict["serviceList"] = []
                    controllers_content[phy.controller_id]["serviceList"] = []

        # # Create a new chunk and add to database
        # # Get the next free ID in db
        # db_id_list = session.query(Chunk.id).all()
        # db_id_list = [r for (r, ) in db_id_list]
        # db_id_list.sort()
        # if len(db_id_list) == 0:
        #     new_chunk_id = 1
        # else:
        #     new_chunk_id = db_id_list[len(db_id_list)-1]+1

        # Add the chunk in the database
        chunk = Chunk(
            name=chunk_dict["name"],
            serviceList=json.dumps([]),
            assignedQuota=chunk_dict["assignedQuota"],
            controllers_phys=str(controllers_phys),
            phyList=str(
                [phy["id"] for phy in chunk_dict["physicalInterfaceList"]]
            ),
            linkList=json.dumps([]), chunk_json=json.dumps(chunk_dict))
        session.add(chunk)

        # Register the chunk on each of the controllers
        controllers_chunk_dict = {}
        for controller_id in controllers_content.keys():
            response, code = controllers[controller_id].registerNewChunk(
                json.dumps(controllers_content[controller_id]))
            log_content = "controller:{}:content:{}"
            log_content += ":response:{}/{}".\
                format(
                    controller_id,
                    json.dumps(
                        controllers_content[controller_id]),
                    code, response)
            logger.info(log_base.format(SOUTHBOUND, REQRESP, log_content))
            if code == API_RESPONSE["CREATED"]["code"]:
                controllers_chunk_dict[controller_id] = response["id"]
            else:
                return errorResponder(
                    "CONTROLLER", "Managed Controller returned an error")

        # Update Service in Database
        chunk_dict["id"] = chunk.id
        chunk.chunk_json = json.dumps(chunk_dict)
        chunk.controllers_chunk = str(controllers_chunk_dict)
        session.commit()
        return json.dumps(
            {'id': chunk.id}), API_RESPONSE["CREATED"]["code"]
    except KeyError:
        return errorResponder(
            "VERIFICATION_ERROR", "Malformed request")
    except NoResultFound:
        return errorResponder(
            "NOTFOUND", "Item not found")
    except IntegrityError:
        return errorResponder(
            "DB_INTEGRITY", "Database integrity error")
    finally:
        session.close()


@app.route('/chunkete/chunk/<chunk_id>', methods=['GET'])
def getChunkById(chunk_id):
    log_content = "chunk_id:{}".format(chunk_id)
    logger.info(
        log_base.format(NORTHBOUND, REQUEST, log_content))

    try:
        chunk = session.query(Chunk).filter(Chunk.id == chunk_id).one()

        response_data = _dictChunk(chunk)

        return jsonify(
            response_data), API_RESPONSE["OK"]["code"]
    except NoResultFound:
        return errorResponder(
            "NOTFOUND", "Object not found")
    except IntegrityError:
        return errorResponder(
            "DB_INTEGRITY", "Database integrity error")
    finally:
        session.close()


@app.route('/chunkete/chunk/<chunk_id>', methods=['DELETE'])
def removeExistingChunk(chunk_id):
    log_content = "chunk_id:{}".format(chunk_id)
    logger.info(log_base.format(NORTHBOUND, REQUEST, log_content))
    try:
        chunk = session.query(Chunk).filter(Chunk.id == chunk_id).one()
        session.close()
        controllers_phys = eval(chunk.controllers_phys)
        serviceList = eval(chunk.serviceList)

        # Remove the Services from the chunk
        while serviceList:
            removeExistingSWAMService(
                chunk_id, serviceList[0], interface=INTERNAL)
            serviceList.pop(0)

        for controller_id in controllers_phys.keys():
            response, code = controllers[controller_id].removeExistingChunk(
                eval(chunk.controllers_chunk)[controller_id])
            log_content = "controller:{}:chunk_id:{}"
            log_content += ":response:{}/{}".\
                format(controller_id, chunk_id, code, response)
            logger.info(log_base.format(SOUTHBOUND, REQRESP, log_content))

        # Remove the chunk from the database
        session.delete(chunk)
        session.commit()
        return API_RESPONSE["OK"]["content"], API_RESPONSE["OK"]["code"]
    except NoResultFound:
        return errorResponder("NOTFOUND", "Item not found")
    except IntegrityError:
        return errorResponder("DB_INTEGRITY", "Database integrity error")
    finally:
        session.close()


# Service API implementation
@app.route('/chunkete/chunk/<chunk_id>/service/SWAM', methods=['GET'])
def getAllSWAMServices(chunk_id):
    log_content = "chunk_id:{}".format(chunk_id)
    logger.info(log_base.format(NORTHBOUND, REQUEST, log_content))

    response = []

    try:
        db_chunk = session.query(Chunk).filter(Chunk.id == chunk_id).one()

        for service_id in eval(db_chunk.serviceList):
            db_service = session.query(Service).filter(
                Service.id == service_id).one()
            response.append(_dictService(db_service))

        return jsonify(response), API_RESPONSE["OK"]["code"]
    except NoResultFound:
        return errorResponder("NOTFOUND", "Item not found")
    finally:
        session.close()


@app.route('/chunkete/chunk/<chunk_id>/service/SWAM', methods=['POST'])
def registerNewSWAMService(chunk_id):
    # VERIFY CONTENT
    # {
    # "lteConfig": { (Más info en los mails que te he pasado de accelleran)
    #     "cellReserved": "not-reserved",
    #     "mmeAddress": "192.168.50.2",
    #     "mmePort": 333,
    #     "plmnId": "00101"
    # },
    # "selectedPhys": [
    # (Sólo se aceptan interfaces de tipo SUB6_ACCESS,
    # LTE_PRIMARY_PLMN y WIRED_TUNNEL)
    #     14, 23
    # ],
    # "vlanId": 201, (1-4095)
    # "wirelessConfig": {
    #     "encryption": "WPA", (NONE, WPA, WPA2, WEP aceptados)
    #     "password": "secret",
    # (No se aceptan espacios. Debe contener un mínimo de
    # 8 caracteres o estar vacia en caso de encryption == "NONE")
    #     "ssid": "Test" (No se aceptan espacios)
    # }
    # }
    PHY_TYPES = ["SUB6_ACCESS", "LTE_PRIMARY_PLMN", "WIRED_TUNNEL"]
    ENCRYPTION_TYPES = ["NONE", "WPA", "WPA2", "WEP"]

    # Action record for rollback in case something fails
    # {
    #   <controller>:{
    #                 "chunk_id": <service_id>
    #                 "service_id": <service_id>
    #               }
    # }
    rollback_flag = True
    rollback = {}

    try:
        content = request.data
        log_content = "chunk_id:{}:content:{}".format(
            chunk_id, json.loads(content))
        logger.info(log_base.format(NORTHBOUND, REQUEST, log_content))
        if content:
            service_dict = json.loads(content)

            # if "lteConfig" in service_dict.keys():
            if service_dict["lteConfig"]:
                pass
            else:
                service_dict["lteConfig"] = {
                    "cellReserved": None,
                    "mmeAddress": None,
                    "mmePort": None,
                    "plmnId": None
                }

            if "wirelessConfig" in service_dict.keys():
                if service_dict["wirelessConfig"]:
                    if service_dict["wirelessConfig"]["encryption"] not in \
                            ENCRYPTION_TYPES:
                        return errorResponder(
                            "VERIFICATION_ERROR", "Malformed request")
                    elif len(service_dict["wirelessConfig"]["password"]) < 8:
                        if service_dict[
                                "wirelessConfig"]["encryption"] != "NONE":
                            return errorResponder(
                                "VERIFICATION_ERROR", "Malformed request")
                    elif ' ' in service_dict["wirelessConfig"]["ssid"]:
                        return errorResponder(
                            "VERIFICATION_ERROR", "Malformed request")
            else:
                service_dict["wirelessConfig"] = {
                    "encryption": None,
                    "password": None,
                    "ssid": None
                }

            if 1 > service_dict["vlanId"] > 4095:
                return errorResponder(
                    "VERIFICATION_ERROR", "Malformed request")

            controllers_phys = {}
            controllers_content = {}
            controllers_xref = {}
            selected_vifs = []
            db_vifs = []

            chunk = session.query(Chunk).filter(Chunk.id == chunk_id).one()

            for phy_id in service_dict["selectedPhys"]:

                if phy_id not in eval(chunk.phyList):
                    return errorResponder(
                        "VERIFICATION_ERROR", "Malformed request")

                phy = session.query(Phy).filter(Phy.id == phy_id).one()

                if phy.type not in PHY_TYPES:
                    return errorResponder(
                        "VERIFICATION_ERROR", "Malformed request")

                if phy.controller_id in controllers_phys.keys():
                    controllers_phys[phy.controller_id].append(phy.id)
                    controllers_xref[phy.controller_id].append(
                        phy.phy_id_controller)
                    controllers_content[phy.controller_id]["selectedPhys"].\
                        append(phy.phy_id_controller)
                else:
                    controllers_phys[phy.controller_id] = [phy.id]
                    controllers_xref[phy.controller_id] = [
                        phy.phy_id_controller]
                    controllers_content[phy.controller_id] = {
                        "selectedPhys": [phy.phy_id_controller],
                        "vlanId": service_dict["vlanId"]
                    }
                    if "lteConfig" in service_dict.keys():
                        controllers_content[phy.controller_id]["lteConfig"] = \
                            service_dict["lteConfig"]
                    if "wirelessConfig" in service_dict.keys():
                        controllers_content[phy.controller_id][
                            "wirelessConfig"] = service_dict["wirelessConfig"]

                # Create a new vif and add to database
                # Get the next free ID in db
                # db_id_list = session.query(Vif.id).all()
                # db_id_list = [r for (r, ) in db_id_list]
                # db_id_list.sort()
                # if len(db_id_list) == 0:
                #     new_vif_id = 1
                # else:
                #     new_vif_id = db_id_list[len(db_id_list)-1]+1

                # Create a new service and add to database
                # Get the next free ID in db
                # db_id_list = session.query(Service.id).all()
                # db_id_list = [r for (r, ) in db_id_list]
                # db_id_list.sort()
                # if len(db_id_list) == 0:
                #     new_service_id = 1
                # else:
                #     new_service_id = db_id_list[len(db_id_list)-1]+1

                # TODO: Name the new vif. At the moment, it just takes the
                # phy name followed by the new_vif_id

                new_vif_dict = {
                    'id': str(uuid.uuid4()),
                    'name': "",
                    "toRootVlan": 0,
                    "toAccessVlan": 0,
                    "toAccessPort": 0,
                    "toRootPort": 0,
                    "openFlowPortList": []
                }
                new_vif_dict['name'] = "{}_{}".\
                    format(phy.name, new_vif_dict['id'])

                vif = Vif(
                    id=new_vif_dict['id'],
                    service_id="",
                    phy_id=phy.id,
                    controller_id=phy.controller_id,
                    vif_json=json.dumps(new_vif_dict))
                session.add(vif)
                db_vifs.append(vif)
                selected_vifs.append(new_vif_dict['id'])
                phy = session.query(Phy).filter(Phy.id == phy.id).one()
                virtualInterfaceList = json.loads(phy.virtualInterfaceList)
                virtualInterfaceList.append(vif.id)
                phy.virtualInterfaceList = json.dumps(virtualInterfaceList)
                phy_dict = json.loads(phy.phy_json)
                if "virtualInterfaceList" in phy_dict:
                    phy_dict["virtualInterfaceList"].append(new_vif_dict)
                else:
                    phy_dict["virtualInterfaceList"] = [new_vif_dict]
                phy.phy_json = json.dumps(phy_dict)

            # Add the service in the database
            service = Service(
                controllers_services=str({}),
                controllers_phys=str(controllers_xref),
                lteConfigCellReserved=service_dict[
                    "lteConfig"]["cellReserved"],
                lteConfigMMEAddress=service_dict["lteConfig"]["mmeAddress"],
                lteConfigMMEPort=service_dict["lteConfig"]["mmePort"],
                lteConfigPLMNId=service_dict["lteConfig"]["plmnId"],
                selectedPhys=str(service_dict["selectedPhys"]),
                selectedVifs=str(selected_vifs),
                wirelessConfigEncryption=service_dict[
                    "wirelessConfig"]["encryption"],
                wirelessConfigPassword=service_dict[
                    "wirelessConfig"]["password"],
                wirelessConfigSSID=service_dict["wirelessConfig"]["ssid"],
                vlanId=service_dict["vlanId"],
                service_json=json.dumps(service_dict)
            )

            vlan = Vlan(
                tag=service_dict["vlanId"],
                service_id="",
                controllers_vlans_id="")

            session.add(vlan)
            session.add(service)
            session.flush()

            # Update Chunk in database
            # update serviceList
            serviceList = json.loads(chunk.serviceList)
            serviceList.append(service.id)
            chunk.serviceList = json.dumps(serviceList)
            # update chunk json
            service_dict["id"] = service.id
            vlan.service_id = service.id
            for db_vif in db_vifs:
                db_vif.service_id = service.id
            updated_chunk = json.loads(chunk.chunk_json)
            updated_chunk["serviceList"].append(service_dict)
            chunk.chunk_json = json.dumps(updated_chunk)
            service.service_json = json.dumps(service_dict)
            session.flush()          

            # Register the service on each controller
            controllers_services_dict = {}
            for controller_id in controllers_phys.keys():
                data, code = controllers[controller_id].\
                    registerNewSWAMService(
                        eval(chunk.controllers_chunk)[controller_id],
                        json.dumps(controllers_content[controller_id]))
                log_content = "controller:{}:chunk_id:{}:content:{}"
                log_content += ":response:{}/{}".\
                    format(
                        controller_id, chunk_id,
                        json.dumps(controllers_content[controller_id]),
                        code, data)
                logger.info(log_base.format(
                    SOUTHBOUND, REQRESP, log_content))
                if code == API_RESPONSE["CREATED"]["code"]:
                    rollback[controller_id] = {
                        'chunk_id': eval(
                            chunk.controllers_chunk)[controller_id],
                        'service_id': data["id"]
                    }
                    controllers_services_dict[controller_id] = data["id"]
                else:
                    return errorResponder(
                        "CONTROLLER",
                        "Managed Controller returned an error")

            # Update and add vlan object
            # vlan.service_id = service.id
            # vlan.controllers_vlans_id = controllers_services_dict['vlanId']

            # Update Service in Database
            service.controllers_services = str(controllers_services_dict)
            session.commit()
            rollback_flag = False
            return json.dumps(
                {'id': service.id}), API_RESPONSE["CREATED"]["code"]
    except NoResultFound:
        return errorResponder(
            "NOTFOUND", "Item not found")
    except IntegrityError:
        return errorResponder(
            "DB_INTEGRITY", "Database integrity error")
    finally:
        if rollback_flag:
            if rollback:
                for controller_id in rollback.keys():
                    data, code = controllers[controller_id].\
                        removeExistingSWAMService(
                            rollback[controller_id]["chunk_id"],
                            rollback[controller_id]["service_id"])
                    log_content = "controller:{}:chunk_id:{}:service_id:{}"
                    log_content += ":response:{}/{}".\
                        format(
                            controller_id,
                            rollback[controller_id]["chunk_id"],
                            rollback[controller_id]["service_id"],
                            code, data)
                    logger.info(log_base.format(
                        SOUTHBOUND, ROLLBACK, log_content))
        session.close()


@app.route(
    '/chunkete/chunk/<chunk_id>/service/SWAM/<service_id>',
    methods=['GET'])
def getSWAMServiceById(chunk_id, service_id):
    log_content = "chunk_id:{}:service_id:{}".format(chunk_id, service_id)
    logger.info(log_base.format(NORTHBOUND, REQUEST, log_content))
    try:
        service = session.query(Service).filter(Service.id == service_id).one()

        response_data = _dictService(service)

        return jsonify(response_data), API_RESPONSE["OK"]["code"]

    except NoResultFound:
        return errorResponder(
            "NOTFOUND", "Item not found")
    except IntegrityError:
        return errorResponder(
            "DB_INTEGRITY", "Database integrity error")
    finally:
        session.close()


@app.route(
    '/chunkete/chunk/<chunk_id>/service/SWAM/<service_id>',
    methods=['DELETE'])
def removeExistingSWAMService(chunk_id, service_id, interface=NORTHBOUND):
    log_content = "chunk_id:{}:service_id:{}".format(chunk_id, service_id)
    logger.info(log_base.format(interface, REQUEST, log_content))
    controllers_phys = {}
    try:
        # Update Chunk in database
        chunk = session.query(Chunk).filter(Chunk.id == chunk_id).one()
        vifs = session.query(Vif).filter(
            Vif.service_id == service_id).all()

        for vif in vifs:
            phy = session.query(Phy).filter(Phy.id == vif.phy_id).one()
            if phy.controller_id in controllers_phys.keys():
                controllers_phys[phy.controller_id].append(phy.id)
            else:
                controllers_phys[phy.controller_id] = [phy.id]
            virtualInterfaceList = eval(phy.virtualInterfaceList)
            virtualInterfaceList.remove(vif.id)
            phy.virtualInterfaceList = json.dumps(virtualInterfaceList)
            session.delete(vif)

        chunk_dict = json.loads(chunk.chunk_json)
        serviceList = json.loads(chunk.serviceList)

        for index in range(len(serviceList)):
            if serviceList[index] == service_id:
                service = session.query(Service).filter(
                    Service.id == service_id).one()
                controllers_services_dict = eval(service.controllers_services)
                for controller_id in controllers_phys.keys():
                    response, code = controllers[controller_id].\
                        removeExistingSWAMService(
                            eval(chunk.controllers_chunk)[controller_id],
                            controllers_services_dict[controller_id])
                    log_content = "controller:{}:chunk_id:{}:service_id:{}"
                    log_content += ":service_id_controller:{}:response:{}/{}".\
                        format(
                            controller_id, chunk_id,
                            service_id,
                            controllers_services_dict[controller_id],
                            code, response)
                    logger.info(log_base.format(
                        SOUTHBOUND, REQRESP, log_content))

                chunk_dict["serviceList"].pop(index)
                serviceList.pop(serviceList.index(service_id))
                chunk.serviceList = json.dumps(serviceList)
                chunk.chunk_json = json.dumps(chunk_dict)

                vlan = session.query(Vlan).filter(
                    Vlan.service_id == service_id).one()
                session.delete(vlan)
                session.delete(service)

                session.commit()
                return (API_RESPONSE["OK"]["content"],
                        API_RESPONSE["OK"]["code"])
        return errorResponder(
            "NOTFOUND", "Item not found")
    except NoResultFound:
        return errorResponder(
            "NOTFOUND", "Item not found")
    except IntegrityError:
        return errorResponder(
            "DB_INTEGRITY", "Database integrity error")

    finally:
        session.close()


app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == '__main__':
    """main function
    Default host: 0.0.0.0
    Default port: 8080
    Default debug: False
    """
    try:
        app.run(
            host='0.0.0.0',
            port=8008,
            debug=False)

    except Exception:
        logging.critical(
            'server: CRASHED: Got exception on main handler')
        raise
