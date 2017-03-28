"""
beachfront-py
https://github.com/venicegeo/beachfront-py

Copyright 2016, RadiantBlue Technologies, Inc.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import logging
import unittest
from beachfront.logger import init_logger


class TestLoggers(unittest.TestCase):
    ''' Test Cumulus logger '''

    def setUp(self):
        """ Clear root handlers """
        logging.root.handlers = []

    def test_config_null(self):
        """ Check configuration of muted logger """
        init_logger(muted=True)
        # null handler
        logger = logging.getLogger(__name__)
        self.assertEqual(len(logger.root.handlers), 1)
        self.assertTrue(isinstance(logger.root.handlers[0], logging.NullHandler))

    def test_config_stdout(self):
        """ Check configuration of logger with stdout stream """
        init_logger()
        logger = logging.getLogger(__name__)
        self.assertEqual(len(logger.root.handlers), 1)

        self.assertTrue(isinstance(logger.root.handlers[0], logging.StreamHandler))

    def _test_logging(self):
        """ Log messages """
        init_logger()
        logger = logging.getLogger(__name__)
        logger.info('logging test')
