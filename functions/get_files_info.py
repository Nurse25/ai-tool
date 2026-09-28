import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    abs_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_path,directory))
    valid_target_dir = os.path.commonpath([abs_path,target_dir]) == abs_path
    if valid_target_dir is False:
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if os.path.isdir(target_dir) is False:
        return(f'Error: "{directory}" is not a directory')
    else:
        dir_list = os.listdir(target_dir)
        dir_list_list = []
        for thing in dir_list:
            dir_item = os.path.join(target_dir,thing)
            is_dir = os.path.isdir(dir_item)
            item_size = os.path.getsize(dir_item)
            dir_list_list.append(f"- {thing}: file_size={item_size} bytes, is_dir={is_dir}")
        dir_list_string = "\n".join(dir_list_list)
        return(dir_list_string)