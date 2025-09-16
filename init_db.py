import pymysql
conn=None
try:
    conn=pymysql.connect(
    host="localhost",
    user="appuser",
    password="app_password",
    database="ai_resume_analyser"
    )
    cursor=conn.cursor()
    cursor.execute("""
    create table if not exists users(
               id int auto_increment primary key,
               username varchar(100) not null unique,
               password varchar(255) not null
               );
     """)
    # conn.commit()

    cursor.execute("""
create table if not exists resumes
                   (id INT AUTO_INCREMENT PRIMARY KEY,
                   user_id int,
                   filename varchar(50),
                   ats_score int  not null,
                   suggestions text,
                   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE);
                   """)
    conn.commit()
    print("Table created sucessfully")
except Exception as e:
     print(e)
finally:
 if conn:
  conn.close()