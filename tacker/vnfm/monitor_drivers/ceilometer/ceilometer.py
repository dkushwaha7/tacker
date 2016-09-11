#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

from oslo_config import cfg
from oslo_log import log as logging
import random
import string
import smtplib
from tacker.common import utils
from tacker.vnfm.monitor_drivers import alarm_abstract_driver


LOG = logging.getLogger(__name__)

trigger_opts = [
    cfg.StrOpt('host', default=utils.get_hostname(),
               help=_('Address which drivers use to trigger')),
    cfg.PortOpt('port', default=9890,
               help=_('number of seconds to wait for a response'))
]
cfg.CONF.register_opts(trigger_opts, group='trigger')


def config_opts():
    return [('trigger', trigger_opts)]

ALARM_INFO = (
    ALARM_ACTIONS, OK_ACTIONS, REPEAT_ACTIONS, ALARM,
    INSUFFICIENT_DATA_ACTIONS, DESCRIPTION, ENABLED, TIME_CONSTRAINTS,
    SEVERITY,
) = (
    'alarm_actions', 'ok_actions', 'repeat_actions', 'alarm'
    'insufficient_data_actions', 'description', 'enabled', 'time_constraints',
    'severity',
)

TACKER_EMAIL = {'email': 'message.tacker@gmail.com', 'password': 'tacker123'}


class VNFMonitorCeilometer(alarm_abstract_driver.VNFMonitorAbstractAlarmDriver):
    def get_type(self):
        return 'ceilometer'

    def get_name(self):
        return 'ceilometer'

    def get_description(self):
        return 'Tacker VNFMonitor Ceilometer Driver'

    def _create_alarm_url(self, vnf_id, mon_policy_name, mon_policy_action):
        # alarm_url = 'http://host:port/v1.0/vnfs/vnf-uuid/monitoring-policy-name/action-name?key=8785'
        host = cfg.CONF.trigger.host
        port = cfg.CONF.trigger.port
        LOG.info(_("Tacker in heat listening on %(host)s:%(port)s"),
                 {'host': host,
                  'port': port})
        origin = "http://%(host)s:%(port)s/v1.0/vnfs" % {'host': host, 'port': port}
        access_key = ''.join(
            random.SystemRandom().choice(string.ascii_lowercase + string.digits)
            for _ in range(8))
        alarm_url = "".join([origin, '/', vnf_id, '/', mon_policy_name, '/',
                             mon_policy_action, '/', access_key])
        return alarm_url

    def call_alarm_url(self, vnf, kwargs):
        '''must be used after call heat-create in plugin'''
        return self._create_alarm_url(**kwargs)

    def _process_alarm(self, params):
        if params['data'].get('alarm_id') and params['data'].get('current') == ALARM:
            return True

    def process_alarm(self, vnf,kwargs):
        '''Check alarm state. if available, will be processed'''
        return self._process_alarm(**kwargs)

    def _process_notification(self, rc_email_address, content):
        mail = smtplib.SMTP('smtp.gmail.com', 9890)
        mail.ehlo()
        mail.starttls()
        mail.login(TACKER_EMAIL['email'], TACKER_EMAIL['password'])
        # Send message
        try:
            mail.sendmail(TACKER_EMAIL['email'], rc_email_address, content)
            return True
        except Exception:
            return False
        finally:
            mail.close()

    def process_notification(self, vnf, kwargs):
        return self._process_notification(**kwargs)




