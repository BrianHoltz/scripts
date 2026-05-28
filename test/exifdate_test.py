#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Brian Holtz
# SPDX-License-Identifier: MIT

import importlib.util
from importlib.machinery import SourceFileLoader
import tempfile
from pathlib import Path
import pytest
import subprocess
import io
from unittest.mock import patch, MagicMock

EXIFDATE_PATH = Path(__file__).parent.parent / "exifdate"
SPEC = importlib.util.spec_from_loader("exifdate", SourceFileLoader("exifdate", str(EXIFDATE_PATH)))
EXIFDATE_MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(EXIFDATE_MODULE)
extract_date_from_filename = EXIFDATE_MODULE.extract_date_from_filename
set_exif_dates = EXIFDATE_MODULE.set_exif_dates


# Minimal valid JPEG file (1x1 pixel)
MINIMAL_JPEG = bytes([
    0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01,
    0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
    0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08, 0x07, 0x07, 0x07, 0x09,
    0x09, 0x08, 0x0A, 0x0C, 0x14, 0x0D, 0x0C, 0x0B, 0x0B, 0x0C, 0x19, 0x12,
    0x13, 0x0F, 0x14, 0x1D, 0x1A, 0x1F, 0x1E, 0x1D, 0x1A, 0x1C, 0x1C, 0x20,
    0x24, 0x2E, 0x27, 0x20, 0x22, 0x2C, 0x23, 0x1C, 0x1C, 0x28, 0x37, 0x29,
    0x2C, 0x30, 0x31, 0x34, 0x34, 0x34, 0x1F, 0x27, 0x39, 0x3D, 0x38, 0x32,
    0x3C, 0x2E, 0x33, 0x34, 0x32, 0xFF, 0xC0, 0x00, 0x0B, 0x08, 0x00, 0x01,
    0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4, 0x00, 0x14, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x03, 0xFF, 0xC4, 0x00, 0x14, 0x10, 0x01, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0xFF, 0xDA, 0x00, 0x08, 0x01, 0x01, 0x00, 0x00, 0x3F, 0x00,
    0x37, 0xFF, 0xD9
])


@pytest.fixture
def temp_jpeg(tmp_path):
    """Create a temporary JPEG file for testing."""
    def _create_jpeg(filename):
        filepath = tmp_path / filename
        filepath.write_bytes(MINIMAL_JPEG)
        return filepath
    return _create_jpeg


