from excel_manager import ExcelManager
from mysql_manager import MySQLManager
from scibert import SciBERT


EXCEL_FILENAMES = ["21.xlsx"] # use 4 files to create 4 tables in database

def main():
    mysql = MySQLManager()
    scibert = SciBERT()
    for filename in EXCEL_FILENAMES:
        excel = ExcelManager(filename)
        data = excel.get()
        # print(data, flush=True)
        print("Inserting records from {}".format(filename), flush=True)

        for i in range(len(data)):
            if i > 0 and i % 100 == 0:
                print("Inserted {} records into MySQL. ".format(i))
            record = {}
            record["photo"] = data[i]["Photo"]
            record["author"] = data[i]["Authors"]
            record["university"] = data[i]["University"]
            record["title"] = data[i]["Title"]
            record["abstract"] = data[i]["Abstract"]
            record["link"] = data[i]["Link"]
            try:
                vector = scibert.vectorize(data[i]["Abstract"])
            except:
                continue
            record["vector"] = vector.dumps()
            mysql.insert(record)
    mysql.close()
    print("Data Inserted", flush=True)

if __name__ == "__main__":
    main()