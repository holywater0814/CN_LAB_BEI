# Connection, Maintenance and Termination of TCP 


<img src="images/Screenshot from 2024-07-22 18-21-27.png">



---

*Sequence Numbers(ISN): Increment based on the number of bytes sent.SYN, SYN-ACK, ACK: Each of these packets consumes 1 sequence number.  Data Packets: Sequence numbers increment by the length of the data (in bytes) being sent.*

*Acknowledgment Numbers: Increment based on the number of bytes received and acknowledge the receipt of data.*

---
### Connection Establishment

##### TCP Connection Initialization (Three-Way Handshake)

1) **SYN (Synchronize)**:The client sends a SYN packet to the server to initiate a connection. This packet   contains the client's initial sequence number (ISN).

2) **SYN-ACK (Synchronize-Acknowledge)**:The server responds with a SYN-ACK packet, acknowledging the client's SYN and providing its own ISN.

3) **ACK (Acknowledge)**:The client sends an ACK packet back to the server, acknowledging the server's SYN-ACK. The connection is now established.

The first three frame shown in the picture above is the packets of TCP connection

1) `**[SYN] Seq=0**`,The client initiates the connection with a SYN packet and sets the initial sequence number (ISN) to 0. The SYN packet itself consumes 1 sequence number.

2) `**[SYN, ACK] Seq=0 Ack=1**`, The server responds with a SYN-ACK packet. The server's sequence number is set to 0 (its ISN), and it acknowledges the client's SYN by setting the acknowledgment number to 1 (Ack=1). This is because the SYN packet from the client consumed 1 sequence number.

3) `**[ACK] Seq=1 Ack=1**`, The client acknowledges the server's SYN-ACK by sending an ACK packet. The client's sequence number is incremented to 1 (Seq=1) to acknowledge the receipt of the server's SYN. The acknowledgment number is set to 1 (Ack=1) because it acknowledges the server's SYN, which consumed 1 sequence number.

---

### Connection Maintenance(Data transfer)

Once the TCP connection is established, the client can send an HTTP request to the server and receive an HTTP response. As you can see in the picture above from frame 7 to 12.

1) The http request is made by the client using GET method whose length is 677 bytes that means 677 bytes transferred to server in frame 7.

2) Which then Acknowledge by server by incrementing ACK=len+1=678(**`[ACK] Seq=1 Ack=678`**), that means yes it heard 677 bytes by pushing the 176 bytes length data (**`[PSH][ACK] Seq=1 Ack=678 Len=176`**) to client. Again which is acknowledge by client by incremneting ACK=len+1=177 and sequence number is set to 678(**`[ACK] Seq=678 Ack=177`**).

3) After that server pushesh the required data(line based text data: text/html *technically index.html*) which is of 1321 bytes in total including http.

4) Again client acknowledges it by incearsing Ack=len+1=1322 (**`[ACK] Seq=678 Ack=1322`**)

---
### Connection termination

After the http transaction the TCP connection is terminated. When terminating a TCP connection, a four-way handshake is typically used. This involves both sides sending and acknowledging FIN packets.


1) **`[FIN, ACK] Seq=678 Ack=1322`** The client initiates the termination with a FIN packet. The sequence number is 678(data sent to server). The acknowledgment number is 1322, acknowledging the data received from the server.

2) **`[ACK] Seq=1322 Ack=679`** The server acknowledges the client’s FIN packet by incrementing the acknowledgment number, Ack=ISN of client+1= 679. The server's sequence number is 1322.

3) **`[FIN, ACK] Seq=1322 Ack=679`**Again, The server also initiates the termination with a FIN packet. The sequence number is 1322(data sent to client). The acknowledgment number is 679, acknowledging the last data received from the client including the FIN packet.

4) **`[ACK] Seq=679 Ack=1323`** The client also acknowledges the server’s FIN packet by incrementing the acknowledgment number, Ack=ISN of server+1= 1323. The client's sequence number is 679.





