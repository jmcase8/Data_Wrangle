from webbrowser import get
from project import get_data, comp_check, consis_check
import pytest
import pathlib
import pandas as pd
import shutil

def test_get_data():
    #test downloading a file from a url
    data = get_data(url='https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data')
    assert pathlib.Path('iris.data').exists()  == True
    assert isinstance(data, pd.DataFrame) == True
    if pathlib.Path('iris.data').exists():
        pathlib.Path.unlink(pathlib.Path('iris.data'))
    #test downloading a zip from a url, and unzipping it
    with pytest.raises(SystemExit) as e:
        data = get_data(url='https://archive.ics.uci.edu/ml/machine-learning-databases/00602/DryBeanDataset.zip')
    assert e.type == SystemExit
    assert pathlib.Path('DryBeanDataset.zip').exists()  == True
    assert pathlib.Path('DryBeanDataset/DryBeanDataset/Dry_Bean_Dataset.xlsx').is_file() == True
    if pathlib.Path('DryBeanDataset').exists():
        shutil.rmtree('DryBeanDataset')
    if pathlib.Path('DryBeanDataset.zip').exists():
        pathlib.Path.unlink(pathlib.Path('DryBeanDataset.zip'))
    #test opening local path
    with pytest.raises(SystemExit) as e:
        get_data(path='blah.txt')    
    assert e.type == SystemExit
    assert e.value.code == "Ensure you have the right link or file location"
    data = get_data(path='test_files/test.data')
    assert isinstance(data, pd.DataFrame) == True
    with pytest.raises(SystemExit) as e:
        get_data(path='test_files/test.unk')   
    assert e.type == SystemExit
    assert e.value.code == 'Please enter a supported file type.'
    
def test_com_check():
    comp_check(get_data(path='test_files/test.data'))
    assert pathlib.Path('test_project_results.txt').exists() == True
    with open('test_project_results.txt', 'r') as f:
        lines = f.readlines()
    assert lines[0] == 'Column 1 has 1 null\n'
    assert lines[1] == 'Column 2 has 1 null\n'
    assert lines[2] == 'Row 17 has 1 null\n'
    assert lines[3] == 'Row 21 has 1 null\n'
    if pathlib.Path('test_project_results.txt').exists():
        pathlib.Path.unlink(pathlib.Path('test_project_results.txt'))
def test_consis_check():
    consis_check(get_data(path='test_files/test.data'))
    assert pathlib.Path('test_project_results.txt').exists() == True
    with open('test_project_results.txt', 'r') as f:
        lines = f.readlines()
    assert lines[0] == 'Column 0 has object type\n'
    assert lines[1] == 'Column 2 has object type\n'
    assert lines[2] == 'Column 4 has object type\n'
    if pathlib.Path('test_project_results.txt').exists():
        pathlib.Path.unlink(pathlib.Path('test_project_results.txt'))