# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

# Adds the Deadline Cloud Install Path to Blender's Script directory list.
# Then enables the submitters plugin.

import bpy
import addon_utils
import argparse
import sys


class ArgumentParserForBlender(argparse.ArgumentParser):
    def _get_argv_after_doubledash(self):
        try:
            return sys.argv[sys.argv.index("--") + 1 :]  # the list after '--'
        except ValueError:  # '--' not in the list:
            return []

    def parse_args(self):
        return super().parse_args(args=self._get_argv_after_doubledash())


def main():
    parser = ArgumentParserForBlender(description="Add Deadline Cloud to Blender preferences")
    parser.add_argument(
        "--deadline_cloud_install_path", required=True, help="Path to Deadline Cloud installation"
    )
    args = parser.parse_args()

    print(f"DEBUG: Install path: {args.deadline_cloud_install_path}")
    
    # Check if path exists
    import os
    if os.path.exists(args.deadline_cloud_install_path):
        print(f"DEBUG: Path exists, contents: {os.listdir(args.deadline_cloud_install_path)}")
    else:
        print(f"DEBUG: Path does not exist!")
        return

    # Check current script directories
    print(f"DEBUG: Current script directories: {bpy.context.preferences.filepaths.script_directories}")

    bpy.ops.preferences.script_directory_add(directory=args.deadline_cloud_install_path)
    
    print(f"DEBUG: Script directories after add: {bpy.context.preferences.filepaths.script_directories}")
    
    bpy.utils.load_scripts(refresh_scripts=True)

    # Check available addons
    available_addons = [addon.__name__ for addon in addon_utils.modules()]
    print(f"DEBUG: Available addons: {[a for a in available_addons if 'deadline' in a.lower()]}")

    try:
        result = addon_utils.enable("deadline_cloud_blender_submitter", default_set=True)
        print(f"DEBUG: Enable result: {result}")
    except Exception as e:
        print(f"DEBUG: Enable failed: {e}")

    bpy.ops.wm.save_userpref()


if __name__ == "__main__":
    main()
