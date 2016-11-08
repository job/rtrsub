rtrsub - RTR Substitution
=========================

*WARNING: NOT SUITABLE FOR PRODUCTION USE - PROOF OF CONCEPT*

A substitute for the RTR protocol: generate configuration blobs for your
routers instead of using the RTR protocol to interact with RPKI.

Templates are in jinja2 format. Thanks to the template approach, you can adopt
this tool to any platform or routing policy configuration style.

Review the [bird.j2](../master/template-examples/bird.j2) for an example.

The dictionary available to the template is called `data`. Layout of the
dictionary is as following:

```
{
    '151.232.23.0/24': {
        'origins': [59587]
    },
    '31.5.128.0/17': {
        'origins': [6830]
    },
    '84.218.240.0/20': {
        'origins': [2119]
    }
    ... etc etc ...
}
```

```
hanna:rtrsub job$ rtrsub -h
usage: rtrsub [-h] [-c CACHE] --afi AFI [-t TEMPLATE] [-o OUTPUT] [-v]

optional arguments:
  -h, --help   show this help message and exit
  -c CACHE     Location of the RPKI Cache in JSON format
               (default: http://localcert.ripe.net:8088/export.json)
  --afi AFI    [ ipv4 | ipv6 | mixed ]
  -t TEMPLATE  Template file (default: STDIN)
  -o OUTPUT    Output file (default: STDOUT)
  -v           Display rtrsub version
hanna:rtrsub job$
```

```
Vurt:rtrsub job$ python rtrsub/cli.py --afi ipv4 -t template-examples/bird.j2 -o example-output.conf
Vurt:rtrsub job$
```

or

```
Vurt:rtrsub job$ python rtrsub/cli.py --afi ipv4 < template-examples/bird.j2 > example-output.conf
Vurt:rtrsub job$
```

Copyright (c) 2016 Job Snijders <job@instituut.net>
