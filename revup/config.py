import argparse
import configparser
import os
import re
from typing import Optional


class Config:
    # Object containing configuration values. Populated by read(), and can then
    # be modified by set_value()
    config: configparser.ConfigParser

    # Path to user global config file
    config_path: str

    # Path to config file in current repo
    repo_config_path: str

    # Whether the config contains values that need to be flushed to the file
    dirty: bool = False

    def __init__(self, config_path: str, repo_config_path: str):
        self.config = configparser.ConfigParser()
        self.config_path = config_path
        self.repo_config_path = repo_config_path

    def read(self) -> None:
        self.config.read(self.config_path)
        self.config.read(self.repo_config_path)

    def write(self) -> None:
        if not self.dirty:
            return

        # Ensure the file is created with secure permissions, due to containing credentials
        with os.fdopen(
            os.open(self.config_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w"
        ) as f:
            self.config.write(f)
        self.dirty = False

    def set_value(self, section: str, key: str, value: str, repo: Optional[str]) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)
            self.dirty = True

        if not self.config.has_option(section, key) or self.config.get(section, key) != value:
            self.config.set(section, key, value)
            self.dirty = True

    def get_config(self) -> configparser.ConfigParser:
        return self.config


def config_main(conf: Config, args: argparse.Namespace) -> int:
    command = args.command[0]
    key = args.flag[0].replace("-", "_")
    value = args.value[0]

    # TODO repo stuff

    if command == "revup" and key == "github_username":
        # From https://www.npmjs.com/package/github-username-regex :
        # Github username may only contain alphanumeric characters or hyphens.
        # Github username cannot have multiple consecutive hyphens.
        # Github username cannot begin or end with a hyphen.
        # Maximum is 39 characters.
        if not re.match(r"^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$", value, re.I):
            raise ValueError(f"{args.value} is not a valid GitHub username")
    elif command == "revup" and key == "github_oauth":
        # TODO: Validate oauth
        if not re.match(r"^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$", value, re.I):
            raise ValueError("Input string is not a valid oauth")

    conf.set_value(command, key, value, args.repo)
    conf.write()
    return 0
