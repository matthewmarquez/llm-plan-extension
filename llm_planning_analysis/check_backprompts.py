import json
import os 
import random

import yaml
from Executor import Executor
from utils import *
from pathlib import Path
from tarski.io import PDDLReader
import argparse
import time





# Get plan and corresponding verification by LLM
# Translate to PDDL
# Verify with VAL
# Compare to LLM verification

def get_intermediate_plans(llm_response, actions, domain, cur_instance, gpt3_plan_file, config, ground_flag=True):
    """
    Gets intermediate plans and corresponding verification by LLM and VAL for an instance
    """
    intermediate_dict = {
        'llm_correct': [],
        'val_correct': []
    }
    for ind, msg in enumerate(llm_response):
        if msg['role'] == 'assistant' and ind!=len(llm_response)-1:
            intermediate_resp = msg['content']
            text_to_plan(intermediate_resp, actions, gpt3_plan_file, config, ground_flag)
            val_correct = int(validate_plan(domain, cur_instance, gpt3_plan_file))
            intermediate_dict['val_correct'].append(val_correct)
        elif msg['role'] == 'user':

            if msg['content'].startswith('Plan is valid'):
                llm_correct = 1
            elif msg['content'].startswith('Plan is invalid'):
                llm_correct = 0
            else:
                continue
            intermediate_dict['llm_correct'].append(llm_correct)
    assert len(intermediate_dict['llm_correct']) == len(intermediate_dict['val_correct'])
    return intermediate_dict

def get_problem(instance, domain):
        reader = PDDLReader(raise_on_error=True)
        reader.parse_domain(domain)
        return reader.parse_instance(instance)

def main():
    file_name = 'json/task_1_plan_generation_backprompting_llm_feedback_zero_shot.json'

    with open(file_name, 'r') as f:
        data = json.load(f)
    count = 0
    avg_per_instance = {
        'TP': 0,
        'FP': 0,
        'TN': 0,
        'FN': 0
    }
    for instance in data['instances']:
        if count==100:
            break
        if instance["steps"]==1:
            continue
        count+=1
        instance_id = instance['instance_id']
        config_file = f'configs/{data["domain"]}.yaml'
        with open(config_file, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        gpt3_plan_file = 'sas_gpt3'
        instance_dir = config['instance_dir']
        instance_template = f'./instances/{instance_dir}/{config["instances_template"]}'
        cur_instance = instance_template.format(instance_id)
        domain_pddl = f'./instances/{config["domain_file"]}'
        problem = get_problem(cur_instance, domain_pddl)
        inter_dict = get_intermediate_plans(instance['messages'], data['actions'], domain_pddl, problem, gpt3_plan_file, config)
        #Caluclate TN, FN        
        act_correct = instance['act_correct']

        """
        If a correct instance has >50% TNs in inter_dict then it received helpful feedback

        If a wrong instance has >50% FNs in inter_dict then it received misleading feedback

        We will calculate and report the number of instances that received helpful/misleading feedback as a whole
        """


        #CHECK FOR HELPFUL/MISLEADING FEEDBACK
        if act_correct==1:
            #Percentage of True Negatives in inter_dict
            pass
        elif act_correct==0:
            #Percentage of False Negatives in inter_dict
            pass

