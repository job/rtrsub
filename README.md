rtrsub - RTR Substitution
=========================

*WARNING: NOT SUITABLE FOR PRODUCTION USE - PROOF OF CONCEPT*

A substitute for the RTR protocol: generate configuration blobs for your
routers instead of using the RTR protocol to interact with RPKI.

Installation
------------

`pip3 install rtrsub`

Use
---

Templates are in jinja2 format. Thanks to the template approach, you can adopt
this tool to any platform or routing policy configuration style.

Review the [bird.j2](../master/template-examples/bird.j2) for an example.

There are a number of variables available to the template, as following:

```
{
    "afi": "ipv4",
    "pfx_dict": {
            "195.221.191.0/20": {
                "prefixlen": 20,
                "origins": [
                    1725,
                    2342
                ],
                "maxlength": 24
            },
            ... etc ...
        },
    "origin_dict": {
        "57348": {
            "185.67.149.0/24": {
                "length": 24,
                "maxlength": 24
            },
            "185.67.148.0/24": {
                "length": 24,
                "maxlength": 24
            }
        },
        ... etc ...
    }
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
Vurt:rtrsub job$ rtrsub --afi ipv4 -t template-examples/bird.j2 -o example-output.conf
Vurt:rtrsub job$
```

or

```
Vurt:rtrsub job$ rtrsub --afi ipv4 < template-examples/bird.j2 > example-output.conf
Vurt:rtrsub job$
```

Copyright (c) 2016-2018 Job Snijders <job@instituut.net>
