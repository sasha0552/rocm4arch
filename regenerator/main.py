#!/usr/bin/env python3

from yaml import add_representer, dump
from hashlib import sha1

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

def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

#####

if __name__ == "__main__":
    add_representer(str, str_presenter)

    #####

    config = Config("config.yml")

    #####

    packageManager = PackageManager(config)

    #####

    packages = packageManager.resolve_all_normalized(config.get_input())

    #####

    names = {}

    for package in packages:
        names[package["name"]] = "_{}".format(sha1(package["name"].encode()).hexdigest())

    #####

    packages = obfuscate_packages(packages, names)

    #####

    jobs = {}

    for package in packages:
        name = package["name"]
        path = package["path"]
        depends = sorted(list(package["depends"]))

        #####

        runs_on = config.runs_on(name)
        timeout = config.timeout(name)
        pre_build_commands = config.pre_build_commands(name)
        post_build_commands = config.post_build_commands(name)
        gpg_keys = config.gpg_keys(name)

        #####

        for key in gpg_keys:
            pre_build_commands.insert(0,
                "su user --command {}".format(
                    "gpg --recv-keys {}".format(
                        key
                    )
                )
            )

        #####

        if len(pre_build_commands) != 0:
            pre_build_commands.insert(0, "cd {}".format(path))
        else:
            pre_build_commands.insert(0, "echo \"no pre-build commands\"")

        if len(post_build_commands) != 0:
            post_build_commands.insert(0, "cd {}".format(path))
        else:
            post_build_commands.insert(0, "echo \"no post-build commands\"")

        #####

        pre_build_commands = "\n".join(pre_build_commands)
        post_build_commands = "\n".join(post_build_commands)

        #####

        jobs[names[name]] = job_template(name, path, depends, runs_on, timeout, pre_build_commands, post_build_commands)

    #####

    action = action_template(jobs)

    #####

    with open(config.get_output(), "w") as file:
        file.write(dump(action))
