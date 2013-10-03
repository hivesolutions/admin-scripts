#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Administration Scripts
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import getopt

USAGE_MESSAGE = "convert-encoding-python path [-r] [-s source_encoding] [-t target_encoding] [-u] [-x replacement_from_1, replacement_to_1, replacement_from_2, replacement_to_2, ...] [-e file_extension_1, file_extension_2, ...] [-c configuration_file]"
""" The usage message """

RELATIVE_BASE_PATH = "/.."
""" The relative base path """

LONG_PATH_PREFIX = u"\\\\?\\"
""" The windows long path prefix """

NT_PLATFORM_VALUE = "nt"
""" The nt platform value """

DOS_PLATFORM_VALUE = "dos"
""" The dos platform value """

WINDOWS_PLATFORMS_VALUE = (
    NT_PLATFORM_VALUE,
    DOS_PLATFORM_VALUE
)
""" The windows platform value """

RECURSIVE_VALUE = "recursive"
""" The recursive value """

SOURCE_ENCODING_VALUE = "source_encoding"
""" The source encoding value """

TARGET_ENCODING_VALUE = "target_encoding"
""" The target encoding value """

WINDOWS_NEWLINE_VALUE = "windows_newline"
""" The windows newline value """

REPLACEMENTS_LIST_VALUE = "replacements_list"
""" The replacements list value """

FILE_EXTENSIONS_VALUE = "file_extensions"
""" The file extensions value """

def normalize_path(path):
    """
    Normalizes the given path, using the characteristics
    of the current environment.
    In windows this function adds support for long path names.

    @type path: String
    @param path: The path to be normalized.
    @rtype: String
    @return: The normalized path.
    """

    # retrieves the current os name
    os_name = os.name

    # in case the current operative system is windows based and
    # the normalized path does start with the long path prefix it
    # must be removed to allow a "normal" path normalization
    if os_name in WINDOWS_PLATFORMS_VALUE and path.startswith(LONG_PATH_PREFIX):
        # removes the long path prefix from the path
        path = path[4:]

    # checks if the path is absolute
    is_absolute_path = os.path.isabs(path)

    # in case the path is not absolute (creates problem in windows
    # long path support)
    if os_name in WINDOWS_PLATFORMS_VALUE and not is_absolute_path:
        # converts the path to absolute
        path = os.path.abspath(path)

    # normalizes the path
    normalized_path = os.path.normpath(path)

    # in case the current operative system is windows based and
    # the normalized path does not start with the long path prefix
    if os_name in WINDOWS_PLATFORMS_VALUE and not normalized_path.startswith(LONG_PATH_PREFIX):
        # creates the path in the windows mode, adds
        # the support for long path names with the prefix token
        normalized_path = LONG_PATH_PREFIX + normalized_path

    # returns the normalized path
    return normalized_path

def has_encoding(string_buffer, encoding):
    """
    Determines if the provided buffer is encoded in the provided encoding.

    @type string_buffer: String
    @param string_buffer: The string buffer.
    @type encoding: String
    @param encoding: The encoding against which to test the string buffer.
    """

    # initializes the has encoding flag
    has_encoding = None

    try:
        # tries to decode the provided buffer, using the specified encoding
        string_buffer.decode(encoding)

        # in case the decode was success sets the has encoding flag
        has_encoding = True
    # in case a problem occurred decoding
    except:
        # sets the has encoding flag as false
        has_encoding = False

    # returns the has encoding flag
    return has_encoding

def apply_replacements_list(string_buffer, replacements_list):
    """
    Applies a list of replacements to the provided string buffer.

    @type string_buffer: String
    @param string_buffer: The string to which the replacements are to be applied to.
    @type replacements_list: List
    @param replacements_list: The list of replacements to apply.
    """

    # for each replacement to be performed
    for replacement in replacements_list:
        # unpacks the replacement tuple
        replacement_from, replacement_to = replacement

        # performs the replacements
        string_buffer = string_buffer.replace(replacement_from, replacement_to)

    # returns the replaced string buffer
    return string_buffer

