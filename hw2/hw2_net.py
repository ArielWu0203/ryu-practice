from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import RemoteController, OVSSwitch

def MininetTopo():
    net = Mininet()

    info("Create host nodes.\n")
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    info("Create switch node.\n")
    s1 = net.addSwitch('s1',switch = OVSSwitch,failMode = 'secure',protocols = 'OpenFlow13')

    info("Create Links.\n")
    net.addLink(h1,s1)
    net.addLink(h2,s1)

    info("Create Controller.\n")
    net.addController(name = 'c0',controller = RemoteController,ip = '127.0.0.1',port = 6633)

    info("Build and start network.\n")
    net.build()
    net.start()

    info("Run mininet CLI.\n")
    CLI(net)

if __name__ == '__main__':
    setLogLevel('info')
    MininetTopo()
