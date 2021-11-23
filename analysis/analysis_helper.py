import os
import json
import tarfile
import glob

import numpy as np
import pandas as pd


def shell(command):
    return os.system(command)


def shell_without_print(command):
    return os.system(command + '>/dev/null 2>&1')


def shell_return(command):
    return os.popen(command).read().strip()


def load(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data


def git_annex(cpu_info, job_info, uuidgen_hash, base_path):

    tmp_result_file_path = os.path.join(base_path, uuidgen_hash + '.csv')
    result_file_path = os.path.join('./', uuidgen_hash + '.csv')
    archive_path = f'{uuidgen_hash}.tgz'

    ## tar gzip metadata archives, append uuids to results csv file

    metadata_archives = glob.glob(f"{base_path}/**/*.tgz", recursive=True)
    # sort metadata in same way as they are sorted in the csv
    metadata_archives.sort()
    # get metadata uuids from absolute paths
    metadata_uuids = [os.path.split(archive)[-1].split('.')[0]
                      for archive in metadata_archives]
    # tar metadata archives for each run
    tar_obj = tarfile.open(archive_path, "w")
    for archive in metadata_archives:
        tar_obj.add(archive,
                    arcname=os.path.join(
                        uuidgen_hash,
                        os.path.split(archive)[-1]))
    tar_obj.close()
    # add metadata uuid to corresponding csv entry
    csv = pd.read_csv(tmp_result_file_path)
    csv['metadata_uuid'] = metadata_uuids
    csv.to_csv(result_file_path)
    
    # works for machines with the naming scheme XXX.name (used for JSC
    # clusters, might need adjustment for other machines)
    machine = os.popen('echo $HOSTNAME').read().strip().split('.')[-1]
    user = os.popen('echo $USER').read().strip()

    shell(f'git annex add {result_file_path}')
    shell(f'git annex add {archive_path}')
    shell_without_print(
        f'git annex metadata {result_file_path} --set key={uuidgen_hash}')

    for info_dict in [job_info, cpu_info]:
        for key, value in info_dict.items():
            value_without_spaces = value.replace(' ', ';')
            shell_without_print(f'git annex metadata {result_file_path} '
                                + f'--set {key}="{value_without_spaces}" '
                                + '--force')
    # additionally add machine and user name
    shell_without_print(f'git annex metadata {result_file_path} '
                        + f'--set machine="{machine}" --force')
    shell_without_print(f'git annex metadata {result_file_path} '
                        + f'--set user="{user}" --force')

    averaged_over = len(
        np.unique(pd.read_csv(result_file_path)['rng_seed'].values))
    shell_without_print(f'git annex metadata {result_file_path} '
                        + f'--set averaged_over="{averaged_over}" --force')
