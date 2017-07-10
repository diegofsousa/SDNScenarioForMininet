from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():
    '''
    Definicão dos componentes da Rede
    '''

    # Criação da rede
    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')


    info( '*** Adicionando controlador OpenFlow\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Adicionando switches\n')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Adicinando hosts\n')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)

    info( '*** Adicionando conexões entre os nós\n')
    net.addLink(s3, h5)
    net.addLink(s3, h4)
    net.addLink(s1, h3)
    net.addLink(s1, h2)
    net.addLink(s4, s3)
    net.addLink(s4, s2)
    net.addLink(s4, s1)
    net.addLink(h1, s2)
    net.addLink(s2, h6)

    info( '*** Criando a rede SDN\n')
    net.build()
    info( '*** Iniciando controlador\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Iniciando switches\n')
    net.get('s2').start([c0])
    net.get('s4').start([c0])
    net.get('s3').start([c0])
    net.get('s1').start([c0])

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

