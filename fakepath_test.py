#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Brian Holtz
# SPDX-License-Identifier: MIT

import sys
import tempfile
from pathlib import Path
import pytest

# Import fakepath module
sys.path.insert(0, str(Path(__file__).parent))
from fakepath import fakepath


class TestFakepathBasic:
    """Basic functionality tests."""

    def test_simple_absolute_path(self):
        """Simple absolute path produces expected format."""
        result = fakepath("/Users/alice/project/README.md")
        assert "_" in result
        parts = result.split("_")
        assert len(parts) >= 3  # parent_basename_hash
        assert "README.md" in result

    def test_deterministic(self):
        """Same input always produces same output."""
        path = "/Users/alice/src/project/file.txt"
        result1 = fakepath(path)
        result2 = fakepath(path)
        assert result1 == result2

    def test_relative_path_resolved(self):
        """Relative path is resolved to canonical form."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("content")

            # Get key using relative path
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                result_rel = fakepath("./test.txt")
                os.chdir(old_cwd)
                result_abs = fakepath(str(test_file))
                # Both should produce the same key (same canonical path)
                assert result_rel == result_abs
            finally:
                os.chdir(old_cwd)


class TestFakepathFormat:
    """Format and structure tests."""

    def test_output_format_parent_basename_hash(self):
        """Output follows <parent>_<basename>_<hash> format."""
        result = fakepath("/Users/alice/src/README.md")
        # Should have at least 2 underscores (parent_basename_hash)
        assert result.count("_") >= 2
        # Last segment should be hex (the hash)
        parts = result.rsplit("_", 1)
        assert len(parts) == 2
        hash_part = parts[1]
        # Hash should be hex digits (8 by default)
        assert all(c in "0123456789abcdef" for c in hash_part)

    def test_parent_chars_truncation(self):
        """Parent path is truncated to parent_chars."""
        path = "/Users/alice/very/long/directory/structure/file.txt"
        result = fakepath(path, parent_chars=20)
        # Parent part should be max 20 chars + underscore
        parts = result.split("_", 1)
        parent_part = parts[0]
        assert len(parent_part) <= 20

    def test_basename_chars_truncation(self):
        """Basename is truncated to basename_chars."""
        result = fakepath(
            "/path/file_with_a_very_long_name_that_exceeds_normal_limits.txt",
            basename_chars=20
        )
        # Extract basename part (between 1st and 2nd-to-last underscore)
        parts = result.rsplit("_", 1)  # Remove hash
        remaining = parts[0]
        # Find the basename (after last _ in remaining)
        basename_part = remaining.rsplit("_", 1)[-1]
        assert len(basename_part) <= 20

    def test_hash_chars_length(self):
        """Hash suffix respects hash_chars parameter."""
        result_8 = fakepath("/path/file.txt", hash_chars=8)
        result_12 = fakepath("/path/file.txt", hash_chars=12)

        hash_8 = result_8.rsplit("_", 1)[1]
        hash_12 = result_12.rsplit("_", 1)[1]

        assert len(hash_8) == 8
        assert len(hash_12) == 12


class TestFakepathSlashHandling:
    """Path separator handling tests."""

    def test_slashes_replaced_with_underscores_in_parent(self):
        """Slashes in parent path are replaced with underscores."""
        result = fakepath("/Users/alice/src/project/file.txt", parent_chars=100)
        # Result should not contain "/" in the parent part (only in the path itself)
        parts = result.rsplit("_", 1)  # Remove hash
        parent_and_basename = parts[0]
        # The parent part should have underscores, not slashes
        assert "/" not in parent_and_basename or parent_and_basename.count("/") == 0

    def test_different_paths_different_keys(self):
        """Different paths produce different keys."""
        result1 = fakepath("/Users/alice/file.txt")
        result2 = fakepath("/Users/bob/file.txt")
        assert result1 != result2


class TestFakepathEdgeCases:
    """Edge case tests."""

    def test_very_long_path(self):
        """Very long path produces valid key within limits."""
        long_path = "/very/long/directory/structure/with/many/levels/deeply/nested/file_with_a_very_long_name.txt"
        result = fakepath(long_path)
        # Result should be < 255 chars (filesystem limit)
        assert len(result) < 255

    def test_short_basename(self):
        """Short basename is not truncated."""
        result = fakepath("/Users/alice/a.txt", basename_chars=120)
        assert "a.txt" in result

    def test_single_level_path(self):
        """Path with minimal depth is handled."""
        result = fakepath("/file.txt")
        assert "file.txt" in result

    def test_path_with_dots(self):
        """Path with . and .. is resolved correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "subdir" / "file.txt"
            test_file.parent.mkdir()
            test_file.write_text("content")

            # Create a key using .. notation
            path_with_dots = str(test_file.parent / ".." / "subdir" / "file.txt")
            result = fakepath(path_with_dots)
            # Should resolve and produce valid output
            assert "_" in result
            assert len(result) < 255

    def test_path_with_spaces(self):
        """Path with spaces is preserved in key."""
        result = fakepath("/Users/alice/My Documents/my file.txt")
        # Spaces should be preserved (no special handling)
        assert "My" in result or "my" in result

    def test_symlink_resolved(self):
        """Symlinks are resolved to real paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create real file and symlink
            real_file = Path(tmpdir) / "real.txt"
            real_file.write_text("content")
            link_file = Path(tmpdir) / "link.txt"
            link_file.symlink_to(real_file)

            # Both should resolve to the same canonical path
            result_real = fakepath(str(real_file))
            result_link = fakepath(str(link_file))
            assert result_real == result_link


class TestFakepathCollisionResistance:
    """Collision resistance and hash verification."""

    def test_8char_hash_different_for_different_files(self):
        """Different files produce different hashes."""
        path1 = "/Users/alice/Documents/file1.txt"
        path2 = "/Users/alice/Documents/file2.txt"

        result1 = fakepath(path1, hash_chars=8)
        result2 = fakepath(path2, hash_chars=8)

        hash1 = result1.rsplit("_", 1)[1]
        hash2 = result2.rsplit("_", 1)[1]

        assert hash1 != hash2

    def test_hash_is_hex(self):
        """Hash suffix is always valid hexadecimal."""
        result = fakepath("/Users/alice/file.txt", hash_chars=8)
        hash_part = result.rsplit("_", 1)[1]
        # All characters should be valid hex
        assert all(c in "0123456789abcdef" for c in hash_part)


class TestFakepathErrors:
    """Error handling tests."""

    def test_nonexistent_path_raises_error(self):
        """Nonexistent path raises ValueError."""
        with pytest.raises(ValueError):
            fakepath("/nonexistent/path/file.txt")

    def test_empty_path_raises_error(self):
        """Empty path raises ValueError."""
        with pytest.raises(ValueError):
            fakepath("")

    def test_invalid_parent_chars_raises_error(self):
        """Invalid parent_chars parameter raises error."""
        with pytest.raises((ValueError, TypeError)):
            fakepath("/Users/alice/file.txt", parent_chars=-1)

    def test_invalid_basename_chars_raises_error(self):
        """Invalid basename_chars parameter raises error."""
        with pytest.raises((ValueError, TypeError)):
            fakepath("/Users/alice/file.txt", basename_chars=0)

    def test_invalid_hash_chars_raises_error(self):
        """Invalid hash_chars parameter raises error."""
        with pytest.raises((ValueError, TypeError)):
            fakepath("/Users/alice/file.txt", hash_chars=-1)


class TestFakepathRealWorldScenarios:
    """Real-world usage scenarios."""

    def test_markdown_file_key(self):
        """Markdown file produces valid key."""
        result = fakepath("/Users/alice/src/docs/README.md")
        assert "README.md" in result
        assert len(result) < 255

    def test_deeply_nested_python_file(self):
        """Deeply nested Python file produces valid key."""
        result = fakepath("/Users/alice/src/myproject/package/subpackage/module/utils.py")
        assert "utils.py" in result
        assert len(result) < 255

    def test_config_file_in_home(self):
        """Config file in home directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / ".config" / "app.conf"
            config_file.parent.mkdir()
            config_file.write_text("config")

            result = fakepath(str(config_file))
            assert ".config" in result or "app.conf" in result
            assert len(result) < 255


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
