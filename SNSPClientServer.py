# Site-local Network Service Protocol (SNSP) Client-server combination.

import socket
import struct
import json
from ipaddress import ip_address

# TODO: Fix selecting non-primary networks
# TODO: Add IPv6

VERSION = "0.01"

PORT = 81

SOURCE_IP4 = False # False means use the default interface
SITE_LOCAL_IP4 = "<broadcast>"

def NewSNSPMessage(service_name, service_port, host_addr, message, version = VERSION):
	"""
	Create a new SNSP message.
	"""
	if not isinstance(service_name, str):
		raise ValueError("service_name was not a string.")
		
	if not isinstance(version, str):
		raise ValueError("version was not a string.")
		
	if not isinstance(service_port, int):
		raise ValueError("service_port was not an integer.")
		
	try:
		ip_address(host_addr) # If the address is not really an address, this will fail.
	except ValueError:
		raise ValueError("Address was not a valid IP address.")	
	messagedict = {'version' : version, 'service_name' : service_name, 'service_port' : service_port, 'host_addr' : host_addr, 'message' : message} # TODO: Finish this!!
	return messagedict
	
def set_network(source_ip, dest_ip):
	'''
	Change our default source IP and destination IP
	'''
	global SOURCE_IP4
	global SITE_LOCAL_IP4
	SOURCE_IP4 = source_ip
	SITE_LOCAL_IP4 = dest_ip
	
def reset_network():
	'''
	Reset the network settings to the default
	'''
	SOURCE_IP4 = False # False means use the default interface
	SITE_LOCAL_IP4 = "<broadcast>"
	
def setup_sockets(port=PORT):
	"""
	Set up sockets for TX/RX
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	if isinstance(SOURCE_IP4, str):
		print("Setting up socket with a changed network.")
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(SOURCE_IP4))
	return sock
		
def teardown_sockets(sock):
	"""
	Tear down our sockets.
	"""
	sock.shutdown()
	sock.close()
		
def SNSP_send(sock, message):
	"""
	Send an SNSP message to all the addresses we have.
	"""
	print("Sending to " + SITE_LOCAL_IP4)
	sock.sendto(bytes(json.dumps(message), 'utf-8'), (SITE_LOCAL_IP4, PORT))
	
	
def SNSP_listen(sock, buf_size=4096):
	"""
	Wait for and return SNSP messages.
	"""
	sock.bind(("", PORT))
	while True:
	    data, addr = sock.recvfrom(0x100)
	    print("received from {0}: {1!r}".format(addr, data))
	
def SNSP_parse(serial_packet):
	"""
	Parse a packet into a dict
	"""
	if not isinstance(packet, str):
		raise ValueError("Tried to SNSP_parse a non-string")
	return json.loads(serial_packet)
	

def __SNSP_serial_print(message):
	print(json.dumps(message))
	
	
	
	
	