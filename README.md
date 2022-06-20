# Career-Prospect-System

Career Prospect System(CPS) is a search engine to match a job or career with job candidates by using job candidates's publications. SciBERT model is used to obtain the job matching rate and average similarity between each job candidates and jobs by the users.

## Installation
1. Download this repository.

2. Change the MySQL connection to your own MySQL scheme from app.py line 14 to 19.
![image](https://user-images.githubusercontent.com/93475397/169525877-40d5b286-4192-4a84-8285-7458ecdcb80e.png)

3. Create database in MySQL. There are 6 databases that should be created, including job, candidate, publications_tab_2018, publications_tab_2019, publications_tab_2020, and publications_tab_2021. You can copy the code from the MySQL folder and paste it into your MySQL to create these databases. 

4. Import data into database. Only job databases need to import the excel file from MySQL. 
  Excel file(job): https://drive.google.com/file/d/10cQdtfhiWztbq4RQSOWQmy-me9DQ4WU6/view?usp=sharing

5. Import data from init_db.py. 
   * Import excel file 18.xlsx, 19.xlsx, 20.xlsx, and 21.xlsx.
   
   * Import excel file 18.xlsx, change line 7 in init_db.py and line 55 in mysql_manager.py before import data. Then, run init_db.py.
    Excel file(18.xlsx): https://docs.google.com/spreadsheets/d/1XrrwoEBH8UwHWl95rRerpb_D9wLDeu2E/edit?usp=sharing&ouid=106666487931104475614&rtpof=true&sd=true
    
   ![image](https://user-images.githubusercontent.com/93475397/169506384-ed7f24cb-26cc-4f07-8db4-6e4ccba29c3b.png)
   ![image](https://user-images.githubusercontent.com/93475397/169506496-ea423afd-e22d-4132-9a41-4c51f62be7a6.png)

   * Import excel file 19.xlsx, change line 7 in init_db.py and line 55 in mysql_manager.py before import data. Then, run init_db.py.
   Excel file(19.xlsx): https://docs.google.com/spreadsheets/d/1CkVkQKfpFN5Mj2ZIcwrif2XtjqP7RtHg/edit?usp=sharing&ouid=106666487931104475614&rtpof=true&sd=true
   
   ![image](https://user-images.githubusercontent.com/93475397/169509417-3aab8a81-7022-49b0-8994-2124eece3406.png)
   ![image](https://user-images.githubusercontent.com/93475397/169509516-3cf7e4b2-6e60-4080-952f-de54df69168a.png)

   * Import excel file 20.xlsx, change line 7 in init_db.py and line 55 in mysql_manager.py before import data. Then, run init_db.py.
   Excel file(20.xlsx): https://docs.google.com/spreadsheets/d/1OObAufBVpHCt_2N9RXcJFjr-nAoDT0_p/edit?usp=sharing&ouid=106666487931104475614&rtpof=true&sd=true
   
   ![image](https://user-images.githubusercontent.com/93475397/170810353-762b6b84-27e4-4895-88d1-ca9f43dd9cbf.png)
   ![image](https://user-images.githubusercontent.com/93475397/169509623-7647b4de-2818-412b-8e77-786c6b220598.png)

   * Import excel file 21.xlsx, change line 7 in init_db.py and line 55 in mysql_manager.py before import data. Then, run init_db.py.
    Excel file(21.xlsx): https://docs.google.com/spreadsheets/d/1NOd6vDG2bDnd2gwr51k-1KjRvqpRVOOZ/edit?usp=sharing&ouid=106666487931104475614&rtpof=true&sd=true
    
   ![image](https://user-images.githubusercontent.com/93475397/169509864-a0e9ea63-5e39-429e-bcf5-84ef9b028ea0.png)
   ![image](https://user-images.githubusercontent.com/93475397/169509945-978831d4-6b69-453d-9a48-88fc98611945.png)
   * Check and make sure the excel file is imported into the correct database.

6. After all step had been done, you can run app.py to execute the system.




 
"# career-prospect-system" 
