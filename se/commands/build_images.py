"""
This module implements the `se build-images` command.
"""

import argparse
import fnmatch
from pathlib import Path
import os

from rich.console import Console

import se
from se.se_epub import SeEpub


def build_images() -> int:
	"""
	Entry point for `libro build-images`
	"""

	parser = argparse.ArgumentParser(description="Build ebook covers and titlepages for a Standard Ebook source directory, and place the output in DIRECTORY/src/epub/images/.")
	parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
	parser.add_argument("directories", metavar="DIRECTORY", nargs="+", help="a Standard Ebooks source directory")
	args = parser.parse_args()

	console = Console(highlight=False, theme=se.RICH_THEME, force_terminal=se.is_called_from_parallel()) # Syntax highlighting will do weird things when printing paths; force_terminal prints colors when called from GNU Parallel

	for directory in args.directories:
		directory = Path(directory).resolve()

		if args.verbose:
			console.print(f"Processing [path][link=file://{directory}]{directory}[/][/] ...")

		try:
			se_epub = SeEpub(directory)

			if args.verbose:
				console.print("\tCleaning metadata ...", end="")

			# Remove useless metadata from cover source files
			for root, _, filenames in os.walk(directory):
				for filename in fnmatch.filter(filenames, "cover.*"):
					se.images.remove_image_metadata(Path(root) / filename)

			if args.verbose:
				console.print(" OK")
				console.print(f"\tBuilding [path][link=file://{directory / 'src/epub/images/cover.svg'}]cover.svg[/][/] ...", end="")

			se_epub.generate_cover_svg()

			if args.verbose:
				console.print(" OK")
				console.print(f"\tBuilding [path][link=file://{directory / 'src/epub/images/titlepage.svg'}]titlepage.svg[/][/] ...", end="")

			se_epub.generate_titlepage_svg()

			if args.verbose:
				console.print(" OK")
		except se.SeException as ex:
			se.print_error(ex)
			return ex.code

	return 0
