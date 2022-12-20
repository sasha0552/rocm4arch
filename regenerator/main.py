#!/usr/bin/env python3

from yaml import dump

from template.job import job_template
from template.action import action_template

from util.config import Config
from util.package.manager import PackageManager

#####

def obfuscate_packages(packages, names):
    for package in packages:
        dependencies = package["depends"]

        #####

        list = []

        #####

        for dependency in dependencies:
            if dependency in names:
                list.append(names[dependency])
            else:
                list.append(dependency)

        #####

        package["depends"] = set(list)

    #####

    return packages

#####

if __name__ == "__main__":
    config = Config("config.yml")

    #####

    packageManager = PackageManager(config)

    #####

    packages = packageManager.resolve_all_normalized(config.get_input())

    #####

    names = {}

    for index, package in enumerate(packages):
        names[package["name"]] = "_{}".format(index)

    #####

    packages = obfuscate_packages(packages, names)

    #####

    jobs = {}

    for package in packages:
        name = package["name"]
        path = package["path"]
        depends = list(package["depends"])

        jobs[names[name]] = job_template(name, path, sorted(depends), config.runs_on(name))

    #####

    action = action_template(jobs)

    #####

    with open(config.get_output(), "w") as file:
        file.write(dump(action))
