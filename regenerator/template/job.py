def job_template(name, path, needs, runs_on, timeout):
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
                "name": "Download artifacts",
                "uses": "actions/download-artifact@v3",

                "with": {
                    "path": "~/artifacts/"
                }
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
                "name": "Create local package repository",
                "uses": "sasha0552/rocm4arch/actions/system-localrepo@master"
            },

            {
                "name": "Install package repositories",
                "uses": "sasha0552/rocm4arch/actions/system-repositories@master"
            },

            {
                "name": "Create users",
                "uses": "sasha0552/rocm4arch/actions/system-users@master"
            },

            {
                "name": "Checkout repository",
                "uses": "actions/checkout@v3",

                "with": {
                    "submodules": True
                }
            },

            {
                "name": "Receive GPG keys",
                "uses": "sasha0552/rocm4arch/actions/package-gpg@master"
            },

            {
                "name": "Build package",
                "uses": "sasha0552/rocm4arch/actions/package-build@master",

                "with": {
                    "package_path": path
                }
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
