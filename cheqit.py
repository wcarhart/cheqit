import argparse
import sys

def cheqit(urls):
	return

def build_parser():
	"""Parse command line args"""
	parser = argparse.ArgumentParser(description=__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('urls', metavar='U', type=str, nargs='+', help='the URL(s) for which to check connectivity', required=True)

def main():
	parser = build_parser()
	args = parser.parse_args()

	if not args.urls:
		raise ValueError('No valid URL(s) detected')
		sys.exit(1)

	cheqit(args.urls)

if __name__ == '__main__':
	main()