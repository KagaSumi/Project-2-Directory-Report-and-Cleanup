import datetime as DT
import sys 
import os
import pathlib as PL

#? Current test input
#! python .\stale_file.py 'C:\Users\Curry\OneDrive\Desktop\Python Code\Weeek11\test_root'  2021-05-09 print

def Print(Directory:PL.Path, Date:DT.datetime):
    """Takes in a directory and date. Prints all files in that directory and subdirectories that have not been modified since Date.

    Args:
        Directory (PL.Path): Path of the of the directory we want to print all files from.
        Date (DT.datetime): The date where we want to judge all files in the directory.
    """    
    Print_Date = Date.strftime('%Y-%m-%d')
    print(f'\nRoot directory: {Directory}')
    print(f'Best Before Date: {Print_Date}')
    print(f'Files to delete:')
    for file in ScrapeFolder(Directory,Date,Directory):
        print(f'{file[0]:{60}}  {file[1]}   {file[2]:{3}} B')
        
def Report():
    print('report')
    
def ScrapeFolder(Directory:PL.Path,Date:DT.datetime,Root:PL.Path) -> list[tuple[str,str,int]]:
    """Takes in a Directory,Date,and Root directory and returns a list of files that was last modified before the date.

    Args:
        Directory (PL.Path): Current working directory
        Date (DT.datetime): Date to compare against date modified
        Root (PL.Path): Original working directory

    Returns:
        list[tuple[str,str,int]]: a List of a tuples containing the files that were last modified before the date specified.
    """    
    Files = os.listdir(Directory)
    List_Files = []
    for file in Files:
        path = os.path.join(Directory,file)
        M_TIME = DT.datetime.fromtimestamp(os.path.getmtime(path))
        if Date > M_TIME:
            M_TIME = M_TIME.strftime('%Y-%m-%d')
            SIZE = os.path.getsize(path)
            rel_file = os.path.relpath(path,Root)
            List_Files.append((rel_file,M_TIME,SIZE))
        if os.path.isdir(path):
            if SubList := ScrapeFolder(path,Date,Root):
                for item in SubList:
                    List_Files.append(item)
    return List_Files

def VerifyAction(Action:str) -> bool:
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
    Actions = [['PRINT', 'P'],['REPORT','R']]  
    if (Action.upper() in Actions[0]):
        return True
    elif  (Action.upper() in Actions[1]):
        return False
    else:
        print(f'{Action} is not a valid action\nActions should be "Print" or "Report"')
        raise ValueError     

def VerifyDirectory(Directory:str) -> PL.Path:
    """This function verifies a directory, it takes a string representing a path and returns a Path object.
    Raises a ValueError if the directory does not exist.

    Args:
        Directory (str): A string representing a directory

    Raises:
        ValueError: Raises if the directory does not exist

    Returns:
        PL.Path: Path object representing the directory passed as a string
    """
    if os.path.exists(Directory):
        return PL.Path(Directory)
    else:
        print(f'{Directory} does not exist')
        raise ValueError

def VerifyDate(Date:str) -> DT.datetime:
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
        print('Stale_file requires 3 arguments to be specified directory , best before date , and action to take')
        return
    try:
        Directory = VerifyDirectory(Directory)
        Date = VerifyDate(Date)
        Action = VerifyAction(Action)
    except ValueError:  
            return
    if Action:
        Print(Directory,Date)
    else:
        Report()   

if __name__ == '__main__':
    main()
    
# rows = [('apple', '$1.09', '80'), ('truffle', '$58.01', '2')]

# lens = []
# for col in zip(*rows):
#     lens.append(max([len(v) for v in col]))
# format = "  ".join(["{:<" + str(l) + "}" for l in lens])
# for row in rows:
#     print(format.format(*row))