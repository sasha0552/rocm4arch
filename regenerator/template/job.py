def job_template(name, path, needs, runs_on, timeout, pre_build_commands, post_build_commands):
    return {
        "name": name,
        "needs": needs,
        "runs-on": runs_on,
        "timeout-minutes": timeout,

        "container": {
            "image": "archlinux"
        },

        "steps": [
            {
                "name": "System cleanup",
                "uses": "sasha0552/rocm4arch/actions/system-cleanup@master"
            },

            {
                "name": "Upgrade system",
                "uses": "sasha0552/rocm4arch/actions/system-upgrade@master"
            },

            {
                "name": "Install required packages",
                "uses": "sasha0552/rocm4arch/actions/system-packages@master",

                "with": {
                    "additional": "base-devel"
                }
            },

            {
                "name": "Create users",
                "uses": "sasha0552/rocm4arch/actions/system-users@master"
            },

            {
                "name": "Download artifacts",
                "uses": "actions/download-artifact@v3",

                "with": {
                    "path": "~/artifacts/"
                }
            },

            {
                "name": "Configure makepkg",
                "uses": "sasha0552/rocm4arch/actions/system-makepkg@master"
            },

            {
                "name": "Create local package repository",
                "uses": "sasha0552/rocm4arch/actions/system-localrepo@master"
            },

            {
                "name": "Install package repositories",
                "uses": "sasha0552/rocm4arch/actions/system-repositories@master"
            },

            {
                "name": "Checkout repository",
                "uses": "actions/checkout@v3",

                "with": {
                    "submodules": True
                }
            },

            {
                "name": "Pre-build commands",
                "shell": "bash",
                "run": pre_build_commands
            },

            {
                "name": "Build package",
                "uses": "sasha0552/rocm4arch/actions/package-build@master",

                "with": {
                    "package_path": path
                }
            },

            {
                "name": "Post-build commands",
                "shell": "bash",
                "run": post_build_commands
            },

            {
                "name": "Upload artifacts",
                "uses": "actions/upload-artifact@v3",

                "with": {
                    "path": "packages/**/*.pkg.tar.zst"
                }
            }
        ]
    }
