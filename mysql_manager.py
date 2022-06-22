import mysql.connector

USER = "root"
PASSWORD = "root"
HOST = "127.0.0.1"
PORT = '3307'
DATABASE = "publications_db"

class MySQLManager:
    def __init__(self):
        self.cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    
    def insert(self, obj, year):       
        sttmt = "INSERT INTO publications_tab_"+year+"(id, photo, author, university, vector, title, link, abstract) VALUES (%(id)s, %(photo)s, %(author)s, %(university)s, %(vector)s, %(title)s, %(link)s, %(abstract)s)"
        cursor = self.cnx.cursor()
        cursor.execute(sttmt, obj)
        self.cnx.commit()
        cursor.close()

    def delete_candidate(self):
        cursor = self.cnx.cursor()
        cursor.execute("delete from candidate")
        self.cnx.commit()
        cursor.close()

    def insert_candidate(self, obj): 
        sttmt = "INSERT INTO candidate(Photo, Candidate, University, Number_of_docs, Avg_sim, Average_Similarity, Image_Avg, Variance, Image_Var, Related) VALUES (%(photo)s, %(author)s, %(university)s, %(doc_count)s, %(avg_sim)s, %(mean)s, %(meanimage)s, %(var)s, %(varimage)s, %(related_count)s)"
        cursor = self.cnx.cursor()
        cursor.execute(sttmt, obj)
        self.cnx.commit()       
        cursor.close()
    
    def select(self,year):
        sttmt = "SELECT * FROM publications_tab_"+year
        cursor = self.cnx.cursor()
        cursor.execute(sttmt)
    
        res = []
        for (id, photo, author, university, vector, title, abstract, link) in cursor:
            res.append({
                "id": id,
                "photo": photo,
                "author": author,
                "university": university,
                "vector": vector,
                "title": title,
                "abstract": abstract,
                "link": link
            })

        self.cnx.commit()
        cursor.close()
        return res
    
    def close(self):
        self.cnx.close()
