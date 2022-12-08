# rpirrigation
raspberry pi scheduled irrigation with relays and electrovalve
Controls GPIO pins 5,6,13,19 connected trough relays to 4 waterring electrovalves  
Put the irrigation.py and irrigation_config.yml in /home/pi
Modify yaml file as you needed

Run is as service at startup:

1. Create file to Define the service and add below content
  $sudo nano /lib/systemd/system/irrigation.service
  
      [Unit]
	    Description=Test Sevice
	    After=multi-user.target

	    [Service]
	    Type=simple
	    ExecStart=/usr/bin/python /home/pi/irrigation.py
	    Restart=on-abort

	    [Install]
	    WantedBy=multi-user.target
     
2. Activate the service
    $sudo chmod 644 /lib/systemd/system/irrigation.service
    $chmod +x /home/pi/irrigation.py
    $sudo systemctl daemon-reload
    $sudo systemctl enable irrigation.service

    Start service
    $sudo systemctl start irrigation.service

    Check service status
    $sudo systemctl status irrigation.service
