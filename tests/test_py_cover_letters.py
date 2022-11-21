#!/usr/bin/env python
"""Tests for `py_cover_letters` package."""

from click.testing import CliRunner

from py_cover_letters import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'py-cover-letters' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_config_show():
    runner = CliRunner()
    result = runner.invoke(cli.main, ['config', 'show'], input='\n'.join('N'))
    print('>>>', result.output)
