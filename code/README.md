# Covert Storage Channel exploiting the Acknowledgment Number field in TCP (Code: CSC-PSV-TCP-AN)

# About Our Project
This project implements a **Covert Storage Channel** using the acknowledgment number field in TCP packets to transmit data in a covert way. The implementation focuses on manipulating this protocol field to encode binary data and decoding it at the receiver's end. The approach involves custom increment-based logic for encoding and decoding messages, leveraging the structure and functionality of TCP.

The project consists of two main functions, send and receive, facilitating the transmission and reception of covert messages. This implementation provides insights into covert communication techniques and their potential implications for network security.

# Methods that we used in our project

## Initialization (__init__)
* **Function Structure:**
    * The init function is simplified and uses a pass statement
    * Configuration values such as IP addresses, ports, and the base sequence number are provided as arguments during the execution of the send and receive functions, allowing dynamic configuration

## Custom Increment Logic (get_increment)
* The get_increment function determines the acknowledgment number increment for each bit or sequence of bits
* **Key Features:**
    * For Initial Bits:
        * Increment is 3 for the first 0
        * Increment is 17 for the first 1
    * For Subsequent Bits:
        * If the current bit matches the previous bit, the increment is straightforward
        * If the bits differ, the byte is reversed and additional calculations generate the increment

## Sending Data (send)
* **Parameters Configuration:**
    * dst_ip: Destination IP address
    * dst_port: Destination port
    * src_port: Source port
    * base_seq: Base sequence number
    * log_file_name: File name for logging the transmitted message
* **Message Processing:**
    * Generates a binary message
    * Processes it in 2-bit chunks
    * Logs the message for verification
* **Packet Operations:**
    * Calculates acknowledgment number increments for each bit chunk
    * Constructs TCP packets with updated acknowledgment numbers
    * Sends packets using super().send function
    * Implements 0.06 second delay between packets

## Receiving Data (receive)
* **Parameter Configuration:**
    * dst_port: Destination port to listen on
    * base_seq: Base sequence number
    * log_file_name: File name for logging
* **Packet Processing:**
    * Uses Scapy's sniff function for packet capture
    * Filters packets based on destination port
    * Analyzes acknowledgment number increments
    * Decodes 2-bit chunks using decode_increment
* **Message Handling:**
    * Collects decoded bits into bytes
    * Converts bytes to characters
    * Builds message until termination character (.) is found
* **Output Management:**
    * Saves reconstructed message to specified log file

# Configuration File
```json
{
  "covert_channel_code": "CSC-PSV-TCP-AN",
  "send": {
    "parameters": {
      "dst_ip": "172.18.0.3",
      "dst_port": 8505,
      "src_port": 8505,
      "base_seq": 1000,
      "log_file_name": "Example_UDPTimingInterarrivalChannelSender.log"
    }
  },
  "receive": {
    "parameters": {
      "dst_port": 8505,
      "base_seq": 1000,
      "log_file_name": "Example_UDPTimingInterarrivalChannelReceiver.log"
    }
  }
}
```
# Capacity 
```
Covert Channel Capacity: 24.53 bits/second
Message length: 128 bits
Transmission time: 5.44 seconds

```

