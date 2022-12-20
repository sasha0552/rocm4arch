import srcinfo.parse as srcinfo

#####

class PackageManager:
    def __init__(self, config):
        self._config = config

    ##########

    def _parse_package_info(self, file_path, info):
        name = file_path.parents[0].name
        path = str(file_path.parents[0])
        depends = set()
        altnames = set()

        #####

        if "depends" in info:
            depends.update(info["depends"])

        if "makedepends" in info:
            depends.update(info["makedepends"])

        #####

        if "provides" in info:
            altnames.update(info["provides"])

        #####

        for key, value in info["packages"].items():
            if key != name:
                altnames.add(key)

            #####

            if "depends" in value:
                depends.update(value["depends"])

            if "makedepends" in value:
                depends.update(value["makedepends"])

            #####

            if "provides" in value:
                altnames.update(value["provides"])

        #####

        return {
            "name": name,
            "path": path,
            "depends": depends,
            "_altnames": altnames
        }

    #####

    def _replace_altnames(self, packages):
        real_names = {}

        #####

        for package in packages:
            name = package["name"]
            altnames = package["_altnames"]

            #####

            for altname in altnames:
                real_names[altname] = name

            #####

            del package["_altnames"]

        #####

        for package in packages:
            dependencies = package["depends"]

            #####

            list = []

            #####

            for dependency in dependencies:
                if dependency in real_names:
                    list.append(real_names[dependency])
                else:
                    list.append(dependency)

            #####

            package["depends"] = set(list)

        #####

        return packages

    #####

    def _remove_missing_dependencies(self, packages):
        package_names = set()

        #####

        for package in packages:
            package_names.add(package["name"])

        #####

        for package in packages:
            dependencies = package["depends"]

            #####

            def validDependency(dependency):
                return dependency in package_names

            #####

            dependencies = filter(validDependency, dependencies)

            #####

            package["depends"] = set(dependencies)

        #####

        return packages

    #####

    def normalize_dependencies(self, packages):
        return self._remove_missing_dependencies(
            self._replace_altnames(
                packages
            )
        )

    #####

    def resolve(self, path):
        with open(path, "r") as file:
            content = file.read()

        #####

        (info, errors) = srcinfo.parse_srcinfo(content)

        #####

        if len(errors) != 0:
            return None

        #####
        
        packageInfo = self._parse_package_info(path, info)

        #####

        if not self._config.is_build(packageInfo["name"]):
            return None

        #####

        return packageInfo

    #####

    def resolve_all(self, path):
        pathes = path.rglob(".SRCINFO")

        #####

        packages = []

        #####

        for path in pathes:
            package = self.resolve(path)

            #####

            if package is None:
                continue

            #####

            packages.append(
                package
            )

        #####

        return packages

    #####

    def resolve_all_normalized(self, path):
        return self.normalize_dependencies(
            self.resolve_all(path)
        )
