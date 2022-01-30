# import netmiko to handle the SSH connection to the device as well as the connection handler itself
# Import logging to display debugging information regarding the SSH connection to the device
import logging
import pprint
import sys
from getpass import getpass

import netmiko

# import textfsm to parse the text that the cli will give us
import textfsm
from netmiko import ConnectHandler

# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# from TestBed.ArubaTests.arubatestlib import *
import arubatestlib.py
import yaml

print("Please enter the IP address of the rw1 device:")
aruba_rw1 = input()
print("Please enter the IP address of the rw2 device:")
aruba_rw1 = input()
print("Please enter the username you would like to use:")
aruba_username = input()
print("Please enter your password:")
aruba_password = input()
# aruba_password = getpass.getpass()


"""
rw1 = ConnectHandler(device_type='aruba_os', ip=aruba_rw1, username=aruba_username, password=aruba_password,
                     secret=aruba_password)
rw2 = ConnectHandler(device_type='aruba_os', ip=aruba_rw2, username=aruba_username, password=aruba_password,
                     secret=aruba_password)
"""

# Open the variable file and parse its contains
with open("variables.var") as f:
    variable_data = yaml.load(f, Loader=yaml.FullLoader)

# Input check #TODO expand the checks
if not variable_data["master_ip"]:
    print("Unable to load the master_ip from the variable file. Terminating program")
    exit()
elif not variable_data["local_ip"]:
    print("Unable to load the local_ip from the variable file. Terminating program")
    exit()

# Open a connection with the controllers from the var file
rw1 = ConnectHandler(
    device_type="aruba_os",
    ip=variable_data["master_ip"].split("/")[0],
    username=aruba_username,
    password=aruba_password,
    secret=aruba_password,
)
rw2 = ConnectHandler(
    device_type="aruba_os",
    ip=variable_data["local_ip"].split("/")[0],
    username=aruba_username,
    password=aruba_password,
    secret=aruba_password,
)

# ------------------------------------------------------
# Interface check
# ------------------------------------------------------

print()

show_interface_result_dict = {}

interface_list = ["gig 0/0/2", "gig 0/0/3", "vlan 606", "vlan 611", "vlan 800", "vlan 801", "vlan 1"]

for x in interface_list:
    print("Interface status for : " + str(x) + " on rw1", end=" ..... : ")
    show_interface_result = show_interface(x, rw1)

    if show_interface_result == -1:
        show_interface_result_dict.update({"show interface " + str(x) + " on rw1": "FAILED to pull data"})
        print("FAILED to pull data. Please check if the interface exists")
    else:
        show_interface_result_dict.update({"show interface " + str(x) + " on rw1": show_interface_result})
        if x == "vlan 1":
            if (
                show_interface_result["admin_status"] == "administratively down"
                and show_interface_result["line_status"] == "down"
            ):
                print(
                    "OK. "
                    + x
                    + " interface admin status is: "
                    + str(show_interface_result["admin_status"])
                    + " Line status is: "
                    + str(show_interface_result["line_status"])
                )
            else:
                print(
                    "OK. "
                    + x
                    + " interface admin status is: "
                    + str(show_interface_result["admin_status"])
                    + " Line status is: "
                    + str(show_interface_result["line_status"])
                )
        else:
            if show_interface_result["admin_status"] == "up" and show_interface_result["line_status"] == "up":
                print(
                    "OK. "
                    + x
                    + " interface admin status is: "
                    + str(show_interface_result["admin_status"])
                    + " Line status is: "
                    + str(show_interface_result["line_status"])
                )
            else:
                print(
                    "OK. "
                    + x
                    + " interface admin status is: "
                    + str(show_interface_result["admin_status"])
                    + " Line status is: "
                    + str(show_interface_result["line_status"])
                )

