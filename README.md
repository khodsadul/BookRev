# BookRev
A Flask Project for managing book review and rattings. Following functionalities are offered by this project:
1. Registeration by a new user
2. Verify account by verify email.
3. Reset password when forgot.
4. Login and view ratings for existing books.
5. Add a new book.
6. Add a rating or comment on an existing book.

### Important Technical Features
1. Sending Email for registeration and forget password.
2. JWT based user authentication and authorization.
3. Rest Api Creation.
4. Swagger UI.
5. Application of SQLAlachemy library with PostgreSQL

### Available Endpoints
![image](https://user-images.githubusercontent.com/69482350/166149915-47742df9-9681-45d5-956a-1e10dd7c9069.png)



### Database Setup
Check db folder for database script. 
To setup db create a postgres database with db name *postgres* and run __ddl.sql__ file in postgres db.
There are three main entities:
1. User: stores user information.
2. Book: stores boook information.
3. UserBook: stores ratings and comments on a book created by any user.

### To run the project on your computer
1. Clone project 
2. Import it into pycharm or any python ide/editor.
3. Setup postgres database by following above steps for db setup.
4. Navigate to the project root folder.
5. Run command __*pip3 -r requirements.txt*__
6. Run command __*flask routes*__ to check all available routes.
7. Run project with __*flask run*__ command.
