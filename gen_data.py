#!/usr/bin/env python3

import json
import argparse
import string
import random
import csv
import multiprocessing as mp
import os


def rand_from_file(fname):
    with open(fname, 'r') as readfile:
        csvreader = csv.reader(readfile)
        elements = []
        for row in csvreader:
            elements.extend(row)
        return elements.copy()


def read_pattern(pfile):
    try:
        with open(pfile, 'r') as conf_file:
            json_sch = json.load(conf_file)
            res_dict = {}
            for k, v in json_sch.items():
                if v.strip().startswith('randstr'):
                    res_dict[k] = (0, tuple())
                elif v.strip().startswith('randint'):
                    if v.strip() == 'randint':
                        res_dict[k] = (1, tuple())
                    else:
                        ar = eval(v.strip()[7:])
                        if isinstance(ar, tuple):
                            if len(ar) == 2:
                                res_dict[k] = (2, ar)
                            else:
                                print(f'Invalid format of config file {pfile}: cannot read string "{k}": "{v}"')
                                exit(1)
                        elif isinstance(ar, int):
                            res_dict[k] = (3, ar)
                        else:
                            print(f'Invalid format of config file {pfile}: cannot read string "{k}": "{v}"')
                            exit(1)
                elif v.strip().startswith('serial'):
                    res_dict[k] = (4, 0)
                else:
                    res_dict[k] = rand_from_file(v)
            return res_dict
    except json.JSONDecodeError:
        print(f'Config file you provided ({pfile}) not in json format')
        exit(1)


def generate_strings(pattern, cnt, fname, min_id):
    def generate_randint(a=0, b=0x7FFFFFFFFFFFFFFF, size=0):
        if size < 1:
            return random.randint(a, b)
        else:
            size = int(size)
            return random.randint(10 ** (size - 1), 10 ** size - 1)

    def generate_randstr():
        return ''.join(random.choices(string.ascii_letters, k=random.randint(2, 10)))

    with open(f"{fname}_{os.getpid()}.csv", 'w') as outfile:
        writer = csv.writer(outfile)
        for cur_id in range(cnt):
            line = []
            for val in pattern.values():
                if isinstance(val[0], int):
                    if 1 <= val[0] <= 3:
                        chis = -1
                        if val[0] == 1:
                            chis = generate_randint()
                        elif val[0] == 2:
                            chis = generate_randint(a=val[1][0], b=val[1][1])
                        elif val[0] == 3:
                            chis = generate_randint(size=val[1])
                        line.append(chis)
                    elif not val[0]:
                        line.append(generate_randstr())
                    elif val[0] == 4:
                        line.append(min_id + cur_id)
                else:
                    line.append(random.choice(val))
            writer.writerow(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script generating data')
    parser.add_argument('-c', '--config', type=str, required=True, help='path to config file (.json)')
    parser.add_argument('-n', '--name', type=str, default='file', help='filename of generated file (without .csv)')
    parser.add_argument('-m', '--num-rows', type=int, required=True, help='number of rows to generate')
    parser.add_argument('-p', '--num-processes', type=int, required=True, help='number of generator processes')
    args = parser.parse_args()

    pattern = read_pattern(args.config)
    # print(pattern)
    n_thr = args.num_processes
    strs_togen = [int(args.num_rows / n_thr) for _ in range(n_thr - 1)]
    strs_togen.append(args.num_rows - sum(strs_togen))
    min_id = [sum(strs_togen[:n]) for n in range(len(strs_togen))]
    with mp.Pool(processes=n_thr) as pool:
        multiple_results = [pool.apply_async(generate_strings, [pattern, strs_togen[idx], args.name, min_id[idx]])
                            for idx in range(len(strs_togen))]
        for result in multiple_results:
            result.get()
