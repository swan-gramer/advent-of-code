from functools import reduce
from math import prod

class RawPacket:
    def __init__(self, data):
        self.data = data

    def get_version_bin(self):
        return self.data[:3]

    def get_version_dec(self):
        return eval('0b' + self.get_version_bin())

    def get_type(self):
        return self.data[3:6]

    def get_header(self):
        return self.data[:6]

    def get_payload(self):
        return self.data[6:]

    def get_size(self):
        return len(self.data)

    def get_header_size(self):
        return 6

    def is_valid(self):
        if len(self.data) > 6:
            for c in self.data:
                if c != '0':
                    return True
        return False

    def __getitem__(self, key):
        if isinstance(key, slice):
           return RawPacket(self.data[key])


    @staticmethod
    def parse(data, number = None):
        raw_packet = RawPacket(data)
        packets = []
        while raw_packet.is_valid():
            type = raw_packet.get_type()
            if type == '100':
                packet = LiteralPacket(raw_packet)
            else:
                packet = OperationPacket(raw_packet)
            packets.append(packet)
            raw_packet = raw_packet[packet.get_size():]
            if number != None and len(packets) == number:
                return packets
        if number != None and number != len(packets):
            raise Exception('Number error {}'.format(data))
        return packets

class Packet:
    def __init__(self, data):
        if isinstance(data, RawPacket):
            self.data = data
        else:
            self.data = RawPacket(data)

    def get_version(self):
        return self.data.get_version_dec()

    def get_type(self):
        return self.data.get_type()

    def get_size(self):
        return self.data.get_size()


class LiteralPacket(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.value = None
        self.payload_size = None
        self.parse()

    def parse(self):
        payload = self.data.get_payload()
        value = ''
        group_size = 5
        payload_size = 0
        for i in range(0, len(payload), group_size):
            group = payload[i:(i + group_size)]
            flag = group[0]
            content = group[1:]
            value += content
            if flag == '0':
                payload_size = i + group_size
                break
        self.value = int(value)
        self.payload_size = payload_size

    def get_value(self):
        return self.value

    def get_size(self):
        return self.data.get_header_size() + self.payload_size


class OperationPacket(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.sub_packets = None
        self.payload_size = None
        self.parse()

    def get_length_type(self):
        payload = self.data.get_payload()
        return payload[0]

    def get_sub_packets(self):
        if self.sub_packets is None:
            self.parse()
        return self.sub_packets

    def parse(self):
        payload = self.data.get_payload()
        if self.get_length_type() == '0':
            length = eval('0b' + payload[1:16])
            self.payload_size = 16 + length
            if len(payload) < self.payload_size:
                raise Exception('Discrepancy {}'.format(payload))
            sub_packets_raw = payload[16:16+length]
            self.sub_packets = RawPacket.parse(sub_packets_raw)
        else:
            number = eval('0b' + payload[1:12])
            sub_packets_raw = payload[12:]
            self.sub_packets = RawPacket.parse(sub_packets_raw, number)
            if number != len(self.sub_packets):
                raise Exception('Number discrepancy {}'.format(payload))
            self.payload_size = 12
            for sub_packet in self.sub_packets:
                self.payload_size += sub_packet.get_size()


    def get_size(self):
        return self.data.get_header_size() + self.payload_size

    def get_value(self):
        op = eval('0b' + self.get_type())
        if op == 0: #sum
            return reduce(lambda x, y: x + y.get_value(), self.sub_packets, 0)
        elif op == 1: #product
            return reduce(lambda x, y: x * y.get_value(), self.sub_packets, 1)
        elif op == 2: #minimum
            return reduce(lambda x, y: min(x, y.get_value()), self.sub_packets, self.sub_packets[0].get_value())
        elif op == 3: #maximum
            return reduce(lambda x, y: max(x, y.get_value()), self.sub_packets, 0)
        elif op == 5: #greater than
            assert len(self.sub_packets) == 2
            v1, v2 = list(map(lambda x: x.get_value(), self.sub_packets))
            return 1 if v1 > v2 else 0
        elif op == 6: #less than
            assert len(self.sub_packets) == 2
            v1, v2 = list(map(lambda x: x.get_value(), self.sub_packets))
            return 0 if v1 > v2 else 1
        elif op == 7: #equal to
            assert len(self.sub_packets) == 2
            v1, v2 = list(map(lambda x: x.get_value(), self.sub_packets))
            return 1 if v1 == v2 else 0
        else:
            raise Exception("Unknow operator {}".format(op))

hex_bin_map = {
    '0':'0000',
    '1':'0001',
    '2':'0010',
    '3':'0011',
    '4':'0100',
    '5':'0101',
    '6':'0110',
    '7':'0111',
    '8':'1000',
    '9':'1001',
    'A':'1010',
    'B':'1011',
    'C':'1100',
    'D':'1101',
    'E':'1110',
    'F':'1111'
}
def parse(line):
    bstr = ''
    for c in line.strip():
        bstr += hex_bin_map[c]
    return RawPacket.parse(bstr)


def cal_total_version(packet):
    total_version = 0
    total_version += packet.get_version()
    if isinstance(packet, OperationPacket):
        sub_packets = packet.get_sub_packets()
        for s in sub_packets:
            total_version += cal_total_version(s)
    return total_version


with open('input_test') as f:
    for line in f:
        root_packet = parse(line)[0]
        version = cal_total_version(root_packet)
        print("Answer one is {}".format(version))
        value = root_packet.get_value()
        print("Answer two is {}".format(value))

