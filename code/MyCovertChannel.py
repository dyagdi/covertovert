from CovertChannelBase import CovertChannelBase
from scapy.all import IP, TCP, sniff
import random
import time

class MyCovertChannel(CovertChannelBase):
    """
    - You are not allowed to change the file name and class name.
    - You can edit the class in any way you want (e.g. adding helper functions); however, there must be a "send" and a "receive" function, the covert channel will be triggered by calling these functions.
    """
    def __init__(self):
        pass
    
    def get_increment(self, bit, previous_bits=""):
        if len(previous_bits) == 0:
            return 3 if bit == '0' else 17
            
        if len(previous_bits) < 8:
            byte_value = int(previous_bits, 2)
        else:
            byte_value = int(previous_bits[-8:], 2)
        if bit == previous_bits[-1]:
            increment = byte_value + 1
        else:
            reversed_bits = format(byte_value, '08b')[::-1]
            increment = int(reversed_bits, 2) + 3
        return increment

    def send(self, dst_ip, dst_port, src_port, base_seq, log_file_name):

        binary_message = self.generate_random_binary_message_with_logging(log_file_name)

        message_length = len(binary_message)
        
        start_time = time.time()
        current_ack = base_seq
        sent_bits = ""

        for i in range(0, len(binary_message), 2):
            chunk = binary_message[i:i+2]
            increment = self.get_increment(chunk[0], sent_bits)
            current_ack += increment
            sent_bits += chunk[0]
            increment = self.get_increment(chunk[1], sent_bits)
            current_ack += increment
            sent_bits += chunk[1]

            tcp_packet = IP(dst=dst_ip)/TCP(
                sport=src_port,
                dport=dst_port,
                flags="A",
                seq=base_seq,
                ack=current_ack
            )
            
            super().send(tcp_packet)
            time.sleep(0.06)

        end_time = time.time()
        transmission_time = end_time - start_time
        capacity = message_length / transmission_time
        print(f"Covert Channel Capacity: {capacity:.2f} bits/second")
        print(f"Message length: {message_length} bits")
        print(f"Transmission time: {transmission_time:.2f} seconds")

    def decode_increment(self, increment, previous_bits=""):
        if len(previous_bits) == 0:
            test_0_in_first_bit = 3
            test_1_in_first_bit = 17
            previous_bits_0 = previous_bits + '0'
            previous_bits_1 = previous_bits + '1'
            test_0_in_second_bit = self.get_increment('0', previous_bits_0)
            test_0_in_second_bit += test_0_in_first_bit
            test_0_in_second_bit_2 = self.get_increment('0', previous_bits_1)
            test_0_in_second_bit_2 += test_1_in_first_bit
            test_1_in_second_bit = self.get_increment('1', previous_bits_1)
            test_1_in_second_bit += test_1_in_first_bit
            test_1_in_second_bit_2 = self.get_increment('1', previous_bits_0)
            test_1_in_second_bit_2 += test_0_in_first_bit

            if increment == (test_0_in_second_bit):
                return '00'
            elif increment == (test_0_in_second_bit_2):
                return '10'
            elif increment == (test_1_in_second_bit):
                return '11'
            elif increment == (test_1_in_second_bit_2):
                return '01'
            else:
                return None
        
        test_0_in_first_bit = self.get_increment('0', previous_bits)
        test_1_in_first_bit = self.get_increment('1', previous_bits)
        previous_bits_0 = previous_bits + '0'
        previous_bits_1 = previous_bits + '1'
        test_0_in_second_bit = self.get_increment('0', previous_bits_0)
        test_0_in_second_bit += test_0_in_first_bit
        test_0_in_second_bit_2 = self.get_increment('0', previous_bits_1)
        test_0_in_second_bit_2 += test_1_in_first_bit
        test_1_in_second_bit = self.get_increment('1', previous_bits_1)
        test_1_in_second_bit += test_1_in_first_bit
        test_1_in_second_bit_2 = self.get_increment('1', previous_bits_0)
        test_1_in_second_bit_2 += test_0_in_first_bit

        if increment == (test_0_in_second_bit):
            return '00'
        elif increment == (test_0_in_second_bit_2):
            return '10'
        elif increment == (test_1_in_second_bit):
            return '11'
        elif increment == (test_1_in_second_bit_2):
            return '01'
        else:
            return None

    def receive(self, dst_port, base_seq, log_file_name):

        received_bits = ""
        prev_bits = ""
        last_ack = base_seq
        message = ""
        stop_char = '.'  
        
        while True:
            packets = sniff(
                filter=f"tcp and dst port {dst_port}",
                timeout=2,
                iface="eth0",
                count=1
            )
            
            if packets:
                if 'TCP' in packets[0]:
                    current_ack = packets[0]['TCP'].ack
                    
                    if current_ack <= last_ack: 
                        continue
                    
                    increment = current_ack - last_ack
                    last_ack = current_ack
                    
                    bits = self.decode_increment(increment, prev_bits)
                    if bits is not None:
                        received_bits += bits
                        prev_bits += bits

                        if len(received_bits) >= 8:
                            while len(received_bits) >= 8:
                                byte = received_bits[:8]
                                try:
                                    char = chr(int(byte, 2))
                                    message += char
                                    
                                    if char == stop_char:
                                        self.log_message(message, log_file_name)
                                        return
                                    
                                    received_bits = received_bits[8:]

                                except Exception as e:
                                    break
