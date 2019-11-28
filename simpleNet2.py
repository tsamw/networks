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

    #c0 = RemoteController( 'c0', protocol='tcp', port= 6653) # this is for external Floodlight controller
    #net.addController(c0)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)

    info( '*** Add links\n')
    #adds a bidirectional link with bandwidth, delay and loss characteristics, 
    #with a maximum queue size of 1000 packets using the Hierarchical Token Bucket rate limiter
    linkopts = dict(bw=15, delay='1ms', loss=1, max_queue_size=1000, use_htb=True) 

    net.addLink(s1, h1, **linkopts)
    net.addLink(s1, h2, **linkopts)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')
    hosts = net.hosts
    server = hosts[ 0 ]
    outfiles, capfiles, errfiles = {}, {}, {}

    for h in hosts:
        #h.cmdPrint('IP address of', h) #, h.name.IP())
        outfiles[ h ] = './simpleNet/out/%s.out' % h.name # to store the output of ping command for client to server
        capfiles[ h ] = './simpleNet/cap/%s.txt' % h.name #cap file to store the output of tcpdump command
        errfiles[ h ] = './simpleNet/err/%s.err' % h.name
       
    newHosts = {hosts[ 1 ]} 
    h2 = {hosts[ 0 ]} # set h1 as a ping sender, i.e., client
    h1 = {hosts[ 1 ]} 

    serverHost = {hosts [ 0 ]} 

    for h in serverHost:
        h.cmdPrint('tcpdump -n -i h2-eth0',
                 '>', capfiles[ h ],
                 '2>', errfiles[ h ],
                 '&' )

    
    print('IP address of the server is %s', server.IP())

    for h in newHosts:
    #ping -w option
    #This option sets the required running Time window value in second
        h.cmdPrint('ping -w 20', server.IP(),
                 '>', outfiles[ h ],
                 '2>', errfiles[ h ]
                 )

        #server.cmdPrint('iperf -s -u -p 5566 -i 10',
     #                  '>', outfiles[ h1 ],
     #                  '2>', errfiles[ h1 ],
     #                  '&' )
    # bandwidth=6
    # running_time=100
    # src.cmd('iperf -c %s -u -b %sM -p 5566 -t %s' % (des.IP(),bandwidth, running_time)

    #CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

