Be sure to change the following variables to your own

The following are the variables which need to be changed:
- username: The username for the RTSP stream authentication.
- password: The password for the RTSP stream authentication.
- rtsp_url: The RTSP stream URL, which incorporates the encoded username and password.

If you are having issues with the accuracy in detecting once movement has stopped, it might be worth increasing this variable.
- no_movement_time_threshold: The time threshold (in seconds) for detecting no movement (10 seconds in the example).
