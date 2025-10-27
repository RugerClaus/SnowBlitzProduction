class NetworkInterface:
    def __init__(self, name, ip_address, mac_address):
        self.name = name
        self.ip_address = ip_address
        self.mac_address = mac_address

    def get_info(self):
        return {
            "name": self.name,
            "ip_address": self.ip_address,
            "mac_address": self.mac_address
        }
    