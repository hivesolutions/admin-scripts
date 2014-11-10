#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Administration Scripts
# Copyright (c) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Administration Scripts.
#
# Hive Administration Scripts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Administration Scripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Administration Scripts. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import getopt

import xml.dom.minidom

import legacy

import admin_scripts.extra as extra

USAGE_MESSAGE="pydev [-r] [-w exclusion_1, exclusion_2, ...] [-c configuration_file]"
""" The usage message to be printed in case there's an
error with the command line or help is requested. """

def pydev_file(file_path):
    """
    Runs the pydev configuration file normalization that consists
    in the definition in order of each of the xml lines.

    This operation should fail with an exception in case the
    structure of the xml document is not the expected one.

    @type file_path: String
    @param file_path: The path to the file that contains the
    pydev configuration specification in xml.
    """

    xmldoc = xml.dom.minidom.parse(file_path)
    xmldoc.getElementsByTagName("item")

def pydev_walker(arguments, directory_name, names):
    """
    Walker method to be used by the path walker for running the
    normalization pydev process.

    @type arguments: Tuple
    @param arguments: The arguments tuple sent by the walker method.
    @type directory_name: String
    @param directory_name: The name of the current directory in the walk.
    @type names: List
    @param names: The list of names in the current directory.
    """

    # unpacks the arguments tuple
    file_exclusion, = arguments

    # removes the complete set of names that are meant to be excluded from the
    # current set names to be visit (avoid visiting them)
    for exclusion in file_exclusion:
        if not exclusion in names: continue
        names.remove(exclusion)

    # retrieves the valid names for the names list (removes directory entries)
    valid_complete_names = [directory_name + "/" + name for name in names
        if not os.path.isdir(directory_name + "/" + name)]

    # filters the names with non valid file extensions so that only the
    # ones that conform with the pydev project ones are selected
    valid_complete_names = [os.path.normpath(name) for name in valid_complete_names
        if name == ".pydevproject"]

    # iterates over all the valid complete names with valid structure
    # as defined by the pydev project specification
    for valid_complete_name in valid_complete_names:
        # print a message a message about the pydev
        # operation that is going to be performed and
        # then runs the operation with the correct path
        print("Normalizing pydev configuration file: %s" % valid_complete_name)
        pydev_file(valid_complete_name)

def pydev_recursive(directory_path, file_exclusion):
    """
    Normalizes pydev in recursive mode.
    All the options are arguments to be passed to the
    walker function.

    @type directory_path: String
    @param directory_path: The path to the (entry point) directory.
    @type file_exclusion: List
    @param file_exclusion: The list of file exclusion to be used.
    """

    legacy.walk(directory_path, pydev_walker, (file_exclusion,))

def main():
    """
    Main function used for the pydev file normalization.
    """

    # in case the number of arguments
    # is not sufficient
    if len(sys.argv) < 2:
        # prints a series of message related with he
        # correct usage of the command line and then
        # exits the process with error indication
        print("Invalid number of arguments")
        print("Usage: " + USAGE_MESSAGE)
        sys.exit(2)

    # sets the default values for the parameters
    # this values are going to be used as the basis
    # for the generation of the configuration
    path = sys.argv[1]
    recursive = False
    file_exclusion = None
    configuration_file_path = None

    try:
        options, _arguments = getopt.getopt(sys.argv[2:], "rc:", [])
    except getopt.GetoptError:
        # prints a series of messages about the
        # correct usage of the command line and
        # exits the current process with an error
        print("Invalid number of arguments")
        print("Usage: " + USAGE_MESSAGE)
        sys.exit(2)

    # iterates over all the options, retrieving the option
    # and the value for each
    for option, value in options:
        if option == "-r":
            recursive = True
        elif option == "-w":
            file_exclusion = [value.strip() for value in value.split(",")]
        elif option == "-c":
            configuration_file_path = value

    # retrieves the configurations from the command line arguments
    # either from the command line or configuration file
    configurations = extra.configuration(
        file_path = configuration_file_path,
        recursive = recursive,
        file_exclusion = file_exclusion
    )

    # iterates over all the configurations, executing them
    for configuration in configurations:
        # retrieves the configuration values
        recursive = configuration["recursive"]
        file_exclusion = configuration["file_exclusion"]

        # in case the recursive flag is set, normalizes the multiple
        # found pydev configuration file
        if recursive: pydev_recursive(path, file_exclusion)
        # otherwise it's a "normal" iteration and runs the
        # pydev normalization process in it
        else: pydev_file(path)

if __name__ == "__main__":
    main()
