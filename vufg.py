#!/usr/bin/python3

import argparse
import xml.etree.ElementTree as ET

# USB Vendor list is available at https://www.usb.org/developers

with open('vendor_ids.txt', 'r') as file:
    valid_vids = [int(line.strip(), 16) for line in file]

range_min_limit = 1
range_max_limit = 0xffff


def auto_int(x):
    return int(x, 0)


def is_range_arguments_correct(range_from: int, range_to: int):
    if range_from < range_min_limit:
        print(f"vufg: error: range must start at a value greater than 0x{format(range_min_limit, '04x')}.")
        return False
    elif range_from > range_to:
        print(f"vufg: error: range end must be greater than range start.")
        return False
    elif range_to > range_max_limit:
        print(f"vufg: error: range must end at a value lesser than 0x{format(range_max_limit, '04x')}.")
        return False
    return True

def add_filter(filter_id):
    hexcount = format(filter_id, '04x')
    device_filter = ET.SubElement(elem_device_filters, "DeviceFilter", name="Filter 0x" + hexcount, active="true",
                                  vendorId=hexcount, remote="0")
    device_filter.tail = "\n"
    return ()

def gen_filters_range_good(range_from, range_to, elem_device_filters):
    counter = range_from
    while counter <= range_to:
        if counter in valid_vids:
            add_filter(counter)
        counter += 1
    return ()


def gen_filters_range_all(range_from, range_to, elem_device_filters):
    counter = range_from
    while counter <= range_to:
        add_filter(counter)
        counter += 1
    return ()


parser = argparse.ArgumentParser(
    prog='vufg',
    description='VirtualBox USB filters generator',
    epilog='\n', add_help=True)
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.2')
parser.add_argument('-a', '--all', dest='r_all', action='store_true', help='''
generate filters for every VID within range, including invalid or obsolete. If omitted (by default) generate
 filters including only valid VIDs within range. Warning! Any existing filters will be overwritten.''')
parser.add_argument('-f', '--from', dest='r_from', type=auto_int, metavar='value', default=range_min_limit, help=f'''
generate filters within range of VIDs beginning from 'value' (0x{format(range_min_limit, '04x')}-
0x{format(range_max_limit, '04x')} hex or dec, default 0x{format(range_min_limit, '04x')})''')
parser.add_argument('-t', '--to', dest='r_to', type=auto_int, metavar='value', default=range_max_limit, help=f'''
generate filters within range of VIDs ending at 'value' (0x{format(range_min_limit, '04x')}-0x{format(range_max_limit,
 '04x')} hex or dec, default 0x{format(range_max_limit, '04x')})''')
parser.add_argument('filename', type=argparse.FileType('r+'), help='VirtualBox configuration filename')

if __name__ == '__main__':
    args = parser.parse_args()

    tree = ET.parse(args.filename)
    root = tree.getroot()

    parent_map = {c: p for p in root.iter() for c in p}

    for elem in root.iter('{http://www.virtualbox.org/}DeviceFilters'):
        parent_map[elem].remove(elem)

    elem_usb = root.find('.//{http://www.virtualbox.org/}USB')
    elem_device_filters = ET.SubElement(elem_usb, "DeviceFilters")
    elem_device_filters.tail = "\n"

    if is_range_arguments_correct(args.r_from, args.r_to):
        if args.r_all:
            gen_filters_range_all(args.r_from, args.r_to, elem_device_filters)
        else:
            gen_filters_range_good(args.r_from, args.r_to, elem_device_filters)

        ET.register_namespace("", "http://www.virtualbox.org/")
        tree.write(args.filename.name, encoding='utf-8')
        print("Filters added.")

