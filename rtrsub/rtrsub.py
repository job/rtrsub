#!/usr/bin/env python3
# rtrsub - A RTR Substitution
#
# Copyright (C) 2016-2018 Job Snijders <job@instituut.net>
#
# This file is part of rtrsub
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from collections import OrderedDict
from ipaddress import ip_network
from operator import itemgetter

import argparse
import jinja2
import json
import os
import pprint
import radix
import requests
import rtrsub
import sys


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-c', dest='cache',
                        default="https://console.rpki-client.org/vrps.json",
                        type=str,
                        help="""Location of the RPKI Cache in JSON format
(default: https://console.rpki-client.org/vrps.json)""")

    parser.add_argument('--afi', dest='afi', type=str, required=True,
                        help="[ ipv4 | ipv6 | mixed ]")

    parser.add_argument('-t', dest='template', type=str,
                        default="-", help='Template file (default: STDIN)')

    parser.add_argument('-o', dest='output', type=str,
                        default='-',
                        help='Output file (default: STDOUT)')

    parser.add_argument('--asns', dest='asns', type=str,
                        help="""Limit output to the comma separated specified
ASNs and related ROAs""")

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + rtrsub.__version__)

    args = parser.parse_args()

    if args.asns:
        asns = list(map(int, args.asns.split(',')))
    else:
        asns = None

    if args.afi not in ["ipv4", "ipv6", "mixed"]:
        print("ERROR: afi must be 'ipv4', 'ipv6' or 'mixed'")
        sys.exit(2)

    env = jinja2.Environment()

    if args.template == "-":
        template_stdin = sys.stdin.read()
        template = env.from_string(template_stdin)
    else:
        template = env.from_string(
            open(os.path.abspath(args.template), 'r').read())

    if 'http' in args.cache:
        r = requests.get(args.cache, headers={'Accept': 'text/json'})
        validator_export = r.json()
    else:
        validator_export = json.load(open(args.cache, "r"))

    data = dict()
    data['roa_list'] = load_roa_list(args.afi, validator_export, asns)
    data['afi'] = args.afi

    if args.output == "-":
        print(template.render(**data))
    else:
        f = open(args.output, 'w')
        f.write(template.render(**data))
        f.close


def aggregate_roas(rtree):
    """
    remove any supplied prefixes which are superfluous because they are
    already included in another supplied prefix. For example, 203.97.2.0/24
    would be removed if 203.97.0.0/17 was also supplied.
    """
    prefixes = list(rtree.prefixes())
    for prefix in prefixes:
        if not prefix == rtree.search_worst(prefix).prefix:
            rtree.delete(prefix)
    return rtree.prefixes()


def load_roa_list(afi, export, asns):
    """
    :param afi:     which address family to filter for
    :param export:  the JSON blob with all ROAs
    """

    roa_list = []

    """ each roa tuple has these fields:
        asn, prefix, maxLength, ta
    """

    for roa in export['roas']:
        prefix_obj = ip_network(roa['prefix'])
        if afi == "ipv4":
            if prefix_obj.version == 6:
                continue
        elif afi == "ipv6":
            if prefix_obj.version == 4:
                continue

        try:
            asn = roa['asn']
            if not 0 <= asn < 4294967296:
                raise ValueError
        except ValueError:
            print("ERROR: ASN malformed", file=sys.stderr)
            print(pprint.pformat(roa, indent=4), file=sys.stderr)
            continue

        prefix = str(prefix_obj)
        prefixlen = prefix_obj.prefixlen
        maxlength = int(roa['maxLength'])

        roa_list.append((prefix, prefixlen, maxlength, asn))

    roa_list_uniq = []
    for roa in set(roa_list):
        if not asns or int(roa[3]) in asns:
            roa_list_uniq.append({'prefix': roa[0],
                                  'prefixlen': roa[1],
                                  'maxlen': roa[2],
                                  'origin': roa[3]})

    return roa_list_uniq
