"""
Tests for lint command.
"""

from pathlib import Path
import pytest
from helpers import assemble_book, run, output_is_golden



def test_lint(data_dir: Path, draft_dir: Path, work_dir: Path, capfd, update_golden,test_name='clean' ):
	"""Run lint command on several books with different expected lint output:
		clean   - No errors expected
		content - Errors for a default content.opf
	"""
	print(f"{data_dir},{draft_dir},{work_dir}")
	text_dir = data_dir / "lint" / test_name
	print(text_dir)
	book_dir = assemble_book(draft_dir, work_dir, text_dir)

	result = run(f"libro lint --plain {book_dir}")

	# All books with errors should return a non-zero return code
	if test_name != "clean":
		assert result.returncode != 0

	# Output of stderr should always be empty
	out, err = capfd.readouterr()
	assert err == ""

	# Update golden output files if flag is set
	golden_file = data_dir / "lint" / f"{test_name}-out.txt"
	
	assert output_is_golden(out, golden_file, update_golden)
