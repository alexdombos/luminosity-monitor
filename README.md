# Repository for luminosity monitor

Intended to be used while tuning the beam through HIPPO, in order to monitor the luminosity as a function of time as the beam interacts with the gas jet

# Directions
1. Connect via `ssh` to the Raspberry Pi Camera and start the video server. This can only be done from stg@redacted-stg-hostname
    - `stg@redacted-stg-hostname $ ssh pi@redacted-rbpi-hostname`
    - `pi@redacted-rbpi-hostname $ ./kill_server.sh`
        - This is done to make sure you start with the server (next line) on `/dev/video0`
    - `pi@redacted-rbpi-hostname $ ./start_server.sh`
        - This will start the video server. Make sure that the last line contains: `<notice> [core] Registering device node /dev/video0`
	- The full output should be:
	  <notice> [core] Trying to load driver 'raspicam' from built-in drivers first...
	  <warning> [core] Driver 'raspicam' not found
	  <notice> [core] Trying to load driver 'raspicam' from external plug-in's instead...
	  <notice> [driver] Dual Raspicam & TC358743 Video4Linux2 Driver v1.9.59 built Nov 11 2017
	  <notice> [driver] Detected camera imx219, 3280x2464
	  <notice> [driver] Selected format: 480x640, encoding: h264, H264 Video Compression
	  <notice> [driver] Framerate max. 10 fps
	  <notice> [driver] ROI: 0, 0, 1, 1
	  <notice> [driver] H264 costant bitrate: 8000000
	  <notice> [core] Device detected!
	  <notice> [core] Registering device node /dev/video0
	- If the output contains `<warning> [driver] Cannot read cameara info, keeping the defaults for OV5647` then there is a problem with the cable connection (disconnected or wrong orientation) between the camera and Raspberry Pi
	    - If you disconnect then connect the cable between the camera and Raspberry Pi, you must reboot the Raspberry Pi (`kill_server.sh` and `start_server.sh` is insufficient)
    - `pi@redacted-rbpi-hostname $ exit`
3. Start the luminosity monitor
    - `stg@redacted-stg-hostname $ cd /home/stg/luminosity-monitor`
    - `stg@redacted-stg-hostname $ ./luminosity_monitor.py`
