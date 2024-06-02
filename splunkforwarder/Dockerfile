FROM balenalib/raspberrypi3
ARG SPKPASS
ADD splunkforwarder-8.1.6-c1a0dd183ee5-Linux-arm.tgz /opt/
COPY splunk-configs/outputs.conf /opt/splunkforwarder/etc/system/local
COPY splunk-configs/inputs.conf /opt/splunkforwarder/etc/system/local
COPY splunk-configs/test.txt /tmp/test.txt
RUN /opt/splunkforwarder/bin/splunk start --accept-license --answer-yes --no-prompt --seed-passwd "$SPKPASS"
RUN /opt/splunkforwarder/bin/splunk enable boot-start
ENTRYPOINT service splunk start && tail -F /dev/null 
