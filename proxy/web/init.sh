#!/usr/bin/env bash
# Copyright 2017-2022 Univertity of Bristol - High Performance Networks Group
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

GUNICORN=$(which gunicorn 2> /dev/null)
PIDFILE="/tmp/awproxy.pid"

start() {
    echo -ne "Starting Agnostic Wireless Proxy..."
    if [ -x $GUNICORN ]
    then
        $GUNICORN -D -w 1 -p $PIDFILE -b 0.0.0.0:8008 app_web:app
        echo -ne "..." && sleep 1 && echo -ne "  OK\n"
    else
        echo -ne "..." && sleep 1 && echo -ne "  FAIL (Gunicorn not found!)\n"
    fi
}

stop() {
    echo -ne "Stopping Agnostic Wireless Proxy..."
    if [ -f $PIDFILE ]
    then
        kill $(cat $PIDFILE)
        echo -ne "..." && sleep 1 && echo -ne "  OK\n"
    else
        echo -ne "..." && sleep 1 && echo -ne "  PIDFILE not found!\n"
    fi
}

restart(){
    stop
    start
}

status(){
    echo -ne "Agnostic Wireless Proxy..."
    if [ -f $PIDFILE ]
    then
        echo -ne "..." && sleep 1 && echo -ne "  RUNNING\n"
    else
        echo -ne "..." && sleep 1 && echo -ne "  NOT RUNNING\n"
    fi
}

case "$1" in
    start)
        start
        RETVAL=$?
        ;;
    stop)
        stop
        RETVAL=$?
        ;;
    restart)
        restart
        RETVAL=$?
        ;;
    status)
        status
        RETVAL=$?
        ;;
    *)
        echo $"Usage: $0 {start|stop|status|restart}"
        RETVAL=2
esac
