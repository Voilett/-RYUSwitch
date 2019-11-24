from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4


class SimpleSwitch(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

	def __init__(self, *args, **kwargs):
		super(SimpleSwitch, self).__init__(*args, **kwargs)

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def _packet_in_handler(self, ev):
		msg = ev.msg
		datapath = msg.datapath
		ofproto = datapath.ofproto

		pkt = packet.Packet(msg.data)
		eth = pkt.get_protocol(ethernet.ethernet)
     
		if eth.ethertype == ether_types.ETH_TYPE_LLDP:
			#ignore lldp packet
			return
		if eth.ethertype == ether_types.ETH_TYPE_IPV6:
			#ignore ipv6 packet
			return
  
		print ("PACKET_IN:")

		print (eth.ethertype)
		print ("ethernet:")
		print ("eth_src=",eth.src)
		print ("eth_dst=",eth.dst)

		if eth.ethertype == ether_types.ETH_TYPE_IP:
			_ipv4 = pkt.get_protocol(ipv4.ipv4)
			print ("ipv4:")
			print ("ip_src=",_ipv4.src)
			print ("ip_dst=",_ipv4.dst)
           

		dpid = datapath.id

		out_port = ofproto.OFPP_FLOOD
		actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

		data = None

		out = datapath.ofproto_parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,  actions=actions, data=data)
		datapath.send_msg(out)
		print ("PACKET_OUT...")
		print


