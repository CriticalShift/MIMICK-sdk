#!/bin/sh
# runbook_metadata_start
# name: HWI v2 board test
# description: Powers, identifies, flashes and boots an HWI v2 under OpenHTF.
# image: <your registry>/hwi-v2-test:latest
# input: HWI_POWER_RELAY:string=relay0#Relay peripheral that powers the board
# input: HWI_POWER_CHANNEL:integer=1#Relay channel
# input: HWI_CONSOLE:string=uart0#UART peripheral on the board's console
# runbook_metadata_end
set -e
cd /opt/hwi
exec python hwi_test.py
