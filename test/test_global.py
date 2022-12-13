# Standard libraries
import datetime
import os
import pytest
import random
import re
import string
import sys

# Fixing the paths
path = os.path.dirname(__file__)
if not path:
    path = '.'
sys.path.append('{}/../'.format(path))
sys.path.append('{}/libs/'.format(path))

# Local libraries, we need the path for that
import clock_time  # noqa: E402

# Get a filename that is unlikely to be used
test_db_name = 'ci_test_{}.sql'.format(
    ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))

# Testing the creation of the DB


def test_db_generation(monkeypatch):
    if os.path.exists(test_db_name):
        os.system('rm -f {}'.format(test_db_name))

    monkeypatch.setattr(
        sys, 'argv', ['time_clock', '--sqlite-file', test_db_name])
    clock_time.main_function()
    assert os.path.exists(test_db_name)

    # Clean up
    os.system('rm -f {}'.format(test_db_name))


# Testing the days
def test_days(monkeypatch, capsys):
    # Pre-clean up if needed
    if os.path.exists(test_db_name):
        os.system('rm -f {}'.format(test_db_name))

    # Create an entry
    monkeypatch.setattr(sys, 'argv', [
                        'time_clock', '--sqlite-file', test_db_name, 'day', 'office', '--date', '2000-01-01'])
    clock_time.main_function()
    assert os.path.exists(test_db_name)

    # More entries
    monkeypatch.setattr(sys, 'argv', [
                        'time_clock', '--sqlite-file', test_db_name, 'day', 'wfh', '--date', '2000-01-02'])
    clock_time.main_function()
    monkeypatch.setattr(sys, 'argv', [
                        'time_clock', '--sqlite-file', test_db_name, 'day', 'trip', '--date', '2000-01-03'])
    clock_time.main_function()
    monkeypatch.setattr(sys, 'argv', [
                        'time_clock', '--sqlite-file', test_db_name, 'day', 'sick', '--date', '2000-01-04'])
    clock_time.main_function()
    monkeypatch.setattr(sys, 'argv', [
                        'time_clock', '--sqlite-file', test_db_name, 'day', 'free', '--date', '2000-01-05'])
    clock_time.main_function()

    # One further entry on the current day
    monkeypatch.setattr(
        sys, 'argv', ['time_clock', '--sqlite-file', test_db_name, 'day', 'office'])
    clock_time.main_function()

    # Test that all what we entered worked as expected
    monkeypatch.setattr(
        sys, 'argv', ['time_clock', '--sqlite-file', test_db_name, 'day', '--list'])
    clock_time.main_function()
    out, err = capsys.readouterr()
    assert not err
    assert '2000-01-01: Working at the office\n2000-01-02: Home office\n2000-01-03: Business trip\n2000-01-04: Sick day\n2000-01-05: Holiday or other non-worked days\n{}: Working at the office\n'.format(
        datetime.date.today().isoformat()) == out

    # Test deleting an entry
    monkeypatch.setattr(sys, 'argv', [
                        'time_clock', '--sqlite-file', test_db_name, 'day', '--delete', '--date', '2000-01-04'])
    clock_time.main_function()
    monkeypatch.setattr(
        sys, 'argv', ['time_clock', '--sqlite-file', test_db_name, 'day', '--list'])
    clock_time.main_function()
    out, err = capsys.readouterr()
    assert not err
    assert '2000-01-01: Working at the office\n2000-01-02: Home office\n2000-01-03: Business trip\n2000-01-05: Holiday or other non-worked days\n{}: Working at the office\n'.format(
        datetime.date.today().isoformat()) == out

    # Test modifying an entry
    monkeypatch.setattr(sys, 'argv', ['time_clock', '--sqlite-file',
                                      test_db_name, 'day', 'trip', '--date', '2000-01-05', '--edit'])
    clock_time.main_function()
    out, err = capsys.readouterr()
    assert not err
    assert 'Updating from free to trip for 2000-01-05\n' == out
    monkeypatch.setattr(
        sys, 'argv', ['time_clock', '--sqlite-file', test_db_name, 'day', '--list'])
    clock_time.main_function()
    out, err = capsys.readouterr()
    assert not err
    assert '2000-01-01: Working at the office\n2000-01-02: Home office\n2000-01-03: Business trip\n2000-01-05: Business trip\n{}: Working at the office\n'.format(
        datetime.date.today().isoformat()) == out

    # Test some random parameter
    rn = ''.join(random.choices(string.ascii_uppercase, k=6))
    monkeypatch.setattr(
        sys, 'argv', ['time_clock', '--sqlite-file', test_db_name, 'day', rn])
    with pytest.raises(SystemExit):
        clock_time.main_function()
    out, err = capsys.readouterr()
    assert not out
    assert 'Err: wrong parameter ({}), possible choices: office, wfh, trip, sick, free\n'.format(
        rn) == err
    monkeypatch.setattr(sys, 'argv', [
                        'time_clock', '--sqlite-file', test_db_name, 'day', '--{}'.format(rn)])
    with pytest.raises(SystemExit):
        clock_time.main_function()
    out, err = capsys.readouterr()
    assert not out
    assert re.match(
        'usage:.+\ntime_clock: error: unrecognized arguments: --{}\n'.format(rn), err) is not None

    # Clean up
    os.system('rm -f {}'.format(test_db_name))
