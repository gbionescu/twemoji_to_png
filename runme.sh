while true; do
    date
    ./twemoji2imgur.py;
    if [[ "$?" != 0 ]]; then
        echo "Sleeping for 10 minutes"
        sleep 600
    else
        echo "No exceptions raised. Exiting"
        exit 0
    fi
done
