# Flask_CRUD_3
Create a website for employees to record their own work logs.

## Feature
- Login
- Logout
- Sign Up
- Edit personal information
- Work Log CRUD

## Resources Used

**Python Version :** 3.8.2  
**IDE :** VSCode  
**Requirements :**  
- Install [requirements](https://github.com/JohnnyHsieh1020/Flask_CRUD_3/blob/main/requirements.txt)
```
pip3 install -r requirements.txt
```

**Reference documents or videos :**

1. https://youtu.be/dam0GPOAvVI
2. https://www.maxlist.xyz/2020/07/30/flask-blueprint/
3. https://www.maxlist.xyz/2019/11/10/flask-sqlalchemy-setting/
4. https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_working_with_joins.htm
5. https://blog.csdn.net/u010591976/article/details/104253489
6. https://blog.csdn.net/yilovexing/article/details/104708198
## DataBase
Connect to PostgreSQL:
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_name:password@IP:PORT/db_name'
``` 
1. Use SQLAlchemy to create a PostgreSQL database.
2. Create User table, with 5 columns.
   - id(P-key)
   - name
   - email
   - password
   - identity
   - work logs
3. Create Work Log table, with 4 columns.
   - id(P-key)
   - content
   - date
   - start times
   - end time
   - user_id(F-key, ref to User-id)

