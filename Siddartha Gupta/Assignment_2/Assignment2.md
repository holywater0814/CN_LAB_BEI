

## 1.Differenciate between OSI & TCP/IP model.


The differences between OSI & TCP/IP model are listed below:

| OSI | TCP/IP |
| ------ | ------ |
| OSI is the generic, protocal independent standard, acting as the communication gateway between the network and end user.| TCP/IP model is based on standard protocals around which the Internet is developed. It is a communication protocal, which allows connection of hosts over a network.  |
| It has 7 layers. | It has 4 layers. |
|It is vertically approached. | It is horizontally approached. |
|Delivery of the package is guaranteed in OSI Model. | Delivery of the package is not guaranteed in TCP/IP Model.|
|Replacement of tools and changes can easily be done in this model.| Replacing the tools is not easy as it is in OSI Model.|
|It is less reliable than TCP/IP Model.| It is more reliable than OSI Model. |

## 2.Differenciate between Peer to Peer architecture & Client Server architecture .

The differences between  Client-Server network architecture & Peer-to-Peer 
network architecture are: 
| CLient Server | Peer to Peer|
| ------ | ------ |
|In Client-Server Network, Clients and server are differentiated, Specific server and clients are present.|In Peer-to-Peer Network, Clients and server are not differentiated.|
|Client-Server Network focuses on information sharing. |While Peer-to-Peer Network focuses on connectivity. |
|In Client-Server Network, Centralized server is used to store the data.|While in Peer-to-Peer Network, Each peer has its own data.|
|In Client-Server Network, Server respond the services which is request by Client.|While in Peer-to-Peer Network, Each and every node can do both request and respond for the services.|
|Client-Server Network are costlier than Peer-to-Peer Network.|While Peer-to-Peer Network are less costlier than Client-Server Network.|
|Client-Server Network are more stable than Peer-to-Peer Network.|While Peer-to-Peer Network are less stable if number of peer is increase.|
|Client-Server Network is used for both small and large networks.|While Peer-to-Peer Network is generally suited for small networks with fewer than 10 computers.|


# 3.What are Seven layers of OSI model and write functions of each layers?

7 Layers of the OSI Model are mentioned below:

#### 1) Physical layer
---
- It is the bottom-most or the first layer of the OSI Model
- It comprises the raw data which is further transmitted to the higher layers of the structure
- Preparing the physical devices in the network and accepting the received data for transmission
- The termination of connection between two nodes of a network also takes place at this stage
- This layer converts the digital bits into electrical, radio, or optical signals
---

#### 2) Data Link Layer
---
- Access to get the data is achieved at this layer
- It breaks the input data into frames which makes analysing the data easier
- Ensures that the data received is free of any errors
-  It controls the flow of data in the stipulated time duration and along with a set speed of transmission
- The data is sent to the next layer in the form of packets which are then reviewed for further processing

---

#### 3) Network Layer

---
- It acts as a network controller
- Transferring of variable data from one node to another, connected in a network, takes place at this layer 
- Each node has a specific address and the network layer ensures that the data is sent to its destination address
- The data is sent in the form of fragments which are then connected to each other once the processing is done
---

#### 4) Transport Layer
---
- The delivery of data packets is managed by the transport layer
- It manages the flow of data, segmentation and desegmentation and error control
- There are five classes of the transport protocol, starting from 0 and continuing till 4 (TP0 to TP4)
- Fragmentation and reassembly of data packets occur that this stag
---

#### 5) Session Layer
---
- The connection between the computers connected in a network is managed at this layer
- Establishment, management and termination between the remote and local application takes place here
- Authentication and authorisation happen at this layer
- This layer can also terminate or end any session or transmission which is complete
---

#### 6) Presentation Layer
---
- The data is converted into the syntax or semantics which an application understands
- Before passing on the data any further, the data is formatted at this stage
 -Functions including compression, encryption, compatible character code set, etc. are also done at this layer of the model
- It serves as a data translator for the network
---

#### 7) Application Layer
---
- The interaction with the user or the user application takes place at this stage
- When identifying communication partners, the application layer determines the identity and availability of communication partners for an application with data to transmit
---

# What are the principles behind the OSI model ?

The OSI (Open Systems Interconnection) model is a conceptual framework used to understand and implement standard communication protocols in computer networks. It is divided into seven layers, each with specific functions. The principles behind the OSI model include:

####    Layered Architecture:
        - The model is divided into seven distinct layers, each responsible for different aspects of communication. This division allows for easier troubleshooting and development.

####    Separation of Concerns:
        - Each layer performs a specific function and interacts with the layers directly above and below it. This modular approach ensures that changes in one layer do not affect others.

####   Standardization:
        - By defining standard interfaces and protocols for each layer, the OSI model facilitates interoperability between different hardware and software systems.

####    Abstraction:
        - The OSI model abstracts the complex process of data communication into manageable pieces, allowing for clearer understanding and implementation.

####    Interoperability:
        - The model promotes the ability of different systems and organizations to work together by adhering to the same set of protocols and standards.

####    Encapsulation:
        - Data encapsulation occurs as information passes down the layers, with each layer adding its own header (and sometimes trailer) to the data. This ensures that each layer has the information needed to process the data correctly.

####    Layer Independence:
        - Each layer is designed to be independent, meaning changes or updates in one layer do not require changes in other layers. This separation simplifies development and enhances flexibility.




