import ipaddress
import argparse


class main:

    standard_mask_bits = {"A": 8, "B": 16, "C": 24}
    onbits_to_mask = {1:128, 2:192, 3:224, 4:240, 5:248, 6:252, 7:254, 8:255}


    def __init__(self, ip, *args, **kargs):
        self.ip = ip
        valid = self.ValidateIp()
        if valid == False:
            raise Exception("KINDLY ENTER A VALID IP ADDRESS")
        print(args)
        if len(args) > 0:
            #self.subnets = args[0]
            self.mask_bit = args[0]

        # if len(kargs.items()) > 0:
        #     self.subnets = kargs["subnet"]


    def no_of_subnets(self):
        ip_class = self.IpClass()
        if ip_class == "D" or ip_class == "E":
            print("[*][*][*] KINDLY USE ONLY CLASS A, B OR C IPV4 ADDRESSES [*][*][*]")
            return
        changed_bits = self.mask_bit - main.standard_mask_bits[ip_class]
        total_subnets = abs(2 ** changed_bits)
        print(f"Total subnets are {total_subnets}")
        return total_subnets


    def no_of_hosts(self):
        off_bits = 32 - self.mask_bit
        total_hosts = abs(2 ** off_bits - 2)
        print(f"Total possible hosts are {total_hosts}")
        return total_hosts

    def host_block_size(self):
        lastoctate_on_bits = self.mask_bit % 8

        if lastoctate_on_bits == 0:
            block_size = 256
        else:
            block_size = 256 - main.onbits_to_mask[lastoctate_on_bits]
        print(f"Block size for the hosts is {block_size}")
        return block_size



    def IpClass(self):

        cat = "none"
        ip = str(self.ip)
        ip = ip.split(".")
        if ip[0] > "0" and ip[0] <= "126":
            cat = "A"

        elif ip[0] >= "128" and ip[0] <= "191":
            cat = "B"

        elif ip[0] >= "192" and ip[0] <= "223":
            cat = "C"

        elif ip[0] >= "224" and ip[0] <= "239":
            cat = "D"

        elif ip[0] >= "240" and ip[0] <= "255":
            cat = "E"

        else:
            raise Exception("[*][*][*] kindly enter valid ip address [*][*][*]")

        return cat

    def get_address_class(self):
        c = self.IpClass()
        print(f"YOUR IP ADDRESS BELONGS TO {c} CLASS")

    def ValidateIp(self):
        val = False
        try:
            ipaddress.ip_address(self.ip)
            val = True
            return val
        except ValueError:
            return val


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="THIS SCRIPT OUTPUTS TOTAL SUBNETS, HOSTS AND HOST BLOCK SIZE ")
    parser.add_argument('-ip', type=str, required=True, metavar='string_value', help="ENTER IP address")
    parser.add_argument('-c', type=int, required=True, metavar='integer_value', help="Enter CIDR notation for subnet mask")

    args = parser.parse_args()

    ip = args.ip
    cidr = args.c

    inst = main(ip, cidr)
    networks = inst.no_of_subnets()
    hosts = inst.no_of_hosts()

    blocks = inst.host_block_size()