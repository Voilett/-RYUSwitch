from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types


class SimpleSwitch(app_manager.RyuApp):
	# TODO define OpenFlow 1.0 version for the switch
	# add your code here


	def __init__(self, *args, **kwargs):
		super(SimpleSwitch, self).__init__(*args, **kwargs)
		self.mac_to_port = {}
    
    
	def add_flow(self, datapath, in_port, dst, src, actions):
		ofproto = datapath.ofproto

		match = datapath.ofproto_parser.OFPMatch(
            in_port=in_port,
            dl_dst=haddr_to_bin(dst), dl_src=haddr_to_bin(src))

		mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)
		# TODO send modified message out
		# add your code here

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def _packet_in_handler(self, ev):
		msg = ev.msg
		datapath = msg.datapath
		ofproto = datapath.ofproto

		pkt = packet.Packet(msg.data)
		eth = pkt.get_protocol(ethernet.ethernet)

		if eth.ethertype == ether_types.ETH_TYPE_LLDP:
			# ignore lldp packet
			return
		if eth.ethertype == ether_types.ETH_TYPE_IPV6:
			# ignore ipv6 packet
			return       
		
		dst = eth.dst
		src = eth.src
		dpid = datapath.id
		self.mac_to_port.setdefault(dpid, {})

		self.logger.info("packet in DPID:%s MAC_SRC:%s MAC_DST:%s IN_PORT:%s", dpid, src, dst, msg.in_port)

		# learn a mac address to avoid FLOOD next time.
		self.mac_to_port[dpid][src] = msg.in_port

		if dst in self.mac_to_port[dpid]:
			out_port = self.mac_to_port[dpid][dst]
		else:
			out_port = ofproto.OFPP_FLOOD

		# TODO define the action for output
		# add your code here


        # install a flow to avoid packet_in next time
		if out_port != ofproto.OFPP_FLOOD:
			self.logger.info("add flow s:DPID:%s Match:[ MAC_SRC:%s MAC_DST:%s IN_PORT:%s ], Action:[OUT_PUT:%s] ", dpid, src, dst, msg.in_port, out_port)
			self.add_flow(datapath, msg.in_port, dst, src, actions)

		data = None
		if msg.buffer_id == ofproto.OFP_NO_BUFFER:
			data = msg.data
        

		# TODO define the OpenFlow Packet Out
		# add your code here

	print ("PACKET_OUT...")
