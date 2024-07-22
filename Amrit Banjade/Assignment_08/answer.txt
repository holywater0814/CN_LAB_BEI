
# Connection Initialization , Maintenance, Termination of TCP 

1) Connection Establishment 
   TCP Connection Initializaiton ( Three Way Handshake) 
    a) SYN (Synchronize):The client sends a SYN packet to the server to initiate a connection. This packet
	   contains the client's initial sequence number (ISN).

	b) SYN-ACK (Synchronize-Acknowledge):The server responds with a SYN-ACK packet, acknowledging the client's
	   SYN and providing its own ISN.

	c) ACK (Acknowledge):The client sends an ACK packet back to the server, acknowledging the server's SYN-ACK.
	   The connection is now established.
   
   The first three frames shown in the picture tcpstream.png is the packets of TCP connection Initialization.

   a) **[SYN] Seq=0**,The client initiates the connection with a SYN packet and sets the initial sequence
      number (ISN) to 0. The SYN packet itself consumes 1 sequence number.

   b) **[SYN, ACK] Seq=0 Ack=1**, The server responds with a SYN-ACK packet. The server's sequence number is
       set to 0 (its ISN), and it acknowledges the client's SYN by setting the acknowledgment number to 1
	   (Ack=1). This is because the SYN packet from the client consumed 1 sequence number.

   c) **[ACK] Seq=1 Ack=1**, The client acknowledges the server's SYN-ACK by sending an ACK packet. The
       client's sequence number is incremented to 1 (Seq=1) to acknowledge the receipt of the server's SYN. The
       acknowledgment number is set to 1 (Ack=1) because it acknowledges the server's SYN, which consumed 1
       sequence number.

2) Connection Maintenance (Data Transfer) 
  Once the TCP connection is established, the client can send an HTTP request to the server and receive an
  HTTP response. On image tcpstream.png we can see that from frame 4 to 10 . 
  
  a) First the TCP window size is updated on frame number 4. 

  b) The http request is made by the client using GET method whose length is 493 bytes that means 493 bytes 
     transferred to server in frame 5.
  
  c) Which then Acknowledge by server by incrementing ACK=len+1=438([ACK] Seq=1 Ack=438), that means yes it
     heard 438 bytes by pushing the 174 bytes length data ([PSH][ACK] Seq=1 Ack=438 Len=174) to client. Again
	 which is acknowledge by client by incremneting ACK=len+1=175 and sequence number is set to 438([ACK]
	 Seq=438 Ack=175).

  d) After that server pushes the required data(line based text data: text/html technically index.html) which
     is of 929 bytes in total including http.

  e) Again client acknowledges it by incearsing Ack=len+1=930 ([ACK] Seq=438 Ack=930)

3) Connection Termination 
  After the http transaction the TCP connection is terminated. When terminating a TCP connection, a four-way
  handshake is typically used. This involves both sides sending and acknowledging FIN packets.


 a) [FIN, ACK] Seq=438 Ack=930 The client initiates the termination with a FIN packet. The sequence number
      is 438(data sent to server). The acknowledgment number is 930, acknowledging the data received from the
	  server.

 b) [ACK] Seq=930 Ack=439 The server acknowledges the client’s FIN packet by incrementing the acknowledgment
      number, Ack=ISN of client+1= 439. The server's sequence number is 930.

 c) **[FIN, ACK] Seq=930 Ack=439**Again, The server also initiates the termination with a FIN packet. The
     sequence number is 930(data sent to client). The acknowledgment number is 439, acknowledging the last
	 data received from the client including the FIN packet.

 d) [ACK] Seq=439 Ack=931 The client also acknowledges the server’s FIN packet by incrementing the
     acknowledgment number, Ack=ISN of server+1= 931. The client's sequence number is 439.



