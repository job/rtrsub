rtrsub - RTR Substitution
=========================

A substitute for the RTR protocol: generate configuration blobs for your
routers instead of using the RTR protocol to interact with RPKI.

Installation
------------

`pip3 install rtrsub`

Use
---

Templates are in jinja2 format. Thanks to the template approach, you can adopt
this tool to any platform or routing policy configuration style.

Review the [bird.j2](../master/template-examples/bird-minimal.j2) for an example.

There are a number of variables available to the template, please review the [JSON example](https://github.com/job/rtrsub/blob/master/template-examples/example-data-available-to-template.json).

```
hanna:rtrsub job$ rtrsub -h
usage: rtrsub [-h] [-c CACHE] --afi AFI [-t TEMPLATE] [-o OUTPUT] [-v]

optional arguments:
  -h, --help   show this help message and exit
  -c CACHE     Location of the RPKI Cache in JSON format
               (default: https://rpki.gin.ntt.net/api/export.json)
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
