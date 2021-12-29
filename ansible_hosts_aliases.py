#############################################################################################################################################################
# this script is usefull if you have many platform, envs, ips and you don't want to speed time to check ip on your favorite IDE to connect on host.

# Inventories_Folder
# |- client1
# |--- techno1.ini
# |--- techno2.ini
# |- client2
# |--- techno1.ini
# |--- techno2.ini
# |--- techno3.ini
# |- client3
# |--- techno1.ini
# |- client4
# |--- techno1.ini

# ssh to client3 on host1 machine ?
# client1.techno1.host1
# autocompletion will help when browsing in multi techno context :)

#############################################################################################################################################################
####################################### python invs_alias.py /home/dev/workspace/inventories-projet ~/.bash_aliases  ########################################
#############################################################################################################################################################



import sys
import os
import json
from ansible.parsing.dataloader import DataLoader
try:
    from ansible.inventory.manager import InventoryManager
    A24 = True
except ImportError:
    from ansible.vars import VariableManager
    from ansible.inventory import Inventory
    A24 = False

inventory_project_dir = sys.argv[1] # ~/.bash_aliases

filename = sys.argv[2] # /home/dev/.bash_aliases
inv_list = []
inv_short_list = []
for r, d, f in os.walk(inventory_project_dir):
    for file in f:
        if ".ini" in file:
            if not "local" in '/'.join(os.path.join(r, file).split('/')[-2:]):
                inv_list.append(inventory_project_dir + '/' + '/'.join(os.path.join(r, file).split('/')[-2:]))
                inv_short_list.append('/'.join(os.path.join(r, file).split('/')[-2:])[:-4].replace("/","."))
loading = "[*]"
out_write_to_file = []
for inv, inv_short in zip(inv_list, inv_short_list):
    print(loading)
    loading = loading[:-1] + "*]"
    loader = DataLoader()
    if A24:
        inventory = InventoryManager(loader, [inv])
        inventory.parse_sources()
    else:
        variable_manager = VariableManager()
        inventory = Inventory(loader, variable_manager, inv)
        inventory.parse_inventory(inventory.host_list)

    out = {'_meta': {'hostvars': {}}}

    for host in inventory.get_hosts():
        out['_meta']['hostvars'][host.name] = host.vars

    for host in inventory.get_hosts():
        if out['_meta']['hostvars'][host.name].get("ansible_host") is not None:
            with open(filename, "a+") as myfile:
                out_write_to_file = "alias "+ inv_short + "." + str(host) + "='ssh " + str(out['_meta']['hostvars'][host.name].get("ansible_host")) + "'\n"
                # alias client1.techno1.host1 = 'ssh x.x.x.x'
                myfile.write(out_write_to_file)
                