for x in interface_list:
    print("Interface status for : " + str(x) + " on rw2", end=" ..... : ")
    show_interface_result = show_interface(x, rw2)
    if show_interface_result == -1:
        show_interface_result_dict.update({"show interface " + str(x) + " on rw1": "FAILED to pull data"})
        print("FAILED to pull data. Please check if the interface exists")
    else:
        show_interface_result_dict.update({"show interface " + str(x) + " on rw1": show_interface_result})
        if x == "vlan 1":
            if (
                show_interface_result["admin_status"] == "administratively down"
                and show_interface_result["line_status"] == "down"
            ):
                print(
                    "OK. "
                    + x
                    + " interface admin status is: "
                    + str(show_interface_result["admin_status"])
                    + " Line status is: "
                    + str(show_interface_result["line_status"])
                )
            else:
                print(
                    "OK. "
                    + x
                    + " interface admin status is: "
                    + str(show_interface_result["admin_status"])
                    + " Line status is: "
                    + str(show_interface_result["line_status"])
                )
        else:
            if show_interface_result["admin_status"] == "up" and show_interface_result["line_status"] == "up":
                print(
                    "OK. "
                    + x
                    + " interface admin status is: "
                    + str(show_interface_result["admin_status"])
                    + " Line status is: "
                    + str(show_interface_result["line_status"])
                )
            else:
                print(
                    "OK. "
                    + x
                    + " interface admin status is: "
                    + str(show_interface_result["admin_status"])
                    + " Line status is: "
                    + str(show_interface_result["line_status"])
                )

# ------------------------------------------------------
# Ping test
# ------------------------------------------------------

# This is the data structure that we will store the results
ping_result_dict = {}

#  Pinging rw1 <> rw2
print("Pinging rw2 (" + variable_data["local_ip"].split("/")[0] + ")" + " from rw1", end=" ..... : ")
ping = pingtest(variable_data["local_ip"].split("/")[0], rw1)

if ping == -1:
    ping_result_dict.update({"Ping " + variable_data["local_ip"].split("/")[0] + " from rw1": "FAIL"})
    print("FAIL")
else:
    ping_result_dict.update({"Ping " + variable_data["local_ip"].split("/")[0] + " from rw1": ping})
    print("OK")

print("Pinging rw1 (" + variable_data["master_ip"].split("/")[0] + ")" + " from rw2", end=" ..... : ")
ping = pingtest(variable_data["master_ip"].split("/")[0], rw2)

if ping == -1:
    ping_result_dict.update({"Ping " + variable_data["master_ip"].split("/")[0] + " from rw2": "FAIL"})
    print("FAIL")
else:
    ping_result_dict.update({"Ping " + variable_data["master_ip"].split("/")[0] + " from rw2": ping})
    print("OK")

# Pinging the gateway from both controllers
print("Pinging gateway (" + variable_data["gateway"] + ")" + " from rw1", end=" ..... : ")
ping = pingtest(variable_data["gateway"], rw1)

if ping == -1:
    ping_result_dict.update({"Ping " + variable_data["gateway"] + " from rw1": "FAIL"})
    print("FAIL")
else:
    ping_result_dict.update({"Ping " + variable_data["gateway"] + " from rw1": ping})
    print("OK")

print("Pinging gateway (" + variable_data["gateway"] + ")" + " from rw2", end=" ..... : ")
ping = pingtest(variable_data["gateway"], rw2)

if ping == -1:
    ping_result_dict.update({"Ping " + variable_data["gateway"] + " from rw2": "FAIL"})
    print("FAIL")
else:
    ping_result_dict.update({"Ping " + variable_data["gateway"] + " from rw2": ping})
    print("OK")

# Pinging the rest of the IPs from both controllers
ping_list = ["198.18.0.1", "198.18.0.8", "198.18.0.9", "192.168.0.1", "198.168.0.8", "198.168.0.9", "10.25.24.14"]

for x in ping_list:

    print("Pinging (" + x + ")" + " from rw1", end=" ..... : ")
    ping = pingtest(x, rw1)

    if ping == -1:
        ping_result_dict.update({"Ping " + x + " from rw1": "FAIL"})
        print("FAIL")
    else:
        ping_result_dict.update({"Ping " + x + " from rw1": ping})
        print("OK")

    ping = pingtest(x, rw2)
    print("Pinging (" + x + ")" + " from rw2", end=" ..... : ")

    if ping == -1:
        ping_result_dict.update({"Ping " + x + " from rw2": "FAIL"})
        print("FAIL")
    else:
        ping_result_dict.update({"Ping " + x + " from rw2": ping})
        print("OK")

# ------------------------------------------------------
# STP VLAN test
# ------------------------------------------------------

print()

stp_result_dict = {}

stp_vlan_list = [606, 611, 800, 801]

