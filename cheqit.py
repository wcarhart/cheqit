import argparse
import sys
import socket
from urllib.parse import urlparse
import os
import time

def cheqit(netlocs, stream, delay):
	"""Handle cheqit"""
	if stream:
		while True:
			statuses = get_status(netlocs)
			display_statuses(statuses, show_timestamp=True)
			time.sleep(delay)
	else:
		statuses = get_status(netlocs)
		display_statuses(statuses)
	return

def get_status(netlocs):
	"""Check status of each hostname or IP address"""
	if len(netlocs) == 0:
		raise ValueError('No valid URL(s) or IP address(es) detected')

	statuses = {}
	for netloc in netlocs:
		response = os.system('ping -c 1 -t 2 {} > /dev/null'.format(netloc))
		status = True if response == 0 else False
		statuses[netloc] = status

	return statuses

def display_statuses(statuses, show_timestamp=False):
	for netloc, status in statuses.items():
		status_text = green("UP") if status else red("DOWN")
		timestamp = ' ({})'.format(time.strftime("%Y-%m-%d %H:%M:%S")) if show_timestamp else ''
		print(" {}: {}{}".format(netloc, status_text, timestamp))

def red(text):
	return f"\033[91m{text}\033[0m"

def green(text):
	return f"\033[92m{text}\033[0m"

def cleanse(resources):
	"""Convert URLs to hostnames and valid IPs"""
	netlocs = []

	for resource in resources:
		url = urlparse(resource)
		if url.netloc == '':
			if url.path == '':
				try:
					socket.inet_aton(resource)
					netlocs.append(resource)
				except socket.error:
					raise ValueError('Invalid IP or URL: {}'.format(resource))
			else:
				netlocs.append(url.path)
		else:
			# strip off scheme (i.e., 'http') and path (i.e. '/stuff/after/hostname/')
			netlocs.append(url.netloc)

	return netlocs

def build_parser():
	"""Parse command line args"""
	parser = argparse.ArgumentParser(description=__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('urls', metavar='U', type=str, nargs='+', help='the URL(s) for which to check connectivity')
	parser.add_argument('-s', '--stream', action='store_true', default=False, required=False, help="if included, URL status will be updated and displayed every 10 seconds")
	return parser

def main():
	parser = build_parser()
	args = parser.parse_args()

	if not args.urls:
		raise ValueError('No valid URL(s) or IP address(es) detected')

	netlocs = cleanse(args.urls)
	cheqit(netlocs, args.stream, 10)

if __name__ == '__main__':
	main()