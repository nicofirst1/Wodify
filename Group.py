import os

from Job import load_json_job
from utils import dump_json_job, load_json, dump_json_group


class Group:

    def __init__(self, name, job_paths):

        self.name=name
        self.job_paths=job_paths
        self.jobs=[load_json_job(j) for j in job_paths]


    def save(self):
        """
        Save group with path to all jobs
        :return:
        """



        to_save=dict(
            name=self.name,
            jobs=self.job_paths
        )

        dump_json_group(to_save)

    def start(self):
        """
        Run every job in the group
        :return:
        """

        for j in self.jobs:
            j.start()



def load_json_group(group_path):
    group = load_json(group_path)
    return Group(group['name'], group['jobs'])

