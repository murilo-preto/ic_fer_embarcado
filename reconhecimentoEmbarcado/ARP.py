import subprocess
import sys

serverMacAddress = "ff:ff:ff:ff:ff:ff"

print(f'Tentando obter IP do servidor via ARP, usando MacAddress:{serverMacAddress}.\n')
cmd = f'arp -a | findstr "{serverMacAddress.replace(":", "-")}" '
try:
    returned_output = subprocess.check_output(
        cmd, shell=True, stderr=subprocess.STDOUT)
    parse = str(returned_output).split(' ', 1)
    serverIp = (parse[1].split(' '))[1]
    print(f"Utilizando IP local do servidor: {serverIp}.")
except Exception as e:
    print(f"Não foi possível obter o endereço de IP do servidor.\nErro:{e}\n")
    sys.exit(1)
