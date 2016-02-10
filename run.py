#!/usr/bin/env python

from __future__ import print_function, unicode_literals

import os
import sys

if len(sys.argv) > 1 and sys.argv[1].startswith('/'):
    os.execvp(sys.argv[1], sys.argv[1:])

import time
import docker
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', '-n',
                    action='store_true',
                    help="perform a trial run with no changes made")
parser.add_argument('--loop-delay',
                    default=0,
                    type=int,
                    help="sleep a certain delay in seconds (0 to disable)")

def is_container_to_delete(client, container):
    info = client.inspect_container(container)
    return (not info['State']['Running'] and
            info['HostConfig']['RestartPolicy']['MaximumRetryCount'] == 0)

def clean_containers(client):
    to_delete = [x for x in client.containers(all=True)
                   if is_container_to_delete(client, x)]
    for container in to_delete:
        try:
            if not args.dry_run:
                client.remove_container(container=container, v=True)
        except docker.errors.APIError as exc:
            print(exc.explanation)
        else:
            print("Deleted:", container['Id'])

args = parser.parse_args()
client = docker.Client(base_url="unix://tmp/docker.sock", version='auto')

if args.loop_delay:
    while True:
        time.sleep(args.loop_delay)
        clean_containers(client)
else:
    clean_containers(client)
