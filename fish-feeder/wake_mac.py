import socket
import struct

def wake_on_lan(mac_address):
    # Validate MAC address format (should be in XX:XX:XX:XX:XX:XX format)
    if len(mac_address) == 17 and mac_address.count(":") == 5:
        # Remove colons from MAC address and convert it to bytes
        mac_bytes = bytes.fromhex(mac_address.replace(":", ""))
        
        # Construct the magic packet
        magic_packet = b'\xff' * 6 + mac_bytes * 16
        
        # Broadcast the packet to port 9 (common WoL port)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, ('255.255.255.255', 9))
        
        print(f"Wake-on-LAN packet sent to {mac_address}")
    else:
        raise ValueError("Invalid MAC address format. It should be in XX:XX:XX:XX:XX:XX format.")

# Example usage
#mac_address = "A8:20:66:4B:29:DA"  # Replace with your server's MAC address
#wake_on_lan(mac_address)



