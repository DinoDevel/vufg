# VirtualBox USB filters generator

Generate VirtualBox USB filters to allow hotplug of arbitrary USB devices

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

