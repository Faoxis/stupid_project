import subprocess
import os
import time

import logging
import yaml
from datetime import datetime, timedelta
from threading import Thread

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', filename='logs/all.log', level=logging.DEBUG)


class LogDownloader(Thread):

    def run(self):
        while True:
            self.download_last_log_file()
            time.sleep(60 * 60 * 24) # once a day

    def download_last_log_file(self):

        logging.info('start download')
        with open('config/ssh.yaml') as ssh_config_file:
            ssh_user = yaml.load(ssh_config_file.read())

        cmd = ['sshpass', '-p', ssh_user['password'],
               'scp', '-P', '65022', ssh_user['username'] + '@192.168.100.41:/var/log/dovecot.log.1.gz', './files/']
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        logging.info('Logfile has been downloaded')

        prefix = str(datetime.now() - timedelta(days=1)).split(' ')[0].replace('-', '_')
        os.rename('files/dovecot.log.1.gz', os.path.join('files', prefix + '.gz'))
        logging.info('Logfile has been renamed')

if __name__ == '__main__':
    LogDownloader().download_last_log_file()