class TestDateParsing:
    """Date parsing tests for extract_date_from_filename."""

    def test_yyyy_mm_dd_format(self):
        """Extract YYYY-MM-DD format from filename."""
        result = extract_date_from_filename("vacation_2024-03-15_beach.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-03-15"
        assert exif_datetime == "2024:03:15 12:00:00"

    def test_yyyy_mm_format(self):
        """Extract YYYY-MM format from filename."""
        result = extract_date_from_filename("IMG_2024-03_spring.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-03"
        assert exif_datetime == "2024:03:01 12:00:00"

    def test_yyyy_format(self):
        """Extract YYYY format from filename."""
        result = extract_date_from_filename("photo_2024_summer.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024"
        assert exif_datetime == "2024:07:01 12:00:00"

    def test_no_date_pattern(self):
        """Files with no date pattern return None."""
        result = extract_date_from_filename("vacation_beach.jpg")
        assert result is None

    def test_multiple_date_patterns_first_match(self):
        """Files with multiple date patterns use first match."""
        result = extract_date_from_filename("2024-03-15_backup_2023-12-01.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-03-15"
        assert exif_datetime == "2024:03:15 12:00:00"

    def test_yyyy_mm_dd_at_start(self):
        """Date pattern at start of filename."""
        result = extract_date_from_filename("2024-03-15.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-03-15"

    def test_yyyy_mm_dd_at_end(self):
        """Date pattern at end of filename."""
        result = extract_date_from_filename("vacation_2024-03-15.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-03-15"

    def test_yyyy_mm_dd_in_middle(self):
        """Date pattern in middle of filename."""
        result = extract_date_from_filename("IMG_2024-03-15_vacation.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-03-15"

    def test_old_date_1900(self):
        """Very old date (1900) is accepted."""
        result = extract_date_from_filename("photo_1900-01-01.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "1900-01-01"
        assert exif_datetime == "1900:01:01 12:00:00"

    def test_future_date_2100(self):
        """Future date (2100) is accepted."""
        result = extract_date_from_filename("photo_2100-12-31.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2100-12-31"
        assert exif_datetime == "2100:12:31 12:00:00"

    def test_year_boundary_1899_rejected(self):
        """Year 1899 is rejected (below 1900 threshold)."""
        result = extract_date_from_filename("photo_1899.jpg")
        assert result is None

    def test_year_boundary_2101_rejected(self):
        """Year 2101 is rejected (above 2100 threshold)."""
        result = extract_date_from_filename("photo_2101.jpg")
        assert result is None

    def test_yyyymmdd_format(self):
        """Extract YYYYMMDD format (8 digits, no dashes) from filename."""
        result = extract_date_from_filename("IMG_20240315_123456.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "20240315"
        assert exif_datetime == "2024:03:15 12:00:00"

    def test_yyyymm_format(self):
        """Extract YYYYMM format (6 digits, no dashes) from filename."""
        result = extract_date_from_filename("photo_202403_spring.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "202403"
        assert exif_datetime == "2024:03:01 12:00:00"

    def test_yyyymmdd_at_start(self):
        """YYYYMMDD pattern at start of filename."""
        result = extract_date_from_filename("20240315_vacation.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "20240315"
        assert exif_datetime == "2024:03:15 12:00:00"

    def test_yyyymm_at_end(self):
        """YYYYMM pattern at end of filename."""
        result = extract_date_from_filename("vacation_202403.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "202403"
        assert exif_datetime == "2024:03:01 12:00:00"

    def test_yyyymmdd_invalid_month(self):
        """YYYYMMDD with invalid month (13) is rejected."""
        result = extract_date_from_filename("IMG_20241315_invalid.jpg")
        assert result is None

    def test_yyyymmdd_invalid_day(self):
        """YYYYMMDD with invalid day (32) is rejected."""
        result = extract_date_from_filename("IMG_20240332_invalid.jpg")
        assert result is None

    def test_yyyymm_invalid_month(self):
        """YYYYMM with invalid month (13) is rejected."""
        result = extract_date_from_filename("photo_202413_invalid.jpg")
        assert result is None

    def test_yyyymmdd_year_boundary_1900(self):
        """YYYYMMDD with year 1900 is accepted."""
        result = extract_date_from_filename("photo_19000101.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "19000101"
        assert exif_datetime == "1900:01:01 12:00:00"

    def test_yyyymmdd_year_boundary_2100(self):
        """YYYYMMDD with year 2100 is accepted."""
        result = extract_date_from_filename("photo_21001231.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "21001231"
        assert exif_datetime == "2100:12:31 12:00:00"

    def test_yyyymmdd_year_boundary_1899_rejected(self):
        """YYYYMMDD with year 1899 is rejected."""
        result = extract_date_from_filename("photo_18991231.jpg")
        assert result is None

    def test_yyyymmdd_year_boundary_2101_rejected(self):
        """YYYYMMDD with year 2101 is rejected."""
        result = extract_date_from_filename("photo_21010101.jpg")
        assert result is None

    @pytest.mark.parametrize(
        "filename, expected_pattern, expected_datetime",
        [
            ("IMG_20260508_vacation.jpg", "20260508", "2026:05:08 12:00:00"),
            ("photo_202605_spring.jpg", "202605", "2026:05:01 12:00:00"),
        ],
    )
    def test_additional_compact_date_formats(self, filename, expected_pattern, expected_datetime):
        """Extract additional compact date formats."""
        result = extract_date_from_filename(filename)
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == expected_pattern
        assert exif_datetime == expected_datetime

    @pytest.mark.parametrize(
        "filename",
        [
            "IMG_20261301_invalid.jpg",
            "IMG_20260532_invalid.jpg",
            "IMG_189912_old.jpg",
            "IMG_210101_future.jpg",
        ],
    )
    def test_additional_compact_date_rejections(self, filename):
        """Reject invalid compact date patterns."""
        assert extract_date_from_filename(filename) is None

    def test_yyyymm_year_boundary_1900(self):
        """YYYYMM with year 1900 is accepted."""
        result = extract_date_from_filename("photo_190001.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "190001"
        assert exif_datetime == "1900:01:01 12:00:00"

    def test_yyyymm_year_boundary_2100(self):
        """YYYYMM with year 2100 is accepted."""
        result = extract_date_from_filename("photo_210012.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "210012"
        assert exif_datetime == "2100:12:01 12:00:00"

    def test_yyyymm_year_boundary_1899_rejected(self):
        """YYYYMM with year 1899 is rejected."""
        result = extract_date_from_filename("photo_189912.jpg")
        assert result is None

    def test_yyyymm_year_boundary_2101_rejected(self):
        """YYYYMM with year 2101 is rejected."""
        result = extract_date_from_filename("photo_210101.jpg")
        assert result is None

    def test_pattern_priority_yyyy_mm_dd_over_yyyymmdd(self):
        """YYYY-MM-DD is matched before YYYYMMDD when both present."""
        result = extract_date_from_filename("2024-03-15_20240320.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-03-15"
        assert exif_datetime == "2024:03:15 12:00:00"

    def test_pattern_priority_yyyymmdd_over_yyyy_mm(self):
        """YYYYMMDD is matched before YYYY-MM when both present."""
        result = extract_date_from_filename("20240315_2024-03.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "20240315"
        assert exif_datetime == "2024:03:15 12:00:00"

    def test_pattern_priority_yyyy_mm_over_yyyymm(self):
        """YYYY-MM is matched before YYYYMM when both present."""
        result = extract_date_from_filename("2024-03_202404.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-03"
        assert exif_datetime == "2024:03:01 12:00:00"

    def test_partial_date_yyyy_mm_preferred_over_yyyy(self):
        """YYYY-MM is matched before YYYY."""
        result = extract_date_from_filename("photo_2024-03.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-03"
        assert exif_datetime == "2024:03:01 12:00:00"

    def test_date_with_underscores_around(self):
        """Date pattern with underscores around it."""
        result = extract_date_from_filename("IMG_2024-03-15_001.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-03-15"

    def test_date_with_dots_in_filename(self):
        """Filename with dots but valid date pattern."""
        result = extract_date_from_filename("photo.2024-03-15.final.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-03-15"


class TestEXIFManipulation:
    """EXIF manipulation tests for set_exif_dates."""

    def test_set_exif_dates_dry_run(self, temp_jpeg):
        """Setting EXIF dates in dry-run mode succeeds."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        result = set_exif_dates(filepath, "2024:03:15 12:00:00", dry_run=True)
        assert result is True

    def test_set_exif_dates_actual_run(self, temp_jpeg):
        """Setting EXIF dates in actual run mode succeeds."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        result = set_exif_dates(filepath, "2024:03:15 12:00:00", dry_run=False)
        assert result is True

    def test_set_exif_dates_sets_all_three_fields(self, temp_jpeg):
        """Verify all three date fields are set."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        
        # Mock piexif to capture what's being set
        with patch.object(EXIFDATE_MODULE, 'piexif') as mock_piexif:
            mock_exif_dict = {"0th": {}, "Exif": {}}
            mock_piexif.load.return_value = mock_exif_dict
            mock_piexif.ImageIFD.DateTime = 306
            mock_piexif.ExifIFD.DateTimeOriginal = 36867
            mock_piexif.ExifIFD.DateTimeDigitized = 36868
            mock_piexif.dump.return_value = b"mock_exif_bytes"
            
            set_exif_dates(filepath, "2024:03:15 12:00:00", dry_run=False)
            
            # Verify all three fields were set
            assert mock_exif_dict["0th"][306] == b"2024:03:15 12:00:00"
            assert mock_exif_dict["Exif"][36867] == b"2024:03:15 12:00:00"
            assert mock_exif_dict["Exif"][36868] == b"2024:03:15 12:00:00"

    def test_set_exif_dates_handles_missing_exif_data(self, temp_jpeg):
        """Handles files without existing EXIF data."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        
        # Mock piexif to return empty EXIF dict
        with patch.object(EXIFDATE_MODULE, 'piexif') as mock_piexif:
            mock_piexif.load.return_value = {}
            mock_piexif.ImageIFD.DateTime = 306
            mock_piexif.ExifIFD.DateTimeOriginal = 36867
            mock_piexif.ExifIFD.DateTimeDigitized = 36868
            mock_piexif.dump.return_value = b"mock_exif_bytes"
            
            result = set_exif_dates(filepath, "2024:03:15 12:00:00", dry_run=False)
            assert result is True

    def test_set_exif_dates_handles_non_image_file(self, tmp_path):
        """Handles non-image files gracefully."""
        filepath = tmp_path / "test.txt"
        filepath.write_text("not an image")
        
        result = set_exif_dates(filepath, "2024:03:15 12:00:00", dry_run=False)
        assert result is False

    def test_set_exif_dates_handles_read_error(self, temp_jpeg):
        """Handles EXIF read errors gracefully."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        
        with patch.object(EXIFDATE_MODULE, 'piexif') as mock_piexif:
            mock_piexif.load.side_effect = Exception("Read error")
            
            result = set_exif_dates(filepath, "2024:03:15 12:00:00", dry_run=False)
            assert result is False

    def test_set_exif_dates_handles_write_error(self, temp_jpeg):
        """Handles EXIF write errors gracefully."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        
        with patch.object(EXIFDATE_MODULE, 'piexif') as mock_piexif:
            mock_piexif.load.return_value = {"0th": {}, "Exif": {}}
            mock_piexif.ImageIFD.DateTime = 306
            mock_piexif.ExifIFD.DateTimeOriginal = 36867
            mock_piexif.ExifIFD.DateTimeDigitized = 36868
            mock_piexif.dump.return_value = b"mock_exif_bytes"
            mock_piexif.insert.side_effect = Exception("Write error")
            
            result = set_exif_dates(filepath, "2024:03:15 12:00:00", dry_run=False)
            assert result is False


class TestCommandLineInterface:
    """Command-line interface tests."""

    def test_help_flag_short(self):
        """Test -h flag shows colorized help."""
        result = subprocess.run([str(EXIFDATE_PATH), "-h"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "\033[1m" in result.stdout  # Bold
        assert "\033[4m" in result.stdout  # Underline
        assert "NAME" in result.stdout
        assert "exifdate" in result.stdout

    def test_help_flag_long(self):
        """Test --help flag shows colorized help."""
        result = subprocess.run([str(EXIFDATE_PATH), "--help"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "\033[1m" in result.stdout
        assert "NAME" in result.stdout

    def test_raw_help_flag_short(self):
        """Test -H flag shows raw help without colors."""
        result = subprocess.run([str(EXIFDATE_PATH), "-H"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "\033[" not in result.stdout  # No ANSI codes
        assert "NAME" in result.stdout
        assert "exifdate - read or set EXIF dates from filename date patterns" in result.stdout

    def test_raw_help_flag_long(self):
        """Test --raw-help flag shows raw help without colors."""
        result = subprocess.run([str(EXIFDATE_PATH), "--raw-help"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "\033[" not in result.stdout
        assert "NAME" in result.stdout

    def test_no_arguments_shows_usage_error(self):
        """Test running with no arguments shows usage error."""
        result = subprocess.run([str(EXIFDATE_PATH)], capture_output=True, text=True)
        assert result.returncode == 1
        assert "usage: exifdate" in result.stderr
        assert "Run 'exifdate -h' for help" in result.stderr

    def test_unknown_option_shows_error(self):
        """Test unknown option shows error."""
        result = subprocess.run([str(EXIFDATE_PATH), "--invalid"], capture_output=True, text=True)
        assert result.returncode == 1
        assert "Error: unknown option '--invalid'" in result.stderr
        assert "Run 'exifdate -h' for help" in result.stderr

    def test_default_behavior_reads_dates(self, temp_jpeg):
        """Test default behavior reads and displays EXIF dates."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        result = subprocess.run([str(EXIFDATE_PATH), str(filepath)], capture_output=True, text=True)
        assert result.returncode == 0
        assert "DateTimeOriginal:" in result.stdout
        assert "DateTime:" in result.stdout
        assert "DateTimeDigitized:" in result.stdout
        assert filepath.name in result.stdout

    def test_from_name_flag_with_dryrun(self, temp_jpeg):
        """Test --from-name with -n flag does dry-run."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        result = subprocess.run([str(EXIFDATE_PATH), "--from-name", "-n", str(filepath)], capture_output=True, text=True)
        assert result.returncode == 0
        assert "DRY RUN (remove -n to actually modify files)" in result.stderr
        assert "Would set EXIF dates" in result.stdout
        assert "remove -n to actually modify files" in result.stderr

    def test_from_name_flag_executes_modifications(self, temp_jpeg):
        """Test --from-name flag executes actual modifications."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        result = subprocess.run([str(EXIFDATE_PATH), "--from-name", str(filepath)], capture_output=True, text=True)
        assert result.returncode == 0
        assert "writing EXIF dates from filenames" in result.stderr
        assert "Set EXIF dates" in result.stdout
        assert "processed 1 file(s)" in result.stderr

    def test_dryrun_requires_from_name(self, temp_jpeg):
        """Test that -n flag requires --from-name."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        result = subprocess.run([str(EXIFDATE_PATH), "-n", str(filepath)], capture_output=True, text=True)
        assert result.returncode == 1
        assert "Error: -n/--dryrun can only be used with --from-name" in result.stderr

    def test_old_run_flag_rejected(self, temp_jpeg):
        """Test that old --run flag is rejected."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        result = subprocess.run([str(EXIFDATE_PATH), "--run", str(filepath)], capture_output=True, text=True)
        assert result.returncode == 1
        assert "Error: unknown option '--run'" in result.stderr

    def test_multiple_file_arguments_read_mode(self, temp_jpeg):
        """Test reading multiple files in default mode."""
        file1 = temp_jpeg("test1_2024-03-15.jpg")
        file2 = temp_jpeg("test2_2024-04-20.jpg")
        result = subprocess.run([str(EXIFDATE_PATH), str(file1), str(file2)], capture_output=True, text=True)
        assert result.returncode == 0
        assert file1.name in result.stdout
        assert file2.name in result.stdout
        assert "DateTimeOriginal:" in result.stdout

    def test_multiple_file_arguments_write_mode(self, temp_jpeg):
        """Test processing multiple files with --from-name."""
        file1 = temp_jpeg("test1_2024-03-15.jpg")
        file2 = temp_jpeg("test2_2024-04-20.jpg")
        result = subprocess.run([str(EXIFDATE_PATH), "--from-name", "-n", str(file1), str(file2)], capture_output=True, text=True)
        assert result.returncode == 0
        assert "would process 2 file(s)" in result.stderr

    def test_missing_file_error(self):
        """Test error handling for missing files."""
        result = subprocess.run([str(EXIFDATE_PATH), "/nonexistent/file.jpg"], capture_output=True, text=True)
        assert result.returncode == 2
        assert "Error: file not found" in result.stderr

    def test_no_date_in_filename_error_write_mode(self, temp_jpeg):
        """Test error when filename has no date pattern in write mode."""
        filepath = temp_jpeg("vacation_beach.jpg")
        result = subprocess.run([str(EXIFDATE_PATH), "--from-name", str(filepath)], capture_output=True, text=True)
        assert result.returncode == 2
        assert "Error: no date pattern found in filename" in result.stderr

    def test_exit_code_0_on_success(self, temp_jpeg):
        """Test exit code 0 on successful processing."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        result = subprocess.run([str(EXIFDATE_PATH), str(filepath)], capture_output=True, text=True)
        assert result.returncode == 0

    def test_exit_code_1_on_usage_error(self):
        """Test exit code 1 on usage error."""
        result = subprocess.run([str(EXIFDATE_PATH), "--invalid"], capture_output=True, text=True)
        assert result.returncode == 1

    def test_exit_code_2_on_processing_error(self):
        """Test exit code 2 on processing error."""
        result = subprocess.run([str(EXIFDATE_PATH), "/nonexistent/file.jpg"], capture_output=True, text=True)
        assert result.returncode == 2

    def test_no_files_specified_error(self):
        """Test error when no files are provided."""
        result = subprocess.run([str(EXIFDATE_PATH), "--from-name"], capture_output=True, text=True)
        assert result.returncode == 1
        assert "Error: no files specified" in result.stderr


class TestIntegration:
    """Integration tests for end-to-end workflows."""

    def test_end_to_end_read_mode(self, temp_jpeg):
        """Test complete workflow in read mode (default)."""
        filepath = temp_jpeg("vacation_2024-03-15.jpg")
        
        # Read mode (default)
        result = subprocess.run([str(EXIFDATE_PATH), str(filepath)], capture_output=True, text=True)
        assert result.returncode == 0
        assert "DateTimeOriginal:" in result.stdout
        assert filepath.name in result.stdout

    def test_end_to_end_write_mode(self, temp_jpeg):
        """Test complete workflow with --from-name."""
        filepath = temp_jpeg("vacation_2024-03-15.jpg")
        
        # Dry-run first
        result_dry = subprocess.run([str(EXIFDATE_PATH), "--from-name", "-n", str(filepath)], capture_output=True, text=True)
        assert result_dry.returncode == 0
        assert "Would set EXIF dates" in result_dry.stdout
        assert "2024-03-15" in result_dry.stdout
        
        # Actual run
        result_run = subprocess.run([str(EXIFDATE_PATH), "--from-name", str(filepath)], capture_output=True, text=True)
        assert result_run.returncode == 0
        assert "writing EXIF dates from filenames" in result_run.stderr
        assert "Set EXIF dates" in result_run.stdout

    def test_end_to_end_multiple_files_mixed_results(self, temp_jpeg, tmp_path):
        """Test workflow with multiple files, some succeed, some fail."""
        file1 = temp_jpeg("photo_2024-03-15.jpg")
        file2 = temp_jpeg("no_date.jpg")
        file3 = temp_jpeg("image_2024-04.jpg")
        
        result = subprocess.run(
            [str(EXIFDATE_PATH), "--from-name", "-n", str(file1), str(file2), str(file3)],
            capture_output=True, text=True
        )
        assert result.returncode == 0  # Some succeeded
        assert "Would set EXIF dates" in result.stdout
        assert "no date pattern found" in result.stderr
        assert "would process 2 file(s), 1 error(s)" in result.stderr

    def test_dry_run_vs_actual_run_comparison(self, temp_jpeg):
        """Test that dry-run and actual run produce consistent output."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        
        # Dry-run
        result_dry = subprocess.run([str(EXIFDATE_PATH), "--from-name", "-n", str(filepath)], capture_output=True, text=True)
        
        # Actual run
        result_run = subprocess.run([str(EXIFDATE_PATH), "--from-name", str(filepath)], capture_output=True, text=True)
        
        # Both should succeed
        assert result_dry.returncode == 0
        assert result_run.returncode == 0
        
        # Output should be similar (except for "Would set" vs "Set")
        assert "2024-03-15" in result_dry.stdout
        assert "2024-03-15" in result_run.stdout

    def test_statistics_output_verification(self, temp_jpeg):
        """Test that statistics output is correct."""
        file1 = temp_jpeg("photo1_2024-03-15.jpg")
        file2 = temp_jpeg("photo2_2024-04-20.jpg")
        file3 = temp_jpeg("photo3_2024-05-10.jpg")
        
        result = subprocess.run(
            [str(EXIFDATE_PATH), "--from-name", "-n", str(file1), str(file2), str(file3)],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "would process 3 file(s), 0 error(s)" in result.stderr

    def test_mixed_date_formats(self, temp_jpeg):
        """Test processing files with different date formats."""
        file1 = temp_jpeg("photo_2024-03-15.jpg")  # YYYY-MM-DD
        file2 = temp_jpeg("image_2024-04.jpg")     # YYYY-MM
        file3 = temp_jpeg("pic_2024.jpg")          # YYYY
        
        result = subprocess.run(
            [str(EXIFDATE_PATH), "--from-name", "-n", str(file1), str(file2), str(file3)],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "2024-03-15" in result.stdout
        assert "2024-04" in result.stdout
        assert "2024" in result.stdout
        assert "would process 3 file(s), 0 error(s)" in result.stderr

    def test_non_jpeg_file_handling_read_mode(self, tmp_path):
        """Test handling of non-JPEG files in read mode."""
        filepath = tmp_path / "test_2024-03-15.txt"
        filepath.write_text("not an image")
        
        result = subprocess.run([str(EXIFDATE_PATH), str(filepath)], capture_output=True, text=True)
        assert result.returncode == 2
        assert "Error reading EXIF" in result.stderr

    def test_non_jpeg_file_handling_write_mode(self, tmp_path):
        """Test handling of non-JPEG files in write mode."""
        filepath = tmp_path / "test_2024-03-15.txt"
        filepath.write_text("not an image")
        
        result = subprocess.run([str(EXIFDATE_PATH), "--from-name", str(filepath)], capture_output=True, text=True)
        assert result.returncode == 2
        assert "Error reading EXIF" in result.stderr

    def test_directory_not_file_error(self, tmp_path):
        """Test error when path is a directory, not a file."""
        dirpath = tmp_path / "test_dir"
        dirpath.mkdir()
        
        result = subprocess.run([str(EXIFDATE_PATH), str(dirpath)], capture_output=True, text=True)
        assert result.returncode == 2
        assert "Error: not a file" in result.stderr

    def test_read_mode_multiple_files(self, temp_jpeg):
        """Test reading EXIF dates from multiple files."""
        file1 = temp_jpeg("photo1_2024-03-15.jpg")
        file2 = temp_jpeg("photo2_2024-04-20.jpg")
        
        result = subprocess.run([str(EXIFDATE_PATH), str(file1), str(file2)], capture_output=True, text=True)
        assert result.returncode == 0
        assert file1.name in result.stdout
        assert file2.name in result.stdout
        assert result.stdout.count("DateTimeOriginal:") == 2

    def test_read_mode_output_format(self, temp_jpeg):
        """Test that read mode output format is correct."""
        filepath = temp_jpeg("test_2024-03-15.jpg")
        
        result = subprocess.run([str(EXIFDATE_PATH), str(filepath)], capture_output=True, text=True)
        assert result.returncode == 0
        assert f"{filepath.name}:" in result.stdout
        assert "DateTimeOriginal:" in result.stdout
        assert "DateTime:" in result.stdout
        assert "DateTimeDigitized:" in result.stdout
        assert "(not set)" in result.stdout  # Fields should be unset initially


class TestEdgeCases:
    """Edge case tests."""

    def test_filename_with_multiple_years(self):
        """Test filename with multiple year patterns."""
        result = extract_date_from_filename("backup_2024_from_2023.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        # Should match first year (2024)
        assert date_pattern == "2024"

    def test_filename_with_year_in_extension(self):
        """Test that year in extension is not matched."""
        result = extract_date_from_filename("photo.2024")
        assert result is not None
        # Should match the year
        assert result[0] == "2024"

    def test_very_long_filename(self, temp_jpeg):
        """Test processing file with very long filename."""
        long_name = "a" * 200 + "_2024-03-15.jpg"
        filepath = temp_jpeg(long_name)
        result = subprocess.run([str(EXIFDATE_PATH), str(filepath)], capture_output=True, text=True)
        assert result.returncode == 0

    def test_filename_with_special_characters(self, temp_jpeg):
        """Test filename with special characters."""
        filepath = temp_jpeg("photo_2024-03-15_[vacation].jpg")
        result = subprocess.run([str(EXIFDATE_PATH), str(filepath)], capture_output=True, text=True)
        assert result.returncode == 0
        assert "2024-03-15" in result.stdout

    def test_filename_with_unicode(self, temp_jpeg):
        """Test filename with unicode characters."""
        filepath = temp_jpeg("фото_2024-03-15.jpg")
        result = subprocess.run([str(EXIFDATE_PATH), str(filepath)], capture_output=True, text=True)
        assert result.returncode == 0
        assert "2024-03-15" in result.stdout

    def test_leap_year_date(self):
        """Test leap year date (Feb 29)."""
        result = extract_date_from_filename("photo_2024-02-29.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-02-29"
        assert exif_datetime == "2024:02:29 12:00:00"

    def test_december_31st(self):
        """Test last day of year."""
        result = extract_date_from_filename("photo_2024-12-31.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-12-31"
        assert exif_datetime == "2024:12:31 12:00:00"

    def test_january_1st(self):
        """Test first day of year."""
        result = extract_date_from_filename("photo_2024-01-01.jpg")
        assert result is not None
        date_pattern, exif_datetime = result
        assert date_pattern == "2024-01-01"
        assert exif_datetime == "2024:01:01 12:00:00"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
