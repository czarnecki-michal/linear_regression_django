import pandas as pd

def load_data():
    django_project = "../.."
    csv_filepathname = "../../machine_learning/salary.csv"

    import sys, os
    sys.path.append(django_project)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cognitive.settings'

    from data_presentation.models import Data
    data = pd.read_csv(csv_filepathname)

    for row in data:
        print(row)

load_data()