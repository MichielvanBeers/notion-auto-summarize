#!/bin/sh

echo "Writing environment variables to /etc/environment"
printenv | grep -v "no_proxy" >> /etc/environment

if [ -z "$RUN_FREQUENCY" ] 
then
    echo "Running single instance of scan"
    python app.py
else
    echo "Found scan frequency variable, adding crontab"
    cat > output.log
    (crontab -l 2>/dev/null; echo "*/$RUN_FREQUENCY * * * * cd /app; /usr/local/bin/python3 ./app.py > output.log") | crontab -  

    echo "Scanning every $RUN_FREQUENCY minute(s)"
    service cron start && tail -f output.log
fi