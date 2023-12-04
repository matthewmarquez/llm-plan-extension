import json
import argparse

def get_steps(file, limit):
    '''
    Assumes file does not give instance id of -1 to any instance. If limit is set to -1, no limit will be used.
    Note that limit refers to the instance id of the last instance you want included in the order instances are presented.
    If instance ids do not match order, limit will stop analysis when it sees an instance with a given id and not
    after limit instances have passed. For example if the order is [1, 51, 2, ..., 49, 50] and the limit is 51, only
    two instances will be included (1 and 51) because analysis will stop when the second instance is processed. We will not
    compute 51 instnaces in this case. It is recommended to have instances ordered by instance id to avoid issues
    like this.
    '''
    with open(file, "r+") as f:
        results = json.load(f)

    steps = []

    for result in results["instances"]:
        steps.append(result["steps"])

        if limit != -1 and result["instance_id"] == limit:
            break

    return float(sum(steps))/float(len(steps))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='File Name')
    parser.add_argument('--limit', type=int, default=-1, help='Limit on instances to include')
    args = parser.parse_args()
    file = args.file
    limit = args.limit
    print(get_steps(file, limit))