def convert_encoding(file_path, source_encoding, target_encoding, windows_newline = True, replacements_list = None):
    """
    Converts the encoding of the specified file.

    @type file_path: String
    @param file_path: The path to the file to have its encoding converted.
    @type source_encoding: String
    @param source_encoding: The encoding from which the file is to be converted from.
    @type target_encoding: String
    @param target_encoding: The encoding to which the file is to be converted.
    @type windows_newline: bool
    @param windows_newline: If the windows newline should be used.
    @type replacements_list: List
    @param replacements_list: The list of replacements to perform.
    """

    # normalizes the file path and uses it as the path to
    # open the reference to it (in reading mode)
    file_path_normalized = normalize_path(file_path)
    file = open(file_path_normalized, "r")

    try:
        # reads the complete string contents from the file and
        # checks if the file already has the target encoding
        string_value = file.read()
        has_target_encoding = has_encoding(string_value, target_encoding)

        # decodes the string value from the specified source encoding, this
        # operation may fail as the source encoding may only be a guess on
        # the true encoding of the file, the encodes the string value again
        # in the target encoding for the file
        string_value_decoded = not has_target_encoding and\
            string_value.decode(source_encoding) or string_value
        string_value_encoded = not has_target_encoding and\
            string_value_decoded.encode(target_encoding) or string_value_decoded

        # applies the replacements
        string_value_encoded_replaced = replacements_list and\
            apply_replacements_list(string_value_encoded, replacements_list) or\
            string_value_encoded

        # applies the windows newline if specified
        string_value_encoded_replaced = windows_newline and\
            string_value_encoded_replaced.replace("\n", "\r\n") or\
            string_value_encoded_replaced
    finally:
        # closes the file for reading
        file.close()

    # opens the file for writing then writes the file string value
    # with the proper string values replaced and re-encoded into the
    # target character encoding (as expected)
    file = open(file_path_normalized, "wb")
    try: file.write(string_value_encoded_replaced)
    finally: file.close()

def convert_encoding_walker(arguments, directory_name, names):
    """
    Walker method to be used by the path walker for the encoding conversion.

    @type arguments: Tuple
    @param arguments: The arguments tuple sent by the walker method.
    @type directory_name: String
    @param directory_name: The name of the current directory in the walk.
    @type names: List
    @param names: The list of names in the current directory.
    """

    # unpacks the arguments tuple
    source_encoding, target_encoding, windows_newline, replacements_list, file_extensions = arguments

    # retrieves the valid names for the names list (removes directory entries)
    valid_complete_names = [directory_name + "/" + name
        for name in names if not os.path.isdir(directory_name + "/" + name)]

    # filters the names with non valid file extensions
    valid_complete_names_extensions = [name for name in valid_complete_names
        if file_extensions == None or name.split(".")[-1] in file_extensions]

    # iterates over all the valid complete names with extension filter
    # ot convert the respective file into the target encoding
    for valid_complete_name_extension in valid_complete_names_extensions:
        # prints a message about the file that is not going to be converted
        # into the proper target encoding as defined in the specification
        print "Convert encoding in file: %s (%s to %s)" %\
            (
                 valid_complete_name_extension,
                 source_encoding,
                 target_encoding
            )

        try:
            # converts the encoding for the provided (path) name according to
            # a set of defined options, for various reasons this operation may
            # fail if such thing happens the operation is skipped
            convert_encoding(
                valid_complete_name_extension,
                source_encoding,
                target_encoding,
                windows_newline,
                replacements_list
            )
        except:
            pass

def convert_encoding_recursive(directory_path, source_encoding, target_encoding, windows_newline, replacements_list = None, file_extensions = None):
    """
    Converts the file encoding in recursive mode.
    All the options are arguments to be passed to the
    walker function.

    @type directory_path: String
    @param directory_path: The path to the (entry point) directory.
    @type source_encoding: String
    @param source_encoding: The source encoding from which the file is to be
    converted.
    @type target_encoding: String
    @param target_encoding: The target encoding to which the file is to be
    converted to.
    @type replacements_list: List
    @param replacements_list: The list of replacements to perform.
    @type file_extensions: List
    @param file_extensions: The list of file extensions to be used.
    """

    os.path.walk(
        directory_path,
        convert_encoding_walker,
        (source_encoding, target_encoding, windows_newline, replacements_list, file_extensions)
    )

