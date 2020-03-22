if [ "$(ping -c 5 8.8.8.8 | grep '0% packet loss' )" != "" ];
then
    echo "Internet is present"
else
    echo "Internet is not present"
    exit 1
fi
