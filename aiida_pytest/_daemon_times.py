import os
import json

import aiida

def set_daemon_interval_times(time=5):
    filename = os.path.join(aiida.common.setup.AIIDA_CONFIG_FOLDER, 'config.json')

    with open(filename) as f:
        config = json.load(f)

    for profile_config in config['profiles'].values():
        for key in [
            "DAEMON_INTERVALS_SUBMIT",
            "DAEMON_INTERVALS_UPDATE",
            "DAEMON_INTERVALS_RETRIEVE"
        ]:
            profile_config[key] = time

    with open(filename, 'w') as f:
        json.dump(config, f)
