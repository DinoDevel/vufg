# VirtualBox USB filters generator

Generate VirtualBox USB filters to allow hotplug of arbitrary USB devices

## Description

vufg intended to solve one specific problem: when you need to automatically attach **any** usb device to the guest. With some early versions of VirtualBox you've been able to create one "catch-all" filter by leaving all its fields blank. With more recent versions this approach doesn't work anymore. You need to fill at least one field or such filter will not work. And to allow attaching any device you need to create a set of filters matching any possible device. vufg does just this - generates number of filter rules with different values in VID fields. It can generate set of valig VIDs, e.g. ones registered with USB Implementers Forum (https://usb.org/) to allow attach any consumer usb device to the guest. Or it can generate set of filters with every possible VID value within range, this will allow to attach some custom, DIY, virtual usb devices to the guest.

## Installation

vufg doesn't require any special installation. Download to the location of your choice. Make it executable: 
`chmod +x vufg.py`  Run: `python3 vufg.py` or just `./vufg.py`

## Usage
```
usage: vufg [-h] [-v] [-a] [-f value] [-t value] filename

VirtualBox USB filters generator

positional arguments:
  filename              VirtualBox configuration filename

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -a, --all             generate filters for every VID within range, including
                        invalid or obsolete. If omitted (by default) generate
                        filters including only valid VIDs within range.
                        Warning! Any existing filters will be overwritten.
  -f value, --from value
                        generate filters within range of VIDs beginning from
                        'value' (0x0001- 0xffff hex or dec, default 0x0001)
  -t value, --to value  generate filters within range of VIDs ending at
                        'value' (0x0001-0xffff hex or dec, default 0xffff)
```

