#! /usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, urllib
import socket, gzip
import argparse
try:
	import pygeoip
except ImportError:
	print '[!] Failed to Import pygeoip'
	try:
		choice = raw_input('[*] Wana install pygeoip? [y/n] ')
	except KeyboardInterrupt:
		print '\n[!] User Interrupted Choice'
		sys.exit(1)
	if choice.strip().lower()[0] == 'y':
		print '[*] Attempting to Install pygeoip... ',
		sys.stdout.flush()
		try:
			import pip
			pip.main(['install', '-q', 'pygeoip'])
			import pygeoip
			print '[DONE]'
		except Exception:
			print '[FAIL]'
			sys.exit(1)
	elif choice.strip().lower()[0] == 'n':
		print '[*] User Denied Auto-install'
		sys.exit(1)
	else:
		print '[!] Invalid Decision'
		sys.exit(1)

class Locator(object):
	def __init__(self, url=False, ip=False, datfile=False):
		self.url = url
		self.ip = ip
		self.datfile = datfile
		self.target = ''
	def check_database(self):
		if not self.datfile:
			self.datfile = '/GeoIP-DB/GeoLiteCity.dat'
		else:
			if not os.path.isfile(self.datfile):
				print '[!] Failed to Detect Specified Database'
				sys.exit(1)
			else:
				return
		if not os.path.isfile(self.datfile):
			print '[!] Default Database Detection Failed'
			try:
				choice = raw_input('[*] Attempt to Auto-install Database? [y/N] ')
			except KeyboardInterrupt:
				print '\n[!] User Interrupted Choice'
				sys.exit(1)
			if choice.strip().lower()[0] == 'y':
				print '[*] Attempting to Auto-install Database, wait... ',
				sys.stdout.flush()
				if not os.path.isdir('/GeoIP-DB'):
					os.makedirs('/GeoIP-DB')
				try:
					urllib.urlretrieve('http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz', '/GeoIP-DB/GeoLiteCity.dat.gz')
				except Exception:
					print '[FAIL]'
					print '[!] Failed to Download Database'
					sys.exit(1)
				try:
					with gzip.open('/GeoIP-DB/GeoLiteCity.dat.gz', 'rb') as compressed_dat:
						with open('/GeoIP-DB/GeoLiteCity.dat', 'wb') as new_dat:
							new_dat.write(compressed_dat.read())
				except IOError:
					print '[FAIL]'
					print '[!] Failed to Decompress Database'
					sys.exit(1)
				os.remove('/GeoIP-DB/GeoLiteCity.dat.gz')
				print '[DONE]\n'
			elif choice.strip().lower()[0] == 'n':
				print '[!] User Denied Auto-Install'
				sys.exit(1)
			else:
				print '[!] Invalid Choice'
				sys.exit(1)
	def query(self):
		if not not self.url:
			print '[*] Translating %s: ' %(self.url),
			sys.stdout.flush()
			try:
				self.target += socket.gethostbyname(self.url)
				print self.target
			except Exception:
				print '\n[!] Failed to Resolve URL'
				return
		else:
			self.target += self.ip
		try:
			print '[*] Querying for Records of %s \n' %(self.target)
			query_obj = pygeoip.GeoIP(self.datfile)
			for key, val in query_obj.record_by_addr(self.target).items():
				print '%s: %s' %(key, val)
			print '\n[*] Complete!'
		except Exception:
			print '\n[!] Failed to Retrieve Records'
			return

if __name__ == '__main__':
	if os.name == 'posix':
		os.system ('clear')
	else:
		os.system('cls')
	print "\n           +----------------------------------+"
	print "             MaxMind Free Database Query Tool"
	print "           +----------------------------------+\n"
	parser = argparse.ArgumentParser(description='MaxMind Database IP/URL Query Tool')
	parser.add_argument('-u','--url', help='Locate via URL ( i.e: roothaxor.in )', action='store', default=False, dest='url')
        parser.add_argument('-t', '--target', help='Locate the specified IP', action='store', default=False, dest='ip')
        parser.add_argument('--dat', help='If Custom database filepath, else nothing', action='store', default=False, dest='datfile')
	args = parser.parse_args()
	if ((not not args.url) and (not not args.ip)) or ((not args.url) and (not args.ip)):
		parser.error('invalid target specification')
	try:
		locate = Locator(url=args.url, ip=args.ip, datfile=args.datfile)
		locate.check_database()
		locate.query()
	except Exception:
		print '\n[!] Sorry Mate, An Unknown Error Occured'