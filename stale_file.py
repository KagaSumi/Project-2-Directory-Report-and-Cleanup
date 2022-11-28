import datetime as DT
import sys
import os
import pathlib as PL


def Print(Directory: PL.Path, Date: DT.datetime):
    """
    Takes in a directory and date. Prints all files in that directory and subdirectories that have
    not been modified since Date.
    
    Args:
        Directory (PL.Path): Path of the of the directory we want to print all files from.
        Date (DT.datetime): The date where we want to judge all files in the directory.
    """
    Print_Date = Date.strftime('%Y-%m-%d')
    print(f'\nRoot directory: {os.path.abspath(Directory)}')
    print(f'Best Before Date: {Print_Date}')
    print('\nFiles to delete:')
    for file in ScrapeFolder(Directory, Date, Directory):
        print(f'{format_file_path(file[0])}{file[1]}{format_file_size(file[2])}')


def Report(Directory: PL.Path, Date: DT.datetime):
    """Takes in a directory and date, and will create a txt file that is formatted like a csv 
    {filepath},{Last Modified Date},{Size in byte}

    Args:
        Directory (PL.Path): Path of directory
        Date (DT.datetime): Date to compare last modified date.
    """
    cwd = PL.Path(__file__).parent.absolute()
    Title_date = Date.strftime('%Y_%m_%d')
    file_write_path = os.path.join(cwd, f'{Title_date}_stale_files.txt')
    with open(file_write_path, 'w') as TextFile:
        for file in ScrapeFolder(Directory, Date, Directory):
            TextFile.write(f'{os.path.join(os.path.abspath(Directory),file[0])},{file[1]},{file[2]}\n')


def ScrapeFolder(Directory: PL.Path, Date: DT.datetime, Root: PL.Path) -> list[tuple[str, str, int,str]]:
    """
    Recursive function takes in a Directory,Date,and Root directory, and check all files
    and subdirectories's files to see if they were modified before the date passed.
    This function will call itself and if it finds a folder to check for files inside the folder.

    Args:
        Directory (PL.Path): Current working directory
        Date (DT.datetime): Date to compare against date modified
        Root (PL.Path): Original working directory

    Returns:
        list[tuple[str,str,int]]: a List of a tuples containing the relative path in the
        directory from the root, the date it was last modified in the form of YYYY-MM-DD,the
        file size in bytes.
    """
    Files = os.listdir(Directory)
    List_Files = []
    for file in Files:
        Path = os.path.join(Directory,file)
        Mod_TIME = DT.datetime.fromtimestamp(os.path.getmtime(Path))
        if Mod_TIME < Date:
            Mod_TIME = Mod_TIME.strftime('%Y-%m-%d')
            Rel_Path = os.path.relpath(Path, Root)
            Size = os.path.getsize(Path)
            List_Files.append((Rel_Path, Mod_TIME, Size))
        if os.path.isdir(Path):
            if SubList := ScrapeFolder(PL.Path(Path), Date, Root):
                for item in SubList:
                    List_Files.append(item)
    return List_Files

def format_file_size(file_size: int) -> str:
    """Format file size in bytes into a human readable format

    Args:
        file_size (int): File size in bytes

    Returns:
        str: Human readable file size
    """
    SIZE_WIDTH = 5  # number of characters to use for file size excluding decimal point
    DECIMAL_PLACES = 2  # number of decimal places to use for file size
    FIELD_WIDTH = 9  # number of characters to use for the entire field
    KILOBYTE = 1024
    SIZE_FORMAT = f">{SIZE_WIDTH}.{DECIMAL_PLACES}f"

    if file_size >= (KILOBYTE**3):
        size_str = f"{round(file_size / (KILOBYTE ** 3), 2):{SIZE_FORMAT}} GB"

    elif file_size >= (KILOBYTE**2):
        size_str = f"{round(file_size / (KILOBYTE ** 2), 2):{SIZE_FORMAT}} MB"

    elif file_size >= KILOBYTE:
        size_str = f"{round(file_size / KILOBYTE, 2):{SIZE_FORMAT}} KB"

    elif file_size < KILOBYTE:
        size_str = f"{file_size:>{SIZE_WIDTH}}  B"

    return f"{size_str: >{FIELD_WIDTH}}"


def format_file_path(file_path: PL.Path) -> str:
    """Format a file path to a specific length, keeping the end of the path

    Args:
        file_path (pathlib.Path): File path to format

    Returns:
        str: Formatted file path
    """
    MAX_WIDTH = 80
    PREFIX = "..."
    format_string = f"{MAX_WIDTH}.{MAX_WIDTH}s"
    # path_str = str(file_path.resolve())
    path_str = str(file_path)

    # if the path is longer than the max width, truncate the beginning of the path,
    # leaving the end of the path and add a prefix to indicate the path has been truncated
    # The maximum width of the path is MAX_WIDTH characters
    if len(path_str) > MAX_WIDTH:
        path_str = PREFIX + str(path_str)[-(MAX_WIDTH - len(PREFIX)) :]

    return f"{str(path_str):{format_string}}"

def VerifyAction(Action: str) -> bool:
    """Takes in a string representing the action user wants to execute. Returns a boolean indicating
    True: Action is Print
    False: Action is Report

    Args:
        Action (str): Argument from command line

    Raises:
        ValueError: If Action is not Print or Report

    Returns:
        bool: True if Action is Print, False if Action is Report
    """
    if Action.upper() in ['PRINT', 'P']:
        return True
    elif Action.upper() in ['REPORT', 'R']:
        return False
    else:
        print(f'{Action} is not a valid action\nActions should be "P/Print" or "R/Report"')
        raise ValueError


def VerifyDirectory(Directory: str) -> PL.Path:
    """
    This function verifies a directory, it takes a string representing a path and returns a Path object.
    Raises a ValueError if the directory does not exist.

    Args:
        Directory (str): A string representing a directory

    Raises:
        ValueError: Raises if the directory does not exist

    Returns:
        PL.Path: Path object representing the directory passed as a string
    """
    if os.path.exists(os.path.join(PL.Path(__file__).parent.absolute(),Directory)):
        return PL.Path(Directory)
    else:
        print(f'{Directory} does not exist')
        raise ValueError


def VerifyDate(Date: str) -> DT.datetime:
    """Takes in a string representing date in ISO8601 format

    Args:
        Date (str): Should be in the form of YYYY-MM-DD

    Raises:
        ValueError: If string is not in ISO8601 format error is raised

    Returns:
        datetime: Returns a datetime value.
    """
    try:
        return DT.datetime.fromisoformat(Date)
    except ValueError:
        print(f'{Date} is not a valid date\nDate should be in the form of YYYY-MM-DD')
        raise ValueError


def main():
    try:
        ARGS = sys.argv[1:]
        Directory = ARGS[0]
        Date = ARGS[1]
        Action = ARGS[2]
    except IndexError:
        print('''Stale_file requires 3 arguments directory, date, and action
              This specified directory can be full path or relative to the current working directory
              Best Before date should be in the form of YYYY-MM-DD
              Valid Actions: R/Report or P/Print''')
        return
    try:
        Directory = VerifyDirectory(Directory)
        Date = VerifyDate(Date)
        Action = VerifyAction(Action)
    except ValueError:
        return
    if Action:
        Print(Directory, Date)
    else:
        Report(Directory, Date)


if __name__ == '__main__':
    main()
