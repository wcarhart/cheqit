import argparse
import socket
import sys
import time
from subprocess import Popen, PIPE
from urllib.parse import urlparse

def cheqit(netlocs, stream, delay):
	"""Handle cheqit process"""
	if stream:
		while True:
			statuses = get_status(netlocs)
			try:
				display_statuses(statuses, show_timestamp=True)
				print("\n^C to exit...")
				time.sleep(delay)

				statuses = get_status(netlocs)
				for _ in range(0, len(netlocs)+2):
					print("\033[A\033[K")
					print("\033[2A")
			except KeyboardInterrupt:
				print('')
				sys.exit(0)
	else:
		statuses = get_status(netlocs)
		display_statuses(statuses)

def get_status(netlocs):
	"""Check status of each hostname or IP address"""
	if len(netlocs) == 0:
		raise ValueError('No valid URL(s) or IP address(es) detected')

	statuses = {}
	for netloc in netlocs:
		cmd = 'ping -c 1 -t 2 {} 2>&1 >/dev/null'.format(netloc)
		proc = Popen(cmd, stdout=PIPE, shell=True)
		out, err = proc.communicate()
		response = proc.returncode
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
	parser.add_argument('urls', metavar='url_or_ip', type=str, nargs='+', help="the URL(s) or IP address(es) for which to check status")
	parser.add_argument('-s', '--stream', action='store_true', default=False, required=False, help="if included, status will be streamed to stdout")
	parser.add_argument('-d', '--delay', type=int, default=10, required=False, help="if streaming, the delay between updates, in seconds (minimum is 10)")
	return parser

def main():
	parser = build_parser()
	args = parser.parse_args()

	if not args.urls:
		raise ValueError('No valid URL(s) or IP address(es) detected')

	if args.delay < 10:
		args.delay = 10

	netlocs = cleanse(args.urls)
	cheqit(netlocs, args.stream, args.delay)

if __name__ == '__main__':
	main()