for x in stp_vlan_list:
    print("STP settings for VLAN (" + str(x) + ")" + " for rw1", end=" ..... : ")
    stp_vlan_list_result = stp_vlan_test(x, rw1)

    if stp_vlan_list_result == -1:
        stp_result_dict.update({"STP VLAN " + str(x) + " on rw1": "FAILED to pull data"})
        print("FAILED to pull data")
    elif stp_vlan_list_result["not_configured"] == x:
        stp_result_dict.update({"STP VLAN " + str(x) + " on rw1": "VLAN not configured"})
        print("FAILED, VLAN not configured")
    else:
        stp_result_dict.update({"STP VLAN " + str(x) + " on rw1": stp_vlan_list_result})
        if "rapid" in stp_vlan_list_result["rspt"].lower() and stp_vlan_list_result["local_priority"] == "65535":
            print("OK, RSPT mode enabled and Local priority is 65535 ")
        elif "rapid" in stp_vlan_list_result["rspt"].lower():
            print(
                "FAILED, RSPT mode enabled but Local priority is not 65535 , its : "
                + stp_vlan_list_result["local_priority"]
            )
        elif stp_vlan_list_result["local_priority"] == "65535":
            print("FAILED, Local priority is 65535 but RSPT mode not enabled")
        else:
            print("FAILED, RSPT mode not enabled and Local priority is not 65535")

    print("STP settings for VLAN (" + str(x) + ")" + " for rw2", end=" ..... : ")
    stp_vlan_list_result = stp_vlan_test(x, rw2)

    if stp_vlan_list_result == -1:
        stp_result_dict.update({"STP VLAN " + str(x) + " on rw2": "FAILED to pull data"})
        print("FAILED to pull data")
    elif stp_vlan_list_result["not_configured"]:
        stp_result_dict.update({"STP VLAN " + str(x) + " on rw2": "VLAN not configured"})
        print("FAILED, VLAN not configured")
    else:
        stp_result_dict.update({"STP VLAN " + str(x) + " on rw2": stp_vlan_list_result})
        if "rapid" in stp_vlan_list_result["rspt"].lower() and stp_vlan_list_result["local_priority"] == "65535":
            print("OK, RSPT mode enabled and Local priority is 65535 ")
        elif "rapid" in stp_vlan_list_result["rspt"].lower():
            print(
                "FAILED, RSPT mode enabled but Local priority is not 65535 , its : "
                + stp_vlan_list_result["local_priority"]
            )
        elif stp_vlan_list_result["local_priority"] == "65535":
            print("FAILED, Local priority is 65535 but RSPT mode not enabled")
        else:
            print("FAILED, RSPT mode not enabled and Local priority is not 65535")

# ------------------------------------------------------
# STP interface test
# ------------------------------------------------------

stp_inter_result_dict = {}

print("\nSTP State for interface 'gigabitethernet 0/0/2' on rw1")
stp_inter_test_result = stp_inter_test("gigabitethernet 0/0/2", rw1)

if stp_inter_test_result == -1:
    stp_inter_result_dict.update({"show spanning-tree interface gigabitethernet 0/0/2 on rw1": "FAIL, command failed"})
    print("FAIL, command failed")
else:
    stp_inter_result_dict.update({"show spanning-tree interface gigabitethernet 0/0/2 on rw1": stp_inter_test_result})

    # Cycle the states for every VLAN and check if it's "Forwarding"
    for x in stp_inter_test_result:
        print("\t For VLAN " + x["vlan"] + " State is : " + x["state"], end=" ..... ")
        if x["state"] == "Forwarding":
            print("OK")
        else:
            print("FAILED")

print("STP State for interface 'gigabitethernet 0/0/2' on rw2")
stp_inter_test_result = stp_inter_test("gigabitethernet 0/0/2", rw2)

if stp_inter_test_result == -1:
    stp_inter_result_dict.update({"show spanning-tree interface gigabitethernet 0/0/2 on rw2": "FAIL, command failed"})
    print("FAIL, command failed")
else:
    stp_inter_result_dict.update({"show spanning-tree interface gigabitethernet 0/0/2 on rw2": stp_inter_test_result})

    # Cycle the states for every VLAN and check if it's "Forwarding"
    for x in stp_inter_test_result:
        print("\t For VLAN " + x["vlan"] + " State is : " + x["state"], end=" ..... ")
        if x["state"] == "Forwarding":
            print("OK")
        else:
            print("FAILED")

print("STP State for interface 'gigabitethernet 0/0/3' on rw1")
stp_inter_test_result = stp_inter_test("gigabitethernet 0/0/3", rw1)

if stp_inter_test_result == -1:
    stp_inter_result_dict.update({"show spanning-tree interface gigabitethernet 0/0/3 on rw1": "FAIL, command failed"})
    print("FAIL, command failed")
