# Copyright 2016, RadiantBlue Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import os
import sys
import datetime
import logging.config

FORMAT = ('<%(PRI)s>1 %(TIMESTAMP)s %(HOSTNAME)s %(APP_NAME)s %(process)s %(MSG_ID)s %(SD_ELEMENT)s'
          '(%(name)s:%(funcName)s) %(levelname)s %(message)s')

PRI_CODES = {
    'FATAL':    0,
    'CRITICAL': 2,
    'ERROR':    3,
    'WARN':     4,
    'WARNING':  4,
    'NOTICE':   5,
    'INFO':     6,
    'DEBUG':    7,
}


def init_logger(logLevel=logging.DEBUG, muted=False):
    logging.basicConfig(
        format=FORMAT,
        level=logLevel,
        stream=sys.stdout
    )

    logging.setLoggerClass(AuditableLogger)
    logger = logging.getLogger(__name__)
    if muted:
        logging.root.handlers = [logging.NullHandler()]

    # overall logging level
    logger.setLevel(1)
    return logger


def mute_logger():
    """ Mute the logger """
    logging.root.handlers = [logging.NullHandler()]


class AuditableLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None,
             actee='', action='', actor='', **kwargs):
        sd_params = []
        if actor:
            sd_params.append('actor="{}"'.format(actor))
        if action:
            sd_params.append('action="{}"'.format(action))
        if actee:
            sd_params.append('actee="{}"'.format(os.path.abspath(actee)))

        sd_element = ''
        if sd_params:
            sd_element = '[{SD_ID} {SD_PARAMS}] '.format(
                SD_ID='bfaudit@48851',
                SD_PARAMS=' '.join(sd_params),
            )

        pri = (1 << 3) | PRI_CODES.get(logging.getLevelName(level), PRI_CODES['NOTICE'])

        # Assemble RFC 5424 elements
        extra = {
            'ACTEE':     actee,
            'ACTION':    action,
            'ACTOR':     actor,
            'APP_NAME':  __name__.split('.')[0],
            'HOSTNAME':  os.uname()[1].lower(),
            'MSG_ID':    '-',
            'PRI':       pri,
            'SD_ELEMENT': sd_element,
            'TIMESTAMP': datetime.datetime.utcnow().isoformat() + 'Z',
        }

        super(AuditableLogger, self)._log(level, msg, args, exc_info, extra)
