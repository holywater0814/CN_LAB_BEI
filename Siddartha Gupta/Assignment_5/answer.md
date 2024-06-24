Q)  What is the value of each of the header fields ? Explain why the value is what it is .


 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+  
 |Version|  IHL  |Type of Service|          Total Length         |  
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+  
 |         Identification        |Flags|      Fragment Offset    |  
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+  
 |  Time to Live |    Protocol   |         Header Checksum       |  
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+  
 |                       Source Address                          |  
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+  
 |                    Destination Address                        |  
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+  
 |                    Options                    |    Padding    |  
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+  
---

--> a. Version(4 bits) ,  value =4. The value 4 means that the ipversion is 4 i.e. IPv4.

--> b. Header Length <IHL> (4 bits) , value =5 . Indicates the number of 32-bit words in the header.
       5 means the header is 20 bytes long (5 * 4 bytes).

--> c. DSCP (6 bits) ,Value= 0x00 .  Value 0x00  indicates that all 6-bits in DCSP field set 0.A DSCP value 
    000000 is typically referred to as the Default Forwarding (DF) class. Traffic marked with DSCP 0x00 (DF) 
    does not get any priority over other traffic types and is treated with the lowest priority.


--> d. ECN (2 bits) , Explicit Congestion Notification (ECN) is an extension to the Internet Protocol (IP) and Transmission Control Protocol (TCP) that allows end-to-end notification of network congestion without dropping packets. Congestion in the context of networking refers to a situation where the demand for network resources exceeds the available capacity, leading to degraded network performance. ECN is congestion control mechanism in Network layer. Value =00 , This value indicates that the packet is not using ECN. It is not ECN-capable, and any network devices should not set or interpret ECN-related bits for this packet.
	  



--> e. Total Length (2 bytes) , Value =52 , This value indicates that the entire packet, including the header
       and data is 52 bytes long .

--> f. Identification (2 bytes), Value =0x0000, This value indicates that the identification value of the 
       packet is 0 . 

--> g. Flags (3 bits) , Value=0x2, Don't fragment. The value 0x2 identifies as Don't fragment.

--> h. Fragment Offset( 13 bits) , Value = 0, Indicates where in the datagram this fragment belongs , 0 means 
       not fragmented. 

--> i. TTL <Time to live> (1 byte) , Value=62 , Indicates it can pass through 62 routers before getting 
       discarded.  MacOS or GNU/Linux often use a default TTL of 64 which means packet has already passed 
	   through 2 routers in my case. 

--> j. Protocal (1 byte) , Value : TCP(6) , It means Transmission Control Protocal (UDP) is being used in the data portion of the IP packet. 

--> k. Header Checksum (2 bytes) , value : 0x650a, It indicates whether the sent packets and recieved packets 
       are same or not , if not same then some data is lost.

--> l. Source Address (4 bytes) , value: 34.107.234.93 , It indiates the ip address of the sender which means
       the packets is sent from the above ip address.

--> m. Destination Address (4 bytes), value: 192.168.1.73, It indicates the ip address of the receiver which 
       means our ip address is 192.168.1.73.


 


