# This Python script sends a ping packet flow from h1 to h2 nodes in an SDN network that contains only two hosts (i.e., h1 and h2), one switch (s1), and one controller.
# Tcpdump is used to sniff the packets at h2-eth0 interface. This script is part of a large project to measure the performance metrics of large-scale network.
# Author: Yaser Al Mtawa
# This code is for ilustrating purposes for Western Univserity, Course 4457. The students of this course can freely re-use it as long as they keep this description.


#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import time

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8',
                   host=CPULimitedHost,
                   link=TCLink)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    #print("Going to sleep for 10 seconds")
    #time.sleep(10)
    #c0 = RemoteController( 'c0', protocol='tcp', port= 6653) # this is for external Floodlight controller
    #net.addController(c0)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch)
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch)
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch)
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)

    info( '*** Add links\n')
    #adds a bidirectional link with bandwidth, delay and loss characteristics,
    #with a maximum queue size of 1000 packets using the Hierarchical Token Bucket rate limiter
    linkopts = dict(bw=15, delay='1ms', loss=1, max_queue_size=1000, use_htb=True)

    net.addLink(s1, h1, **linkopts)
    net.addLink(s1, s2, **linkopts)
    net.addLink(s2, s3, **linkopts)
    net.addLink(s3, s5, **linkopts)
    net.addLink(s5, s6, **linkopts)
    net.addLink(s6, h2, **linkopts)
    net.addLink(s1, s4, **linkopts)
    net.addLink(s2, s7, **linkopts)
    net.addLink(s7, s8, **linkopts)
    net.addLink(s8, h3, **linkopts)
    net.addLink(s7, s9, **linkopts)
    net.addLink(s9, s10, **linkopts)
    net.addLink(s10, s11, **linkopts)
    net.addLink(s11, s12, **linkopts)
    net.addLink(s12, h4, **linkopts)
    net.addLink(s10, h5, **linkopts)
    net.addLink(s9, s13, **linkopts)
    net.addLink(s13, s14, **linkopts)
    net.addLink(s14, h7, **linkopts)
    net.addLink(s14, h8, **linkopts)
    net.addLink(s13, h6, **linkopts)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])
    net.get('s6').start([c0])
    net.get('s7').start([c0])
    net.get('s8').start([c0])
    net.get('s9').start([c0])
    net.get('s10').start([c0])
    net.get('s11').start([c0])
    net.get('s12').start([c0])
    net.get('s13').start([c0])
    net.get('s14').start([c0])

    #CLI(net) # Opens up mininet terminal, use to run 'pingall'

    info( '*** Post configure switches and hosts\n')
    hosts = net.hosts
    server = hosts[ 6 ] # host[0] is h2
    outfiles, capfiles, errfiles = {}, {}, {}

    for h in hosts:
        #h.cmdPrint('IP address of', h) #, h.name.IP())
        outfiles[ h ] = './simpleNet/out/%s.out' % h.name # to store the output of ping command for client to server
        capfiles[ h ] = './simpleNet/cap/%s.txt' % h.name #cap file to store the output of tcpdump command
        errfiles[ h ] = './simpleNet/err/%s.err' % h.name

    newHosts = {hosts[ 1 ]}
    h7 = {hosts[ 6 ]} # set h1 as a ping sender, i.e., client
    h1 = {hosts[ 1 ]}

    serverHost = {hosts [ 6 ]}

    for h in serverHost:
        h.cmdPrint('tcpdump -n -i h7-eth0',
                 '>', capfiles[ h ],
                 '2>', errfiles[ h ],
                 '&' )


    print('IP address of the server is %s', server.IP())

    for h in newHosts:
    #ping -w option
    #This option sets the required running Time window value in second

        # Commented out call to 'ping' utility
        #h.cmdPrint('ping -w 80', server.IP(), # CHANGED: -w 20 => -w 40
        #         '>', outfiles[ h ],
        #         '2>', errfiles[ h ]
        #         )

        server.cmdPrint('iperf -s -u -p 5566 -i 10',
                       '>', outfiles[ h ],
                       '2>', errfiles[ h ],
                       '&' )
        bandwidth=6
        running_time=100
        h.cmd('iperf -c %s -u -b %sM -p 5566 -t %s' % (server.IP(),bandwidth, running_time))

    #CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
