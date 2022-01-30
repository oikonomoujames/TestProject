


def interface_check(interface_list, controller_list):
    show_interface_result_dict = {}

    # list comprehensions can be used to create all the commands
    for controller, interface in [(x, y) for x in controller_list for y in interface_list]:
        # print("Interface status for : {} on {}".format(interface, controller), end=" ..... : ")
        # print("show interface {}".format(interface))  # < --- unitest
        show_interface_result_dict.update({ "{}_{}".format(controller,interface):"show interface {}".format(interface)})

    return show_interface_result_dict


if __name__ == "__main__":
    interface_list = ["gig 0/0/2", "gig 0/0/3", "vlan 606", "vlan 611", "vlan 800", "vlan 801", "vlan 1"]
    controller_list = ["rw1", "rw2"]

    a = interface_check(interface_list, controller_list)

    print(a)

