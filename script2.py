import ipaddress
import argparse

class main:
    standard_mask_bits = {"A": 8, "B": 16, "C": 24}
    onbits_to_mask = {1: 128, 2: 192, 3: 224, 4: 240, 5: 248, 6: 252, 7: 254, 8: 255}
    # usable_hosts_mask_bits = {0:254, 1:126, 2:62, 3:30, 4:14, 5:6, 6:2, 7:0, 8: 0}

    def __init__(self, ip, cidr, subnets, *args):
        self.ip = ip
        self.subnets = subnets
        self.cidr = cidr
        h = sorted(args)
        if self.subnets != len(h):
            raise Exception("*** KINDLY PROVIDE NUMBER OF HOSTS FOR EVERY SUBNET ***")

        self.required_hosts = h[::-1]
        valid = self.ValidateIp()
        if valid == False:
            raise Exception("***KINDLY ENTER A VALID IP ADDRESS***")
        self.IpClass()



    # def no_of_subnets(self):
    #     ip_class = self.IpClass()
    #     if ip_class == "D" or ip_class == "E":
    #         print("[*][*][*] KINDLY USE ONLY CLASS A, B OR C IPV4 ADDRESSES [*][*][*]")
    #         return
    #     changed_bits = self.cidr - main.standard_mask_bits[ip_class]
    #     total_subnets = abs(2 ** changed_bits)
    #     print(f"Total possible subnets are {total_subnets}")
    #     return total_subnets


    def no_of_hosts(self):
        off_bits = 32 - self.cidr
        total_hosts = abs(2 ** off_bits - 2)
        #print(f"Total possible hosts are {total_hosts}")
        return total_hosts

    def host_block_size(self):
        lastoctate_on_bits = self.cidr % 8
        if lastoctate_on_bits == 0:
            block_size = 256
        else:
            block_size = 256 - main.onbits_to_mask[lastoctate_on_bits]
        #print(f"Block size for the hosts is {block_size}")
        return block_size


    def get_base_ip(self):
        octate_no = int(self.cidr / 8)
        b = self.host_block_size()

        base_list = []
        c = 0
        while c != 256:
            base_list.append(c)
            c += b

        ip = str(self.ip)
        ip = ip.split(".")

        base_ips = []

        for i in base_list:

            dummy_ip = ip.copy()
            dummy_ip[octate_no] = i

            if octate_no == 0:
                dummy_ip[octate_no + 1] = 0
                dummy_ip[octate_no + 2] = 0
                dummy_ip[octate_no + 3] = 0

            elif octate_no == 1:
                dummy_ip[octate_no + 1] = 0
                dummy_ip[octate_no + 2] = 0

            elif octate_no == 2:
                dummy_ip[octate_no + 1] = 0

            base_ips.append(dummy_ip)
        return base_ips


    def add_net(self, ip, v):
        octnt = int(self.cidr / 8)
        oct_val = self.host_block_size()

        if ip[3] == octnt:

            if ip[3] + v > oct_val:
                raise Exception("cant have this much hosts")

            else:
                ip[3] += v

                return ip

        else:
            x = ip[3] + v

            if v > 255 or x > 255:
                if ip[2] < 255:
                    if ip[2] == octnt:
                        if ip[2] + 2 < oct_val:
                            ip[2] += 1
                            v = v - 256
                            return self.add_net(ip, v)

                        else:
                            raise Exception("cant have this much hosts")

                    else:
                        ip[2] += 1
                        v = v - 256
                        return self.add_net(ip, v)

                else:
                    if ip[1] < 255:
                        if ip[2] == 255:
                            ip[2] = 0
                        if ip[1] == octnt:
                            if ip[1] + 2 < oct_val:
                                p[1] += 1
                                v = v - 256
                                return self.add_net(ip, v)

                            else:
                                raise Exception("cant have this much hosts")

                        else:
                            ip[1] += 1
                            v = v - 256
                            return self.add_net(ip, v)

                    else:
                        if ip[1] == 255:
                            ip[1] = 0
                        if ip[2] == 255:
                            ip[2] = 0

                        if ip[0] + 2 < oct_val:
                            ip[0] += 1
                            v = v - 256
                            return self.add_net(ip, v)

                        else:
                            raise Exception("cant have this much hosts")

            else:
                if v == 0:
                    return ip
                ip[3] += (v)
                return ip



    def get_networks(self):
        total_hosts_required = sum(self.required_hosts)
        k = self.no_of_hosts() + 2 - (self.subnets * 2)
        if total_hosts_required > k:
            raise Exception("*** YOU CAN'T HAVE THESE NUMBER OF HOSTS in different networks  WITH THIS BASE NETWORK ***")
        ips = self.get_base_ip()
        octant = int(self.cidr / 8)
        p = self.ip.split(".")
        p = int(p[octant])
        #print(p)

        for i in reversed(ips):
            if p >= i[octant]:
                base_ip = i
                break

        networks = self.get_networks_cidr()
        required_networks = []
        b = base_ip.copy()
        #print(base_ip)
        #print(b)
        d = {}
        for n in networks:

            v = 2 ** (32 - n)

            net = self.add_net(base_ip, v)
            #d.update({str(b): str(net)})
            # print(net)
            #print(b)
            netcopy = net.copy()
            last = netcopy[-1] - 1
            #print(last)
            nets = '.'.join([str(nt) for nt in b])
            nets = nets + f"-{last}" '/' + str(n)
            b = net.copy()
            required_networks.append(nets)


        #print(d)
        return required_networks



    def get_networks_cidr(self):
        r = self.required_hosts
        cidr_list = []
        for h in r:
            c = 30 #dummy value

            for i in range(1, 32):
                # if h == 1 or h == 2:
                #     c = 30
                #     break
                if (2 ** i) - 2 > h and h > (2 ** (i-1)) - 2:
                    c = 32 - i
                    break
            cidr_list.append(c)

        return cidr_list


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


    def ValidateIp(self):
        val = False
        try:
            ipaddress.ip_address(self.ip)
            val = True
            return val
        except ValueError:
            return val

if __name__ == '__main__':
    ls = [20,10,5]
    ip = "192.168.5.2"
    cidr = 25
    subnets = 3
    inst = main(ip, cidr, subnets,20,10, 5)
    result = inst.get_networks()
    print(f"Following are the required networks with IP range : {result}")
