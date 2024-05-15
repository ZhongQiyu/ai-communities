def split_file(file_path, size_mb=10, output_dir=None):
    """ Split a file into multiple parts of a specified size in megabytes.
    
    Args:
    file_path (str): The path of the file to split.
    size_mb (int, optional): The size of each split file in megabytes. Default is 10 MB.
    output_dir (str, optional): The directory to save the split files. If None, splits in the same directory as the original file.
    """
    # Convert MB to bytes
    buffer_size = size_mb * 1024 * 1024
    part_num = 1
    
    if output_dir is None:
        output_dir = os.path.dirname(file_path)  # Default to the same directory as the file
    
    with open(file_path, 'rb') as f:
        chunk = f.read(buffer_size)
        while chunk:
            # Build the part file name
            part_name = f"{output_dir}/{os.path.basename(file_path)}_part{part_num}"
            with open(part_name, 'wb') as part_file:
                part_file.write(chunk)
            part_num += 1
            chunk = f.read(buffer_size)

# 使用示例
split_file('/path/to/largefile.dat', size_mb=100, output_dir='/path/to/output')
