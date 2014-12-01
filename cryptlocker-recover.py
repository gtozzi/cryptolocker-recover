#!/usr/bin/env python3

'''
Cryptlocker-Recover.py

Recovers a folder messed up by cryptlocker by selectively restoring a backup

Scans recursively the <destination> folder for any .encrypted file, deletes the
encrypted file and restores the one from the provided <backup> folder.

*** ALWAYS HAVE A BACKUP BEFORE RUNNING THIS SCRIPT ***

@author: Gabriele Tozzi <gabriele@tozzi.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
NAME = 'cryptlocker-recover'
VERSION = '0.9'

import os, sys
import shutil
import argparse
import logging


class Main:
	''' The main class '''

	def __init__(self, destination, backup):
		self.log = logging.getLogger()
		self.destination = destination
		self.backup = backup

	def run(self, real=False):
		self.log.info('%s Recovering folder %s using backup from %s', '' if real else '*SIMULATING*', self.destination, self.backup)
		found = 0
		recovered = 0
		errors = 0
		for root, subdirs, files in os.walk(self.destination):
			for f in files:
				path = os.path.join(root, f)
				if path[-10:] == '.encrypted':
					found += 1
					bpath = os.path.join(self.backup, os.path.relpath(root, self.destination), f)[:-10]
					mex = "Found encrypted file: %s"
					args = [path]

					if not os.path.exists(bpath):
						mex += " but no siutable backup found"
						self.log.error(mex, *args)
						errors += 1
						continue

					mex += ", recovered using backup file: %s"
					args.append(bpath)

					dst = path[:-10]
					if real:
						shutil.copyfile(bpath, path[:-10])
						os.remove(path)
					else:
						self.log.warn('Simulating copy from %s to %s', bpath, dst)
						self.log.warn('Simulating deletion of %s', path)

					recovered += 1
					self.log.info(mex, *args)

		self.log.info('Terminated. %d corrupted files found, %d recovered, %d errors.', found, recovered, errors)


if __name__ == '__main__':
	logging.basicConfig(format='%(message)s', level=logging.DEBUG)
	
	parser = argparse.ArgumentParser()
	parser.add_argument("destination", help="the destination folder to be recovered")
	parser.add_argument("backup", help="the source backup folder")
	parser.add_argument("--real-run", action="store_true", help="run for real (just simulate by default)")
	args = parser.parse_args()

	Main(args.destination, args.backup).run(args.real_run)

	sys.exit(0)