else:
    stp_inter_result_dict.update({"show spanning-tree interface gigabitethernet 0/0/3 on rw1": stp_inter_test_result})

    # Cycle the states for every VLAN and check if it's "Forwarding"
    for x in stp_inter_test_result:
        print("\t For VLAN " + x["vlan"] + " State is : " + x["state"], end=" ..... ")
        if x["state"] == "Discarding":
            print("OK")
        else:
            print("FAILED")

print("STP State for interface 'gigabitethernet 0/0/3' on rw2")
stp_inter_test_result = stp_inter_test("gigabitethernet 0/0/3", rw2)

if stp_inter_test_result == -1:
    stp_inter_result_dict.update({"show spanning-tree interface gigabitethernet 0/0/3 on rw2": "FAIL, command failed"})
    print("FAIL, command failed")
else:
    stp_inter_result_dict.update({"show spanning-tree interface gigabitethernet 0/0/3 on rw2": stp_inter_test_result})

    # Cycle the states for every VLAN and check if it's "Discarding"
    for x in stp_inter_test_result:
        print("\t For VLAN " + x["vlan"] + " State is : " + x["state"], end=" ..... ")
        if x["state"] == "Discarding":
            print("OK")
        else:
            print("FAILED")

# ------------------------------------------------------
# "show switches" test
# ------------------------------------------------------

show_switches_result_dict = {}

print("\n'show switches' on rw1")
show_switches_result, total_switches = show_switches(rw1)

if show_switches_result == -1:
    show_switches_result_dict.update({"'show switches' on rw1": "FAIL, command failed"})
    print("FAIL, command failed")
else:
    show_switches_result_dict.update({"'show switches' on rw1": show_switches_result})

    for x in show_switches_result:
        print(
            "\t Configuration state for "
            + x["switch_hostname"]
            + " type: "
            + x["type"]
            + ", is : "
            + x["configuration_state"],
            end=" ..... ",
        )
        if x["configuration_state"] == "UPDATE SUCCESSFUL":
            print("OK")
        else:
            print("FAILED, Expecting 'UPDATE SUCCESSFUL'")

print("'show switches' on rw2")
show_switches_result, total_switches = show_switches(rw2)

if show_switches_result == -1:
    show_switches_result_dict.update({"'show switches' on rw2": "FAIL, command failed"})
    print("FAIL, command failed")
else:
    show_switches_result_dict.update({"'show switches' on rw2": show_switches_result})

    for x in show_switches_result:
        print(
            "\t Configuration state for "
            + x["switch_hostname"]
            + " type: "
            + x["type"]
            + ", is : "
            + x["configuration_state"],
            end=" ..... ",
        )
        if x["configuration_state"] == "UPDATE SUCCESSFUL":
            print("OK")
        else:
            print("FAILED, Expecting 'UPDATE SUCCESSFUL'")

# ------------------------------------------------------
# Default GW test
# ------------------------------------------------------

show_ip_route_result_dict = {}

print("\nGW IP validation on rw1 :", end=" ..... : ")
show_ip_route_result = show_ip_route(rw1)

if show_ip_route_result == -1:
    show_ip_route_result_dict.update({"'show ip route' on rw1": "FAIL, Unexpected output from 'show ip route'"})
    print("FAIL, Unexpected output")
else:
    show_ip_route_result_dict.update({"'show ip route' on rw1": show_ip_route_result})
    if show_ip_route_result["gateway"] == variable_data["gateway"]:
        print("OK, " + show_ip_route_result["gateway"])
    else:
        print("FAILED, " + show_ip_route_result["gateway"])

print("GW IP validation on rw2 :", end=" ..... : ")
show_ip_route_result = show_ip_route(rw2)

if show_ip_route_result == -1:
    show_ip_route_result_dict.update({"'show ip route' on rw2": "FAIL, Unexpected output from 'show ip route'"})
    print("FAIL, Unexpected output")
else:
    show_ip_route_result_dict.update({"'show ip route' on rw2": show_ip_route_result})
    if show_ip_route_result["gateway"] == variable_data["gateway"]:
        print("OK, " + show_ip_route_result["gateway"])
    else:
        print("FAILED, " + show_ip_route_result["gateway"])

# ------------------------------------------------------
# CPU test
# ------------------------------------------------------

show_cpu_result_dict = {}

print("\nCPU Utilization on rw1 :", end=" ..... : ")
show_cpu_result_result = show_cpu(rw1)

if show_cpu_result_result == -1:
    show_cpu_result_dict.update({"CPU Utilization on rw1": "FAIL, Unexpected output from 'show cpu'"})
    print("FAIL, Unexpected output")
