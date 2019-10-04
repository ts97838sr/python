import pandas ,os

class ReadFile():
    def __init__(self,name):
        self.name = Name

    def extn(self):
        filename,file_extension = os.path.splitext(self)
        return file_extension
    def read_file(self):
        filename,file_extension = os.path.splitext(self)
        if file_extension == ".xlsx":
            df = pandas.read_excel(open(self,'rb'))
        elif file_extension == ".csv":
            df = pandas.read_csv(open(self,'rb'))
        elif file_extension == ".json"
            df = pandas.read_json(open(self,'rb'))
        elif file_extension == ".parquet"
            df = pandas.read_parquet(open(self,'rb'),engine = 'auto')
        elif file_extension == ".avro"
            df = pandas.read_pickle(open(self,'rb'),compression = 'gzip')
        else
            "Extension Not yet supported"
        return df
    def read_file_custom_header(self,column_names):
        filename,file_extension = os.path.splitext(self)
        if file_extension == ".xlsx":
            df.pandas.read_excel(open(self,'rb'),skiprows=1,names=column_names)
        elif file_extension == ".csv"
            df.pandas.read_csv(open(self,'rb'),skiprows=1,names=column_names)
        return df
