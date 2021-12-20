#!/usr/bin/env python3
import unittest

from about import properties
from utils.cmd_utils import CmdUtils


class FlaskServerTestCase(unittest.TestCase):
    ip = "localhost"
    port = "8080"
    username = "admin"
    password = "estuaryoss123!"
    file = "config.yaml"
    exec = "python"
    main_path = "main.py"

    def test_cli_exit_status_0(self):
        response = CmdUtils.run_cmd_shell_true(f"{self.exec} {self.main_path} "
                                               f"--username=\"{self.username}\" "
                                               f"--password=\"{self.password}\" "
                                               f"--file={self.file}")

        print(response)
        self.assertIn(f"{properties.get('version')}", response.get('out'))
        self.assertIn("Global exit code: 0", response.get('out'))


if __name__ == '__main__':
    unittest.main()
