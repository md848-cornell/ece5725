#Stop the background process
sudo /etc/init.d/bluetooth stop
# Turn on Bluetooth
sudo hciconfig hcio up
# Update  mac address
#./updateMac.sh
#Update Name
#./updateName.sh RPi_Mouse
#Get current Path
export C_PATH=$(pwd)
#Create Tmux session
tmux has-session -t  mlabviet
if [ $? != 0 ]; then

    echo "starting tmux commands"
    tmux new-session -s mlabviet -n os -d
    tmux split-window -v -t mlabviet:os.0
    tmux split-window -v -t mlabviet:os.1
    tmux send-keys -t mlabviet:os.0 'cd $C_PATH && sudo /usr/sbin/bluetoothd --nodetach --debug -p time ' C-m
    tmux send-keys -t mlabviet:os.1 'cd $C_PATH/server && sudo python btk_mouse.py ' C-m
    tmux send-keys -t mlabviet:os.2 'cd $C_PATH && sudo /usr/bin/bluetoothctl' C-m
    echo "tmux done"
fi
