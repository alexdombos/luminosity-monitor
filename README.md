# Repository for luminosity monitor

Intended to be used while tuning the beam through HIPPO, in order to monitor the luminosity as a function of time as the beam interacts with the gas jet

# Directions
1. Connect via `ssh` to the Raspberry Pi Camera and start the video server. This can only be done from stg@redacted-stg-hostname
    - `stg@redacted-stg-hostname $ ssh pi@redacted-rbpi-hostname`
    - `pi@redacted-rbpi-hostname $ ./kill_server.sh`
        - This is done to make sure you start with the server (next line) on `/dev/video0`
    - `pi@redacted-rbpi-hostname $ ./start_server.sh`
        - This will start the video server. Make sure that the last line contains: `<notice> [core] Registering device node /dev/video0`
    - `pi@redacted-rbpi-hostname $ exit`
3. Start the luminosity monitor
    - `stg@redacted-stg-hostname $ cd /home/stg/luminosity-monitor`
    - `stg@redacted-stg-hostname $ ./luminosity_monitor.py`
