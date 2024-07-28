## Introduction

When you enter "google.com" into your web browser, a complex series of interactions occurs within your computer and across the internet to retrieve and display the requested webpage. This process involves multiple layers of your operating system and network protocols working together seamlessly. Understanding what happens at each step provides insight into the mechanisms that enable web browsing. This detailed analysis will explore the journey of your request from the moment you hit enter until the Google homepage is displayed, highlighting the intricate processes and interactions that make accessing web content possible. We will use OSI model to study about this.



## Client side(sending data-requesting)

**Application Layer**
    Browser Request: You type google.com into your browser's address bar and hit enter.
    HTTP/HTTPS: The browser constructs an HTTP or HTTPS request to get the web page.


**Presentation Layer**
    Data Formatting: The browser ensures the data is in the correct format (e.g., encryption/decryption for HTTPS).
    SSL/TLS: If using HTTPS, SSL/TLS encryption is applied to the data.


**Session layer**
    Session Management: The browser and Google's server manage the session, ensuring data is exchanged in an organized manner.
    SSL/TLS Handshake: For HTTPS, a session is established via the SSL/TLS handshake to agree on encryption keys.

**Transport layer**
    TCP Connection: The browser uses the Transmission Control Protocol (TCP) to establish a connection with Google's server.
    Port Numbers: The browser uses port 80 for HTTP or port 443 for HTTPS.

**Network layer**
    IP Address Resolution:
        DNS Query: The browser checks its cache or sends a DNS query to resolve google.com to an IP address.
        DNS Response: The DNS server responds with the IP address of google.com.
    IP Routing: The browser constructs an IP packet with the destination IP address of Google's server.

**Data Link layer**
    MAC Address Resolution:
        ARP Request: If on a local network, the browser may send an ARP (Address Resolution Protocol) request to get the MAC address of the gateway router.
        ARP Response: The gateway responds with its MAC address.
    Frame Construction: The browser encapsulates the IP packet into an Ethernet frame with source and destination MAC addresses.

**Physical layer**
    Transmission: The frame is transmitted over the physical network medium (e.g., Ethernet cable, Wi-Fi).
    Signal Conversion: Electrical signals (or wireless signals) represent the data as it travels through the network.



### Detailed Layer Interactions

**Application to Presentation**
    Application Layer: "I want to send an HTTP GET request to google.com."
    Presentation Layer: "I will encrypt this HTTP request for secure transmission (if using HTTPS)."

**Presentation to Session**
    Presentation Layer: "Here is the encrypted HTTP request."
    Session Layer: "I will establish and manage a session for this communication."

**Session to Transport**
    Session Layer: "This session needs reliable data transfer."
    Transport Layer: "I will use TCP to ensure all packets are received correctly."

**Transport to Network**
    Transport Layer: "Here are the TCP segments."
    Network Layer: "I will route these packets to google.com's IP address."

**Network to Data Link**
    Network Layer: "Here are the IP packets with source and destination IP addresses."
    Data Link Layer: "I will create frames with MAC addresses for local network delivery."

**Data Link to Physical**
    Data Link Layer: "Here are the frames ready for transmission."
    Physical Layer: "I will convert these frames into signals and send them over the physical medium."



### Network Path

**Local Network:**
        The frame travels from your device to the local router or switch.

**ISP Network:**
        The router forwards the packet to your ISP, which routes it towards Google's data center.

**Internet Backbone:**
        The packet traverses multiple networks and routers on the internet, moving through various ISPs and backbones.

**Google's Network:**
        The packet reaches Google's data center, where their routers and switches direct it to the appropriate server.


## Server Side(receving data)


**Physical Layer**
    Reception: The server's network interface card (NIC) receives electrical, optical, or radio signals from the physical medium.
    Conversion: The Physical layer converts these signals into raw bitstreams (binary data) and passes them to the Data Link layer.

