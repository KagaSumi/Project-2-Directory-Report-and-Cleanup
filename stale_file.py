import datetime as DT
import sys 
import os
import pathlib as PL

def Print(Directory:PL.Path, Date:DT.datetime):
    print(f'\nRoot directory: {Directory}\nBest Before Date: {Date}')
    print(f'Files to delete:')
    ScrapeFolder(Directory,Date,True)

def ScrapeFolder(Directory:PL.Path,Date:DT.datetime,PRINT_REPORT:bool):
    if PRINT_REPORT:
        Files = os.listdir(Directory)
        for file in Files:
            path = os.path.join(Directory,file)
            M_TIME = DT.datetime.fromtimestamp(os.path.getmtime(path))
            if Date > M_TIME:
                M_TIME = M_TIME.strftime('%Y-%m-%d')
                SIZE = os.path.getsize(path)
                print(f'{file} was last modified: {M_TIME} {SIZE} bytes')
            if os.path.isdir(path):
                ScrapeFolder(path,Date,True)
    else:
        #Todo:Report part of ScrapeFolder
        pass

def Report():
    print('report')

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