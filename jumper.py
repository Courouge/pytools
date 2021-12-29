# pip install paramiko
#Load ssh keys in your local ssh-agent
import paramiko

def jumper(ip_bastion, user_bastion, port_bastion = 22,
           ip_destination, user_destination = "root", port_destination = 22, cmd):

    # connexion to bastion
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_key()
    ssh.connect(hostname=ip_bastion, username=user_bastion)
    
    #connection to target
    target = paramiko.SSHClient()
    target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    target.load_system_host_key()
    target.connect(hostname=ip_destination, username=user_destination, sock=ssh.get_transport().open_channel("direct-tcpip", (ip_destination, port_bastion), (ip_bastion, port_destination)))
    stdin, stdout, stderr = target.exec_command(cmd)
    lines  = stdout.readlines()
    target.close()
    ssh.close()
    return lines

#How to use it ?
result_cmd = jumper('x.x.x.x', "bastion_user", 22, 'x.x.x.x', "root", 22, "ls /")
# or
result_cmd = jumper('x.x.x.x', "bastion_user", 'x.x.x.x', "ls /")

print(result_cmd)
# ['bin\n', "\boot\n","dev\n, "etc\n", "lib\n"]
# for path in result_cmd:
#   print(path[:-2])
