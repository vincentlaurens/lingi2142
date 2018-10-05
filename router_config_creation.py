#!/usr/bin/env python3
import json
import os
import sys
import stat

# from pprint import pprint

from constants import PREFIXES, PATH, VLAN_USES

with open(PATH+'router_configuration.json') as data_file:
    data = json.load(data_file)
    
  ######################## #################router_start config ################################################

    router_start_config = open(PATH+"project_cfg/"+router+"_start", "w")
    router_start_config.write("#!/bin/bash \n\n")
    router_start_config.write("# This file has been generated automatically, see router_config_creation.py for details. \n\n")
    
    
    ######################
    # Router BIRD config #
    ######################

    router_sysctl_config = open(PATH+"project_cfg/"+router+"/sysctl.conf", "w")
    router_sysctl_config.write("""
    net.ipv6.conf.all.disable_ipv6=0
    net.ipv6.conf.all.forwarding=1
    net.ipv6.conf.default.disable_ipv6=0
    net.ipv6.conf.default.forwarding=1
    """)
    router_sysctl_config.close()

    router_bird_config = open(PATH+"project_cfg/"+router+"/bird/bird6.conf", "w")
    router_bird_config.write("router id 0.0.0."+configs["router_id"]+"; \n\n")

    # log
    router_bird_config.write("""log "/etc/log/bird_log" all; \n""")
    router_bird_config.write("debug protocols all; \n")

    router_bird_config.write("""
    protocol kernel {
        learn;
        scan time 20;
        export all;
    }
    protocol device {
        scan time 10;
    }
    """)


    # Creation of a default prefix to be advertised to ISPs and BGP peers.
    # It is useful when a prefix provided by an ISP is advertised to another BGP peer.
    #
    # 'default_bgp_prefix_to_advertise' must exist if no 'prefix_to_advertise'
    # is defined for an isp or a bgp_peer
    if "default_bgp_prefix_to_advertise" in configs:
        router_bird_config.write("""
        protocol static static_default_bgp_out{
           import all;
           route """+configs["default_bgp_prefix_to_advertise"]+""" reject;
        }
        """)

    if(any(configs["isp"])):
        default_routes = []
        for isp, isp_configs in configs["isp"].items():
            # propagating default route to OSPF
            default_routes += "route ::/0 via "+isp_configs["peer_address"]+"; \n"

            export_bgp_prefix_name = "static_default_bgp_out"

            # Creation of a specific prefix to advertise for this ISP
            if "prefix_to_advertise" in isp_configs:
                export_bgp_prefix_name = "static_bgp_out_"+isp_configs["name_bgp"]
                router_bird_config.write("""
                protocol static static_bgp_out_"""+isp_configs["name_bgp"]+"""{
                   import all;
                   route """+isp_configs["prefix_to_advertise"]+""" reject;
                }
                """)

            # BGP peering with ISP
            router_bird_config.write("""
            protocol bgp """+isp_configs["name_bgp"]+""" {
                local as 3;
                neighbor """+isp_configs["peer_address"]+""" as """+isp_configs["asn"]+""";
                export where proto = \""""+export_bgp_prefix_name+"""";
                import filter {
                    if(net = ::/0) then {
                        accept;
                    }
                    reject;
                };
            }
            """)

        # OSPF
        router_bird_config.write("""
        protocol static static_ospf {
           import all;
           """)

        for route in default_routes:
            router_bird_config.write(route)

        # OSPF Hello message sent with 1 second interval
        # Stub 1 is used on interfaces to disable OSPF them
        router_bird_config.write("""
        }
        protocol ospf {
            import all;
            export where proto = "static_ospf";
            area 0.0.0.0 {
                interface "*eth*" {
                    hello 1;
                    dead 3;
                };
                interface "*lan*" {
                   stub 1;
                };
                interface "lo" {
                   stub 1;
                };
            };
        }
        """)

    # router without ISP
    else:
        router_bird_config.write("""
        protocol ospf {
            area 0.0.0.0 {
                interface "*eth*" {
                    hello 1;
                    dead 3;
                };
                interface "*lan*" {
                   stub 1;
                };
                interface "lo" {
                   stub 1;
                };
            };
        }
        """)

    # Configuration for BGP peers that are not ISPs
    if(any(configs["bgp_peers"])):
        for peer, peer_configs in configs["bgp_peers"].items():

            # Default prefix to be advertise to the BGP peer
            # 'default_bgp_prefix_to_advertise' must be declare as field in the json for this router
            export_bgp_prefix_name = "static_default_bgp_out"

            # Creation of a specific prefix to advertise for this ISP
            if "prefix_to_advertise" in peer_configs:
                export_bgp_prefix_name = "static_bgp_out_"+peer_configs["name_bgp"]
                router_bird_config.write("""
                protocol static """+export_bgp_prefix_name+"""{
                   import all;
                   route """+peer_configs["prefix_to_advertise"]+""" reject;
                }
                """)

            # Creation of a filter for the prefixes that are advertised by the BGP peer
            # and creation of the BGP protocol
            router_bird_config.write("""
            filter bgp_in_"""+peer+"""
            {
                if(net ~ ["""+peer_configs["accepted_prefix"]+"""+]) then
                {
                    accept;
                }
                reject;
            }
            protocol bgp """+peer+""" {
                local as 3;
                neighbor """+peer_configs["peer_address"]+""" as """+peer_configs["asn"]+""";
                export where proto = \""""+export_bgp_prefix_name+"""";
                import filter bgp_in_"""+peer+""";
            }
            """)


router_bird_config.close()

    

