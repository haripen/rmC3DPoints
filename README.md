# rmC3DPoints
Processes C3D files to remove specified markers, points, or labels.

Uses the ezc3d library to read and write C3D files and can be called from MATLAB or the command line.

## Features
 - Removes specified markers, points, labels, and all labels (with their data) with the prefix * from C3D files.
 - Updates label lists and data points in the C3D file.
 - Saves the patched C3D file with a new name ending with *_pached*.

## Usage
Make sure you have **ezc3d** and **numpy** installed.

Check the ``virtual_markers`` list if you need to remove others and add the additional ones to the list.

Edit the ``remove_also`` list if necessary.

Call the script with the path to the C3D file as a command line argument:

```
python patch_c3d.py path/to/your/file.c3d
```
or on Windows
```
python patch_c3d.py C:\\path\\to\\walk.c3d
```
or in Matlab use ``pyrunfile("rmC3DPoints.py 'path/to/your/file.c3d'")`` to run the file.

This will create a new C3D file named walk_patched.c3d with the specified changes.
