#!/usr/bin/env python

import os
import sys
import time
import random
import string
import subprocess



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def checkRoot():
    if os.getuid() != 0:
        print(bcolors.FAIL+"[-] Must be run as root.\n"+bcolors.ENDC)
        sys.exit(0)
    return 0


def installPackages(apt):

    # List of dependencies.
    packages = [
        "libncap-dev",          # Required
        "tcpdump",              # Not required but recommended.
        "python-gnuplot",       # Recommended
        "python-crypto"         # Recommended
    ];

    for package in packages:
        try:

            subprocess.check_output(
                [
                    apt, "install", package, "-y"
                ],
                    stderr=subprocess.STDOUT
            );

            sys.stdout.write(bcolors.OKGREEN+"[+] Installed: "+package+bcolors.ENDC+"\n");

        except subprocess.CalledProcessError as e:

            sys.stderr.write(bcolors.WARNING+"[-] Failed to install Package: \n" + item + bcolors.ENDC);
            sys.stderr.write("\t - Reason: \n"+str(e.output));

    return 0;


def createCustomCommand():

    links = [
        "/usr/local/bin/boopsniff",
        "/usr/local/bin/boopsniff_gui",
        "/usr/local/bin/boop",
        "/usr/local/bin/boopstrike"
    ];

    new_links = [
        "/usr/share/Packet-Sniffer/boopsniff.py",
        "/usr/share/Packet-Sniffer/boopsniff_gui.py",
        "/usr/share/Monitor/boop.py",
        "/usr/share/Deauth/boopstrike.py"
    ];

    dirs = [
        "/usr/share/Packet-Sniffer/",
        "/usr/share/Monitor/",
        "/usr/share/Deauth"
    ];

    for dire in dirs:
        if os.path.isdir(dire):
            os.system("rm -rf " + dire)
            sys.stdout.write(bcolors.OKGREEN+"[+] Removed Old Project Directory\n"+bcolors.ENDC)

    try:

        subprocess.check_output(
            [
                "cp", "-r", "Packet-Sniffer/", "/usr/share/"
            ],
                stderr=subprocess.STDOUT
        );

        subprocess.check_output(
            [
                "cp", "-r", "Monitor/", "/usr/share/"
            ],
                stderr=subprocess.STDOUT
        );

        subprocess.check_output(
            [
                "cp", "-r", "Deauth/", "/usr/share/"
            ],
                stderr=subprocess.STDOUT
        );

        sys.stdout.write(bcolors.OKGREEN+"[+] Installed Tools to: /usr/share/\n"+bcolors.ENDC)

    except subprocess.CalledProcessError as e:

        sys.stderr.write(e.output);

    for link in links:

        if os.path.islink(link):

            os.system("rm -f " + link)
            sys.stdout.write(bcolors.OKGREEN+"[+] Removed an old command\n"+bcolors.ENDC)

    for index, value in enumerate(new_links):

        try:

            subprocess.check_output(
                [
                    "ln", "-s", new_links[index], links[index]
                ],
                    stderr=subprocess.STDOUT
            );

            subprocess.check_output(
                [
                    "chmod", "755", links[index]
                ],
                    stderr=subprocess.STDOUT
            );

            sys.stdout.write(bcolors.OKGREEN+"[+] Created New Command\n"+bcolors.ENDC);

        except subprocess.CalledProcessError as e:

            sys.stderr.write(bcolors.FAIL+"[-] Failed During custom command creation.\n");
            sys.stderr.write("\t - Reason: " + str(e.output)+"\n");


    return 0


# Display a welcome message to installer.
def welcomeText():

    print(
    """
    {0}Thanks for installing.
    
    For suggestions or more info on the tool(s),
    contact me @ jayrad.security@protonmail.com.
    {1}""".format(bcolors.OKBLUE, bcolors.ENDC)
    );

    return 0;


def main():

    # Check for proper permissions.
    checkRoot();

    # Install proper packages.
    installPackages("apt-get");

    # Create custom commands for the tools.
    createCustomCommand()

    return 0;


if __name__ == "__main__":
    main()
