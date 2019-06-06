# RAN controller deployment

## 1. Prerequisites

The I2CAT's RAN controller (RACOON) requires an environment of at least:

- 16 GB of RAM
- 8 CPU (recommended)
- 50 GB of HD
- Ports opened: TCP:830, TCP:6640, TCP:8000, TCP:8008 and TCP:8181

The requirements are quite high since RACOON uses as one of its southbound API an OpenDaylight controller.

## 2. Features

RACOON has been developed as a RAN controller for the 5GCITY (H2020) european project and supports:

- Registration and management of I2CAT's wireless devices
- Registration and management of Accelleran's small cells
- Reservation and slicing of sub6 interfaces and LTE ENBs
- Deployment of multiple access points on the sub6 interfaces
- Deployment of multiple PLMNs on the LTE ENBs

## 3. Deployment

### 3.1. Dependencies

#### 3.1.1. General dependencies

- OpenVPN is usually required to establish a connection between the RAN controller and the managed nodes. OpenVPN is not mandatory if both the managed nodes are on the same local network or broadcast domain.
- A [Java SDK (version > 8)](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) is required to run both RACOON and NetconfManager components
- Two components (RACOON and NetconfManager) have been developed using the [spring boot](https://spring.io/) framework. The problem is that there can't be two running instances of the framework and therefore it is mandatory installing either Netconf Manager or RACOON components on a [linux container](https://linuxcontainers.org/) (lxc) or a similar environment (another option would be a [VirtualBox](https://www.virtualbox.org/) VM or even a OpenStack instance).

#### 3.1.2. Opendaylight

RACOON depends on a proprietary extension of OpenDaylight; to be precise requires the following bundles to be active:

- odl-ovsdb-southbound-impl-ui
- odl-ovsdb-ui
- odl-copserver

Since the odl-copserver bundle has been developed by I2CAT and is currently proprietary and non-licensed; a copy of the OpenDaylight BORON SR3 including the previously mentioned bundle can be found at https://drive.google.com/file/d/1g9-2Akoq8oOyBsB5SgY_MDtoLrKcsWU5 (Please contact the I2CAT foundation if not accessible).

To start OpenDaylight:

1. Decompress the `distribution-karaf-0.5.3-Boron-SR3.tar.gz`file
 
    ```sh
    tar -zxvf distribution-karaf-0.5.3-Boron-SR3.tar.gz
    cd distribution-karaf-0.5.3-Boron-SR3
    ```

2. Execute the `karaf`executable file:
 
    ```sh
    bin/karaf clean
    ```
3. Enable the required bundles on the OpenDaylight's CLI:

    ```sh
    opendaylight-user@root>feature:install odl-ovsdb-southbound-impl-ui
    opendaylight-user@root>feature:install odl-ovsdb-ui
    opendaylight-user@root>feature:install odl-copserver
    ```

### 3.1.3. Netconf Manager

This is the component responsible for the Netconf calls to the nodes. The component has been developed by I2CAT and is proprietary and non-licensed; a copy to the latest stable distribution of this software can be found at https://drive.google.com/file/d/1xcVciwj7eMQXCAK-1uMvfnfnzdtBqowQ (Please contact the I2CAT foundation if not accessible).

1. Download the `netconf-api-3.2.0.jar`file

2. To deploy this component just execute `java -jar netconf-api-3.2.0.jar`
 
### 3.2. RACOON deployment

This is the main component. This spring boot application has been developed by I2CAT and is proprietary and non-licensed; a copy to the latest stable distribution of this software can be found at https://drive.google.com/file/d/1eCSMPlESGOBD6-mALofYfUlke3WyedkK (Please contact the I2CAT foundation if not accessible). To install the controller:

1. Download the `api-1.0.0.jar` file

2. Execute `java -jar api-1.0.0.jar`

### 3.3. Checking the installation

The three components have their own front end which can be connected to in order to check if the installation process was successful.

- OpenDaylight (http://CONTROLLER_IP:8181/index.html): Should display a login page (default username is admin and password is admin as well)
- NetconfManager (http://CONTROLLER_IP:8000/swagger-ui.html): This should display a lot of entry points. If there are nodes present on the RACOON's topology executing the GET operations should display some more information and details about them.
- RACOON (http://CONTROLLER_IP:8008/swagger-ui.html): This should be similar to the Netconf Manager view; a lot of entry points. Executing the GET operations on an existing topology should display more information about the nodes and chunks present.

### 3.4. FAQ

Q: Either RACOON or Netconf Manager fails to start
A: As mentioned above, spring-boot applications can't be instantiated twice on the same computer; install one of the components in a linux container

Q: I installed a component on a linux container but the application is not responding
A: Configure IPTABLES to do a static nat to the application's appropriate port; for example, if Netconf Manager has been installed on a container the iptables command would look like this:

    ```sh
    iptables -t nat -A PREROUTING -p tcp -m tcp --dport 8000 -j DNAT --to-destination $CONTAINER_IP:8000
    ```

Q: No nodes appear on my topology after I install the controller and its components
A: The node detection has not been implemented on this version therefore the node MUST start the register process.

Q: The service deployment fails quite a lot
A: This is probably because a node is unstable. The best we can do to solve this issue is to restart OpenDaylight, RACOON and NetconfManager components and check the node's connectivity status towards the RAN controller.

Q: I have installed the different components on different hardware but every query to the RACOON returns a 500 error
A: This version does not support the distributed controller; all the components have to be installed on the same bare metal.
