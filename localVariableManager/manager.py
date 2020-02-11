# Build-In Modules
import os
import shutil
from shutil import copyfile
from pathlib import Path

# 3rd Party Modules
import clipboard

# Global Variables
TEMP_FOLDER = os.path.abspath('.lvm/')


def add(file_path, name):
    """
    Method to add file LVM

    :param String file_path: Path to file
    :param String name: Name of project
    :return: Flag to indicate if we are successful
    :rtype boolean:
    """
    absPathToFile = str(Path(file_path).absolute())

    # Check if our file exists
    if not os.path.isfile(file_path):
        print(f"[Error] File {file_path} does not exists!")
        return False

    # Check if we have the file extension
    if "." not in file_path:
        print(f"[Warning] No extension in file_path!")

    try:
        # Copy our file to our /lvm/ directory
        paths = name.split('/')
        index = TEMP_FOLDER
        if len(paths) > 1:
            for path in paths[:-1]:
                index += f"/{path}"
                if not os.path.isdir(index):
                    # Create directories if they don't exists
                    os.mkdir(index)
        copyfile(absPathToFile, TEMP_FOLDER + '/' + name + Path(file_path).suffix)
        return True
    except Exception as e:
        print(f"[Error] Exception: {e}")
        return False

def delete(name):
    """
    Delete a stored project/value

    :param String name: Name of project/file to be deleted
    :return: Flag to indicate if we are successful
    :rtype boolean:
    """
    absPathToVal = str(Path(f"{TEMP_FOLDER}/{name}").absolute())

    # Check if it is a dir/project
    if os.path.isdir(absPathToVal):
        if confirm(name):
            if confirm(name, really=True):
                # Delete the folder
                shutil.rmtree(absPathToVal)
                return True
        else:
            return False
    # Loop to get the file extension and then delete the value
    parent_folder = str(Path(f"{TEMP_FOLDER}/{name}").parent.absolute())
    name_split = name.split('/')
    for file in os.listdir(parent_folder):
        split_file = file.split(".")
        if split_file[0] in name_split:
            if confirm(f"{name} [AKA {file}]"):
                # We found the file, add its extension
                os.remove(absPathToVal + os.path.splitext(file)[1])
                return True
    else:
        return False

    # Always return false just in case we failed along the way
    return False

def confirm(name, really=False):
    """
    Helper function to deal with user confirming

    :param String name: Value we are deleting
    :param boolean really: Are you sure you want to delete this?
    :return: Flag to indicate if they confirmed
    :rtype: boolean
    """
    if not really:
        confirm = input(f"Are you sure you want to delete: {name}?\n"
                        f"Press Y to confirm:")
    else:
        confirm = input(f"Are you REALLY SURE you want to delete: {name}?\n"
                        f"Press Y to confirm:")
    if confirm == "Y":
        return True
    else:
        return False


def setenv(project_name, name_of_env):
    """
    Delete a stored project

    :param String project_name: Name of project/file to be used
    :param String name_of_env: Name of global variable to be used
    :return: Flag to indicate if we are successful
    :rtype boolean:
    """
    # Copy our file to .exposed
    absPathToVal = str(Path(f"{TEMP_FOLDER}/{project_name}").absolute())

    # Check if its a dir

    # if os.path.isdir(absPathToVal):
    # Connect the export's with a ;

    parent_folder = str(Path(absPathToVal).parent.absolute())
    for file in os.listdir(parent_folder):
        for possible_name in project_name.split('/'):
            if file.startswith(possible_name):
                index = ".exposed"
                for path in project_name.split("/")[:-1]:
                    index += f"/{path}"
                    if not os.path.isdir(index):
                        # Create directories if they don't exists
                        os.mkdir(index)
                copyfile(absPathToVal + Path(file).suffix, ".exposed/" + project_name + Path(file).suffix)
                break

    # Build our string to paste into clipboard
    clipboardString = f"export {name_of_env}=.exposed/{project_name}{Path(file).suffix}"
    clipboard.copy(clipboardString)
    return True

def ls():
    """
    List out projects/values we have stored

    :return: Flag to indicate if we are successful
    :rtype boolean:
    """
    list_files(TEMP_FOLDER)
    return True

def list_files(startpath):
    """
    Helper function to list files
    Taken from: https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python

    :param String startpath: Start of root we should display
    """
    skip_first = False
    for root, dirs, files in os.walk(startpath):
        if not skip_first:
            skip_first = True
            continue
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
            # TODO: If we are at the end, show the file name my.key [main/project/my]

def cleanup():
    """
    Delete .exposed/ dir

    :return: Flag to indicate if we are successful
    :rtype boolean:
    """
    shutil.rmtree(".exposed/")
    return True