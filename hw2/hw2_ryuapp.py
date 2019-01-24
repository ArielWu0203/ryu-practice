from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER,MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

class hw2_RyuApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self,*args,**kwargs):
        super(hw2_RyuApp,self).__init__(*args,**kwargs)

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

        req = parser.OFPPortStatsRequest(datapath,0,ofproto.OFPP_ANY)
        datapath.send_msg(req)

    # TODO : Reply request.
    @set_ev_cls(ofp_event.EventOFPPortStatsReply,MAIN_DISPATCHER)
    def port_states_reply_handler(self,ev):
        
        ports = []

        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        for stat in ev.msg.body : 
            if stat.port_no < ofproto.OFPP_MAX :
                ports.append(stat.port_no)
        #print(ports)

        match_1 = parser.OFPMatch(in_port = ports[0])
        match_2 = parser.OFPMatch(in_port = ports[1])
        action_1 = [parser.OFPActionOutput(port = ports[1])]
        action_2 = [parser.OFPActionOutput(port = ports[0])]
        self.add_flow(datapath,1,match_1,action_1)
        self.add_flow(datapath,1,match_2,action_2)
        
        