else:
    show_cpu_result_dict.update({"CPU Utilization on rw1": show_cpu_result_result})
    if (
        float(show_cpu_result_result["user_load"]) < 50
        and float(show_cpu_result_result["system_load"]) < 50
        and float(show_cpu_result_result["iowait_load"]) < 50
    ):
        print(
            "OK, User load : "
            + show_cpu_result_result["user_load"]
            + " , System Load : "
            + show_cpu_result_result["system_load"]
            + " , IOwait load : "
            + show_cpu_result_result["iowait_load"]
        )
    else:
        print(
            "FAILED, "
            + show_cpu_result_result["user_load"]
            + " , System Load : "
            + show_cpu_result_result["system_load"]
            + " , IOwait load : "
            + show_cpu_result_result["iowait_load"]
        )

print("CPU Utilization on rw2 :", end=" ..... : ")
show_cpu_result_result = show_cpu(rw2)

if show_cpu_result_result == -1:
    show_cpu_result_dict.update({"CPU Utilization on rw2": "FAIL, Unexpected output from 'show cpu'"})
    print("FAIL, Unexpected output")
else:
    show_cpu_result_dict.update({"CPU Utilization on rw2": show_cpu_result_result})
    if (
        float(show_cpu_result_result["user_load"]) < 50
        and float(show_cpu_result_result["system_load"]) < 50
        and float(show_cpu_result_result["iowait_load"]) < 50
    ):
        print(
            "OK, User load : "
            + show_cpu_result_result["user_load"]
            + " , System Load : "
            + show_cpu_result_result["system_load"]
            + " , IOwait load : "
            + show_cpu_result_result["iowait_load"]
        )
    else:
        print(
            "FAILED, "
            + show_cpu_result_result["user_load"]
            + " , System Load : "
            + show_cpu_result_result["system_load"]
            + " , IOwait load : "
            + show_cpu_result_result["iowait_load"]
        )

# ------------------------------------------------------
# Datapth utilization test
# ------------------------------------------------------

show_datapath_utilization_result_dict = {}

print("\nDatapath utilization on rw1", end=" ..... : ")
show_datapath_utilization_result = show_datapath_utilization(rw1)

if show_datapath_utilization_result == -1:
    show_datapath_utilization.update(
        {"Datapath utilization on rw1": "FAIL, Unexpected output from 'show datapath  utilization'"}
    )
    print("FAIL, Unexpected output")
else:
    show_datapath_utilization_result_dict.update({"Datapath utilization on rw1": show_datapath_utilization_result})
    data_util_flag = False

    for x in show_datapath_utilization_result:
        if float(x["one_sec_util"]) > 50 or float(x["four_sec_util"]) > 50 or float(x["sixtyfour_sec_util"]) > 50:
            print(
                "FAILED for CPU# : "
                + x["cpu_number"]
                + " , 1s Util: "
                + x["one_sec_util"]
                + " , 4s Util: "
                + x["four_sec_util"]
                + " , 64s Util: "
                + x["sixtyfour_sec_util"]
            )
            data_util_flag = True

    if not data_util_flag:
        print("OK")

print("Datapath utilization on rw2", end=" ..... : ")
show_datapath_utilization_result = show_datapath_utilization(rw2)

if show_datapath_utilization_result == -1:
    show_datapath_utilization.update(
        {"Datapath utilization on rw2": "FAIL, Unexpected output from 'show datapath  utilization'"}
    )
    print("FAIL, Unexpected output")
else:
    show_datapath_utilization_result_dict.update({"Datapath utilization on rw2": show_datapath_utilization_result})
    data_util_flag = False

    for x in show_datapath_utilization_result:
        if float(x["one_sec_util"]) > 50 or float(x["four_sec_util"]) > 50 or float(x["sixtyfour_sec_util"]) > 50:
            print(
                "FAILED for CPU# : "
                + x["cpu_number"]
                + " , 1s Util: "
                + x["one_sec_util"]
                + " , 4s Util: "
                + x["four_sec_util"]
                + " , 64s Util: "
                + x["sixtyfour_sec_util"]
            )
            data_util_flag = True

    if not data_util_flag:
        print("OK")

pprint.pprint(ping_result_dict)
pprint.pprint(stp_result_dict)
pprint.pprint(stp_inter_result_dict)
pprint.pprint(show_switches_result_dict)
pprint.pprint(show_ip_route_result_dict)
pprint.pprint(show_cpu_result_dict)
pprint.pprint(show_interface_result_dict)

rw1.disconnect()
rw2.disconnect()