def _retrieve_configurations(recursive, source_encoding, target_encoding, windows_newline, replacements_list, file_extensions, configuration_file_path):
    """
    Retrieves the configuration maps for the given arguments.

    @type recursive: bool
    @param recursive: If the removing should be recursive.
    @type source_encoding: String
    @param source_encoding: The source encoding from which the file is to be
    converted.
    @type target_encoding: String
    @param target_encoding: The target encoding to which the file is to be
    converted to.
    @type replacements_list: List
    @param replacements_list: The list of replacements to perform.
    @type file_extensions: List
    @param file_extensions: The list of file extensions to be used.
    @type configuration_file_path: String
    @param configuration_file_path: The path to the configuration file.
    """

    # in case the configuration file path is defined
    if configuration_file_path:
        # creates the base path from the file paths
        base_path = os.path.dirname(os.path.realpath(__file__)) + RELATIVE_BASE_PATH

        # retrieves the real base path
        real_base_path = os.path.realpath(base_path)

        # retrieves the configuration directory from the configuration
        # file path (the directory is going to be used to include the module)
        configuration_directory_path = os.path.dirname(configuration_file_path)

        # in case the configuration directory path is not an absolute path
        if not os.path.isabs(configuration_directory_path):
            # creates the (complete) configuration directory path prepending the manager path
            configuration_directory_path = real_base_path + "/" + configuration_directory_path

        # in case the configuration directory path is valid inserts it into the system path
        configuration_directory_path and sys.path.insert(0, configuration_directory_path)

        # retrieves the configuration file base path from the configuration file path
        configuration_file_base_path = os.path.basename(configuration_file_path)

        # retrieves the configuration module name and the configuration module extension by splitting the
        # configuration base path into base name and extension
        configuration_module_name, _configuration_module_extension = os.path.splitext(configuration_file_base_path)

        # imports the configuration module
        configuration = __import__(configuration_module_name)

        # retrieves the configurations from the configuration module
        configurations = configuration.configurations
    else:
        # creates the base configuration map
        base_configuration = {}

        # sets the base configuration map attributes
        base_configuration[RECURSIVE_VALUE] = recursive
        base_configuration[SOURCE_ENCODING_VALUE] = source_encoding
        base_configuration[TARGET_ENCODING_VALUE] = target_encoding
        base_configuration[REPLACEMENTS_LIST_VALUE] = replacements_list
        base_configuration[FILE_EXTENSIONS_VALUE] = file_extensions

        # creates the configurations tuple with the base configurations
        configurations = (
            base_configuration,
        )

    # returns the configurations tuple
    return configurations

def main():
    """
    Main function used for the encoding conversion.
    """

    # in case the number of arguments
    # is not sufficient
    if len(sys.argv) < 2:
        # prints a message
        print "Invalid number of arguments"

        # prints the usage message
        print "Usage: " + USAGE_MESSAGE

        # exits the system in error
        sys.exit(2)

    # sets the default values for the parameters
    path = sys.argv[1]
    recursive = False
    source_encoding = None
    target_encoding = None
    windows_newline = None
    replacements_list = None
    file_extensions = None
    configuration_file_path = None

    try:
        options, _arguments = getopt.getopt(sys.argv[2:], "rs:t:x:e:c:", [])
    except getopt.GetoptError:
        # prints a message
        print "Invalid number of arguments"

        # prints the usage message
        print "Usage: " + USAGE_MESSAGE

        # exits the system in error
        sys.exit(2)

    # iterates over all the options, retrieving the option
    # and the value for each
    for option, value in options:
        if option == "-r":
            recursive = True
        elif option == "-s":
            source_encoding = value
        elif option == "-t":
            target_encoding = value
        elif option == "-u":
            windows_newline = value
        elif option == "-x":
            replacements_list = [value.strip() for value in value.split(",")]
        elif option == "-e":
            file_extensions = [value.strip() for value in value.split(",")]
        elif option == "-c":
            configuration_file_path = value

    # retrieves the configurations from the command line arguments
    configurations = _retrieve_configurations(
        recursive,
        source_encoding,
        target_encoding,
        windows_newline,
        replacements_list,
        file_extensions,
        configuration_file_path
    )

    # iterates over all the configurations, executing them
    for configuration in configurations:
        # retrieves the configuration values
        recursive = configuration[RECURSIVE_VALUE]
        source_encoding = configuration[SOURCE_ENCODING_VALUE]
        target_encoding = configuration[TARGET_ENCODING_VALUE]
        windows_newline = configuration[WINDOWS_NEWLINE_VALUE]
        replacements_list = configuration[REPLACEMENTS_LIST_VALUE]
        file_extensions = configuration[FILE_EXTENSIONS_VALUE]

        # in case the recursive flag is set must converts the files
        # using the recursive mode
        if recursive:
            convert_encoding_recursive(
                path,
                source_encoding,
                target_encoding,
                windows_newline,
                replacements_list,
                file_extensions
            )
        # otherwise it's a "normal" iteration, must converts the
        # encoding (for only one file)
        else:
            convert_encoding(
                path,
                source_encoding,
                target_encoding,
                windows_newline,
                replacements_list
            )

if __name__ == "__main__":
    main()
