import socket

def is_valid_ip(ip_addr):
    try:
        socket.inet_aton(ip_addr)
        return True
    except:
        return False