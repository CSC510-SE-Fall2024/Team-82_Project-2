"""
Copyright (C) Team-82_Project-2
 
Licensed under the MIT License.
See the LICENSE file in the project root for the full license information.
"""

import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))

sys.path.insert(1, root_dir)
from src.modules import full_version
from src.modules import csv_writer
from src.modules import features
import random
import string
import os
import json
import pytest

def test_set_player_name(monkeypatch):
    fv = full_version.full_version()
    if not os.path.exists(fv.default_user_file):
        name = "".join(random.choices(string.ascii_lowercase, k=5)) 
        answers = iter([name])
        monkeypatch.setattr('builtins.input', lambda name: next(answers))

        assert fv.login() == name
    else:
        with open(fv.default_user_file) as json_file:
            data = json.load(json_file)
            name = data["name"]
        assert fv.login() == name

def test_change_user(monkeypatch, capfd):
    fv = full_version.full_version()
    features.create_user('test','pass')
    fv.name = 'test'
    answers = iter(["user1"])
    monkeypatch.setattr('builtins.input', lambda name: next(answers))
    fv.change_user()
    out, err = capfd.readouterr()
    assert "Welcome" in out

def test_csv_writer():
    x = csv_writer.write_csv([{"name": "parth", "surname": "parikh", "age": 10}], "Names", ".")
    assert x[:5] == "Names"