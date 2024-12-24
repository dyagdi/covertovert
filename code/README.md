# Covert Storage Channel exploiting the Acknowledgment Number field in TCP (Code: CSC-PSV-TCP-AN)


## About Our Project:

This project implements a Covert Storage Channel using the acknowledgment number field in TCP packets to covertly transmit data. The implementation focuses on manipulating this protocol field to encode binary data and decoding it at the receiver’s end. The approach involves custom increment-based logic for encoding and decoding messages, leveraging the structure and functionality of TCP.

The project consists of two main functions, send and receive, which facilitate the transmission and reception of covert messages. This implementation provides insights into covert communication techniques and their potential implications in network security.

## Methods that we  used in our project:


Initialization (__init__):
	•	IP and Port Configuration:
The class initializes with predefined IP addresses (dst_ip and src_ip) and ports (dst_port and src_port).
	•	Base Sequence Number:
A base sequence number (base_seq) is set to start encoding the acknowledgment numbers. This is used as a reference for calculating subsequent acknowledgment values.

Custom Increment Logic (get_increment):
	•	The get_increment function calculates how much to increment the acknowledgment number based on the current bit (0 or 1) and the context of previous bits.
	•	Key Features:
	•	For the first bit, increments are set to 2 for 0 and 3 for 1.
	•	For subsequent bits, the increment depends on the value of the previous byte or the most recent 8 bits.
	•	If the current bit matches the previous bit, the increment is straightforward. Otherwise, the byte is reversed, and additional calculations are performed to generate the increment.

Sending Data (send):
	•	Message Preparation:
A binary message is generated and logged for testing purposes. The message is encoded bit by bit.
	•	Packet Construction:
For each bit, the acknowledgment number is incremented based on the get_increment function, and a TCP packet is constructed with the new acknowledgment number.
	•	Packet Transmission:
Each packet is sent using the super().send function from the base class, with a delay (0.05 seconds) to simulate transmission.
	•	Performance Logging:
The function calculates and logs:
	•	Covert channel capacity (bits/second).
	•	Total message length (in bits).
	•	Transmission time (in seconds).

Decoding Increment (decode_increment):
	•	The decode_increment function determines the bit (0 or 1) corresponding to a given acknowledgment increment, using the same logic as get_increment for consistency.
	•	It ensures that decoding at the receiver mirrors the encoding process used by the sender.

Receiving Data (receive):
	•	Packet Sniffing:
The function uses Scapy’s sniff function to capture incoming TCP packets that match the specified destination port.
	•	Increment Analysis:
For each captured packet, the acknowledgment number increment is calculated, and the corresponding bit is decoded using decode_increment.
	•	Message Reconstruction:
	•	Decoded bits are collected into bytes (8 bits each).
	•	Each byte is converted to a character and appended to the message.
	•	The function continues until a termination character (.) is detected, indicating the end of the message.
	•	Logging:
The reconstructed message is logged to a specified file ("Example_UDPTimingInterarrivalChannelReceiver.log").

## Configuration File

```python
{
  "covert_channel_code": "CSC-PSV-TCP-AN",
  "send": {
    "parameters": {
      "log_file_name": "Example_UDPTimingInterarrivalChannelSender.log"
    }
  },
  "receive": {
    "parameters": {
      "log_file_name": "Example_UDPTimingInterarrivalChannelReceiver.log"
    }
  }
}
```





