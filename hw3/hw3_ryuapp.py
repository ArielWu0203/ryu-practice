from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER,MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ofproto_v1_3_parser
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import lldp
from ryu.lib.packet import packet

class hw3_RyuApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    lldp_struct = {}

    def __init__(self,*args,**kwargs):
        super(hw3_RyuApp,self).__init__(*args,**kwargs)

    # TODO : Add rules.
    def add_flow(self,datapath,priority,match,actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        mod = parser.OFPFlowMod(datapath = datapath,priority = priority,match = match,instructions = inst)
        datapath.send_msg(mod)

    # TODO : Request switch's port.
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures,CONFIG_DISPATCHER)
    def switch_features_handler(self,ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPPortDescStatsRequest(datapath,0)
        datapath.send_msg(req)

    # TODO : Reply request.
    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply,MAIN_DISPATCHER)
    def port_states_reply_handler(self,ev):
        
        ports = []

        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # TODO: LLDP to CP rule.
        match = parser.OFPMatch(eth_type = ether_types.ETH_TYPE_LLDP)
        action = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath,1,match,action)

        for stat in ev.msg.body : 
            if stat.port_no < ofproto.OFPP_MAX :
                ports.append(stat.port_no)
                self.send_lldp(datapath,stat.port_no,stat.hw_addr)
                
        if len(ports) == 2:
            match_1 = parser.OFPMatch(in_port = ports[0])
            match_2 = parser.OFPMatch(in_port = ports[1])
            action_1 = [parser.OFPActionOutput(port = ports[1])]
            action_2 = [parser.OFPActionOutput(port = ports[0])]
            self.add_flow(datapath,1,match_1,action_1)
            self.add_flow(datapath,1,match_2,action_2)
        
    @set_ev_cls(ofp_event.EventOFPPacketIn,MAIN_DISPATCHER)
    def packet_in_handler(self,ev):
        # TODO : handle lldp packet.
        datapath = ev.msg.datapath
        pkt = packet.Packet(data = ev.msg.data)
        pkt_ether = pkt.get_protocol(ethernet.ethernet)
        if not pkt_ether:
            return
        lldp_pkt = pkt.get_protocol(lldp.lldp)
        if lldp_pkt:
            self.lldp_struct.setdefault(datapath.id,{})
            self.lldp_struct[datapath.id].setdefault(ev.msg.match['in_port'],[lldp_pkt.tlvs[0].chassis_id,lldp_pkt.tlvs[1].port_id])
            print (self.lldp_struct)

    def send_lldp(self,datapath,port_no,hw_addr):
        ofproto = datapath.ofproto
        pkt = packet.Packet()
        pkt.add_protocol(ethernet.ethernet(ethertype = ether_types.ETH_TYPE_LLDP,src = hw_addr,dst = lldp.LLDP_MAC_NEAREST_BRIDGE))
        chassis = lldp.ChassisID(subtype = lldp.ChassisID.SUB_LOCALLY_ASSIGNED,chassis_id = str(datapath.id))
        port = lldp.PortID(subtype = lldp.PortID.SUB_LOCALLY_ASSIGNED,port_id = str(port_no))
        ttl = lldp.TTL(ttl = 10)
        end = lldp.End()
        tlvs = (chassis,port,ttl,end)
        pkt.add_protocol(lldp.lldp(tlvs))
        pkt.serialize()

        data = pkt.data
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionOutput(port = port_no)]
        out = parser.OFPPacketOut(datapath = datapath,buffer_id = ofproto.OFP_NO_BUFFER,in_port = ofproto.OFPP_CONTROLLER,actions = actions,data = data)
        datapath.send_msg(out)
