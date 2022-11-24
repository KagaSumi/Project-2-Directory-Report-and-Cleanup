import datetime as DT
import sys 
import os
import pathlib as PL

def Print():
    print('print')
    return

def Report():
    print('report')
    return

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
        print(f'{Action} is not a valid input')
        raise ValueError     

def VerifyDirectory(Directory:str):
    return

def VerifyDate(Date):
    try:
        return DT.date.fromisoformat(Date)
    except ValueError:
            print(f'{Date} is not a valid date')
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
        Action = VerifyAction(Action)
        VerifyDirectory(Directory)
        Date = VerifyDate(Date)
        print(Date)
    except ValueError:  
            return
        
    if Action:
        Print()
    else:
        Report()
    

if __name__ == '__main__':
    main()