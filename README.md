# osc_rpi_shutdown
 shutdown rpi from osc command

 # Import OSC library
 `pip install pyOSC`



 ` cd /home/pi/Documents `

 ` git clone https://github.com/AurelienConil/osc_rpi_shutdown ` 
 
 `cd osc_rpi_shutdown`

# Activer les scripts en execution

`
cd script
sudo chmod 777 shutdown.sh
sudo chmod 777 reboot.sh
`

# Activer le service
`
sudo cp service/oscshutdown.service /etc/systemd/system/oscshutdown.service
sudo systemctl enable oscshutdown.service
sudo reboot
`




