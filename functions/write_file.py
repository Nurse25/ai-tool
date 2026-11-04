import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    abs_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_path,file_path))
    valid_target_file = os.path.commonpath([abs_path,target_file]) == abs_path
    if valid_target_file is False:
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    if os.path.isdir(target_file) is True:
        return(f'Error: Cannot write to "{file_path}" as it is a directory')
    dir_to_make = os.path.dirname(target_file)
    os.makedirs(dir_to_make,exist_ok=True)
    with open(target_file,mode='w') as file:
        file.write(content)
    return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a specified file within the working directory (overwriting if the file exists)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}