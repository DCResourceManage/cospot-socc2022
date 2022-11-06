from collections import OrderedDict
import csv
from gurobipy import *
import json
import numpy as np

excluded_vms = [0, 1, 2, 3, 4, 14, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121]

def solve_cores(csv_fname):
    vm_flavours = OrderedDict()
    servers = OrderedDict()

    with open(csv_fname, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            vm_flavour = int(row[1])
            server = int(row[2])

            core_prop = float(row[3])
            ram_prop = float(row[4])

            if server not in servers:
                servers[server] = None

            if vm_flavour not in excluded_vms:
                if vm_flavour not in vm_flavours:
                    vm_flavours[vm_flavour] = [(server, core_prop, ram_prop)]
                else:
                    vm_flavours[vm_flavour].append((server, core_prop, ram_prop))

    gr_model = Model()
    gr_model.setParam('OutputFlag', False)
    gr_model.setParam('Threads', 1)

    vm_core_counts = gr_model.addVars(sorted(vm_flavours.keys()), lb=1, vtype=GRB.INTEGER, name="vm_cores")
    server_core_counts = gr_model.addVars(sorted(servers.keys()), lb=1, vtype=GRB.INTEGER, name="server_cores")

    for vm in vm_flavours:
        if vm in excluded_vms:
            continue
        for curr_tup in vm_flavours[vm]:
            gr_model.addConstr(vm_core_counts[vm] == curr_tup[1] * server_core_counts[curr_tup[0]])

    gr_model.setObjectiveN(quicksum(server_core_counts.values()), 0, priority=1)
    gr_model.setObjectiveN(quicksum(vm_core_counts.values()), 1, priority=0)
    gr_model.optimize()

    if gr_model.status == GRB.Status.OPTIMAL:
        server_results = dict(zip([x.VarName for x in server_core_counts.values()], gr_model.getAttr('x', server_core_counts.values())))
        vm_results = dict(zip([x.VarName for x in vm_core_counts.values()], gr_model.getAttr('x', vm_core_counts.values())))
        return vm_results, server_results

def solve_ram(csv_fname):
    vm_flavours = OrderedDict()
    servers = OrderedDict()

    with open(csv_fname, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            vm_flavour = int(row[1])
            server = int(row[2])

            core_prop = float(row[3])
            ram_prop = float(row[4])

            if server not in servers:
                servers[server] = None

            if vm_flavours not in excluded_vms:
                if vm_flavour not in vm_flavours:
                    vm_flavours[vm_flavour] = [(server, core_prop, ram_prop)]
                else:
                    vm_flavours[vm_flavour].append((server, core_prop, ram_prop))

    gr_model = Model()
    gr_model.setParam('OutputFlag', False)
    gr_model.setParam('Threads', 1)

    vm_ram_counts = gr_model.addVars(sorted(vm_flavours.keys()), lb=1, vtype=GRB.INTEGER, name="vm_ram")
    server_ram_counts = gr_model.addVars(sorted(servers.keys()), lb=1, vtype=GRB.INTEGER, name="server_ram")

    for vm in vm_flavours:
        if vm in excluded_vms:
            continue
        for curr_tup in vm_flavours[vm]:
            gr_model.addConstr(vm_ram_counts[vm] == curr_tup[2] * server_ram_counts[curr_tup[0]])

    gr_model.setObjectiveN(quicksum(server_ram_counts.values()), 0, priority=1)
    gr_model.setObjectiveN(quicksum(vm_ram_counts.values()), 1, priority=0)
    gr_model.optimize()

    if gr_model.status == GRB.Status.OPTIMAL:
        server_results = dict(zip([x.VarName for x in server_ram_counts.values()], gr_model.getAttr('x', server_ram_counts.values())))
        vm_results = dict(zip([x.VarName for x in vm_ram_counts.values()], gr_model.getAttr('x', vm_ram_counts.values())))
        return vm_results, server_results

# Call solve_ram, solve_cores with a CSV file in the form of vmType.csv 
vm_ram, server_ram = solve_ram('')
vm_cores, server_cores = solve_cores('')
with open('server-vm-cores-ram.json', 'w') as outfile:
    json.dump([vm_cores, server_cores, vm_ram, server_ram], outfile, ensure_ascii=False, indent=4)

