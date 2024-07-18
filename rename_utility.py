import os
from datetime import datetime

# Function checks if user provided position is negative. If so, subtract it from total length.
def sort_filename_pos(filename, t):
    return len(filename) + t[0] if t[0] < 0 else t[0]

# Function to rename file(s) within a directory
def rename(directory, replace=[], remove=[], add=[], replace_first=False, 
            check_func=lambda file: True, extension='', include_extension=False, 
            overwrite=False, inc_subdirs=False, show_output=False, log=False, 
            log_path='changes.log', test=False):
    """
    Parameters:
    directory (str): Path to the directory containing files to be renamed.
    replace (list of tuples): List of tuples with strings to be replaced and their replacements.
    remove (list of tuples): List of tuples specifying slices (start, end) to be removed from filenames.
    add (list of tuples): List of tuples specifying positions and texts to be added to filenames.
    replace_first (bool): If True, replace only the first occurrence of each string in `replace`.
    check_func (function): Function to filter files to be renamed.
    extension (str): Only rename files with this extension.
    include_extension (bool): If True, consider the file extension as part of the filename for renaming.
    overwrite (bool): If True, overwrite existing files with new names.
    inc_subdirs (bool): If True, include subdirectories in the renaming process.
    show_output (bool): If True, print renaming actions to the console.
    log (bool): If True, log renaming actions to a file.
    log_path (str): Path to the log file.
    test (bool): If True, perform a dry run without making any changes.

    Returns:
    tuple: Number of files renamed and total number of files processed.
    """
    
    if not os.path.exists(directory):
        print(f'Directory not found: "{directory}"')
        return 0, 0

    files_rename_count = 0
    files_total_count = 0
    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and item.endswith(extension):
            files_total_count += 1
            if check_func(item):
                files_rename_count += 1
                new_filename, ext = (item, '') if include_extension else (item[:-4], item[-4:])
                
                for old, new in replace:
                    new_filename = new_filename.replace(old, new, 1) if replace_first else new_filename.replace(old, new)
                
                for slice in remove:
                    if slice[0] >= 0 and slice[1] >= 0:
                        slice_start, slice_end = min(slice), max(slice)
                    elif slice[0] < 0 and slice[1] < 0:
                        slice_start = len(new_filename) + 1 + min(slice)
                        slice_end = len(new_filename) + 1 + max(slice)
                    elif slice[0] >= 0 and slice[1] < 0 and len(new_filename) + slice[1] > slice[0]:
                        slice_start, slice_end = slice[0], len(new_filename) + 1 + slice[1]
                    else:
                        print(f'Error: ({slice[0]} to {slice[1]}) is not a valid range for removal!')
                        break
                    new_filename = new_filename[:slice_start] + '*' * (slice_end - slice_start) + new_filename[slice_end:]
                
                add.sort(key=lambda x: sort_filename_pos(new_filename, x))
                offset = 0
                for pos, text in add:
                    pos = pos if pos >= 0 else len(new_filename) + 1 + pos
                    new_pos = pos + offset
                    new_filename = new_filename[:new_pos] + text + new_filename[new_pos:]
                    offset += len(text)
                
                new_filename = new_filename.replace('*', '')
                
                if show_output or test:
                    print(f'{item} => {new_filename + ext}')
                
                if log:
                    with open(log_path, 'a') as log_file:
                        log_file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {item} => {new_filename + ext}\n')
                
                if not test:
                    new_item_path = os.path.join(directory, new_filename + ext)
                    if os.path.exists(new_item_path):
                        if not overwrite:
                            print(f'Error: {new_item_path} already exists!')
                            continue
                        else:
                            print(f'Overwrite: {new_item_path} already exists!')
                            os.remove(new_item_path)
                    os.rename(item_path, new_item_path)
        
        elif inc_subdirs and os.path.isdir(item_path):
            subdir_count = rename(item_path, replace, remove, add, replace_first, check_func, extension, include_extension, overwrite, inc_subdirs, show_output, log, log_path, test)
            files_rename_count += subdir_count[0]
            files_total_count += subdir_count[1]
    
    return files_rename_count, files_total_count
