import os


def output(msg):
    with open('debug.log','a') as log:
        log.write(f"{msg}\n")
    