**Data Link Layer**
    Frame Reception: The Data Link layer reassembles the bitstream into frames.
    Error Checking: It checks for errors in the frames using methods like CRC.
    MAC Address Check: It verifies the destination MAC address to ensure the frame is meant for this server.
    Packet Extraction: It extracts the network layer packet from the frame and passes it to the Network layer.

**Network Layer**
    Packet Reception: The Network layer receives the packet.
    IP Address Check: It checks the destination IP address to ensure the packet is meant for this server.
    Routing: If the packet is meant for this server, it processes it; otherwise, it might be forwarded or dropped.
    Segment Extraction: It extracts the transport layer segment from the packet and passes it to the Transport layer.

**Transport layer**
    Segment Reception: The Transport layer receives the segment.
    Port Number Check: It checks the destination port number to determine which application should handle the data (e.g., port 80 for HTTP, port 443 for HTTPS).
    Error Checking and Flow Control: It ensures data integrity and manages flow control.
    Session Reassembly: It reassembles data segments into a complete message and passes it to the Session layer.

**Session layer**
    Session Reception: The Session layer receives the reassembled message.
    Session Management: It manages the state of the communication session, maintaining synchronization and orderly data exchange.
    Data Forwarding: It passes the session data to the Presentation layer.

**Presentation layer**
    Data Reception: The Presentation layer receives the session data.
    Decryption and Decompression: If the data is encrypted (e.g., HTTPS) or compressed, it decrypts and decompresses it.
    Data Formatting: It ensures the data is in a usable format for the application.
    Application Preparation: It passes the formatted data to the Application layer.

**Application Layer**
    Data Reception: The Application layer receives the formatted data.
    Processing: The web google server processes the request (e.g., handling an HTTP GET request for a web page).
    Response Generation: The server generates an appropriate response (e.g., HTML content for the requested web page).


## Server side(sending a respose)

**Application layer**
    Data Generation: The web server generates the response data (e.g., an HTML page).
    Data Passing: It passes the response data to the Presentation layer.


**Presentation layer**
    Data Formatting: The Presentation layer formats the data, compresses it, and encrypts it (if using HTTPS).
    Session Preparation: It prepares the data for the Session layer.
    Data Passing: It passes the formatted data to the Session layer.

**Session layer**
    Session Management: The Session layer manages the session state.
    Data Passing: It passes the data to the Transport layer.

**Transport layer**
    Segment Generation: The Transport layer segments the data into smaller chunks.
    Port Assignment: It assigns the appropriate port number (e.g., 80 for HTTP, 443 for HTTPS).
    Error Checking and Flow Control: It ensures data integrity and controls the flow.
    Data Passing: It passes the segments to the Network layer.


**Network layer**
    Packet Generation: The Network layer encapsulates the segments into packets.
    IP Address Assignment: It assigns the source and destination IP addresses.
    Routing: It determines the best route for the packets to reach the client.
    Data Passing: It passes the packets to the Data Link layer.

**Data Link layer**
    Frame Generation: The Data Link layer encapsulates the packets into frames.
    MAC Address Assignment: It assigns the source and destination MAC addresses.
    Error Checking: It adds error-checking information to the frames.
    Data Passing: It passes the frames to the Physical layer

**Physical layer**
    Transmission: The Physical layer converts the frames into electrical, optical, or radio signals.
    Signal Sending: It transmits the signals over the physical medium (e.g., cables, wireless).


## Client-side(receving data-return path)
When data is received, each layer processes the incoming data and passes it up to the next higher layer:

**Physical Layer**: Receives signals, converts them into frames, and passes them to the data link layer.

**Data Link Layer**: Verifies frames, extracts packets, and sends them to the network layer.

**Network Layer**: Processes packets, determines the appropriate transport layer segment, and passes data up.

**Transport Layer**: Reassembles segments into a complete message, checks for errors, and sends data to the session layer.

**Session Layer**: Manages the session state and passes the data to the presentation layer.

**Presentation Layer**: Decrypts, decompresses, and formats the data for the application layer.

**Application Layer**: Processes the received data and presents it to the user (e.g., displaying a web page in a browser).

