**README**

**Project Name: Question and Answer App**

**Overview:**
The Question and Answer App is a Flask-based web application designed to facilitate communication between users by allowing them to ask questions, answer questions, and view unanswered questions. The application provides a centralized platform for managing questions and answers, improving collaboration and knowledge sharing among users.

**Setup Instructions:**

1. **Clone the Repository:**
   ```
   git clone https://github.com/Temple111/specializationproject
   ```

2. **Install Dependencies:**
   ```
   cd question_and_answer_app
   pip install -r requirements.txt
   ```

3. **Database Setup:**
   - The application uses SQLite as its database engine.
   - Ensure that SQLite is installed on your system.
   - Initialize the database by running the following command:
     ```
     python initialize_database.py
     ```

4. **Run the Application:**
   ```
   python app.py
   ```
   The application will run locally on http://127.0.0.1:5000/ by default.

**Usage Outlines:**

1. **Registration:**
   - Navigate to the registration page (/register).
   - Enter a username and password to create a new account.

2. **Login:**
   - Access the login page (/login).
   - Enter your registered username and password to log in.

3. **Asking Questions:**
   - Logged-in users can ask questions by navigating to the ask questions page (/askquestions).
   - Select a teacher from the dropdown menu and submit your question.

4. **Answering Questions:**
   - Teachers can answer questions by visiting the unanswered questions page (/unansweredquestions).
   - Click on a question to view details and submit an answer.

5. **Viewing Unanswered Questions:**
   - Users can view unanswered questions by accessing the unanswered questions page (/unansweredquestions).

6. **Promoting Users:**
   - Admins can promote users to teachers by visiting the all users page (/allusers).
   - Click on the "Promote" button next to the user you want to promote.

7. **Logging Out:**
   - Users can log out by clicking on the logout button or navigating to the logout page (/logout).

**Project Architecture:**

1. **Flask Framework:**
   - The application is built using the Flask web framework, which provides tools and libraries for developing web applications in Python.

2. **SQLite Database:**
   - The application uses SQLite as its database engine for storing user information, questions, and answers.

3. **HTML Templates:**
   - HTML templates are used to render dynamic content and user interfaces.

4. **Session Management:**
   - Flask's session management is utilized for maintaining user sessions and persisting user-specific data across requests.

5. **Password Hashing:**
   - User passwords are hashed using the PBKDF2 algorithm with SHA-256 before storing them in the database.

6. **Routing Logic:**
   - Flask's routing system is used to define routes for different parts of the application, such as login, registration, asking questions, answering questions, etc.

7. **Error Handling:**
   - The application handles errors such as incorrect login credentials, duplicate usernames during registration, etc., and displays appropriate error messages to the user.

8. **Model-View-Controller (MVC) Pattern:**
   - The application follows the MVC pattern, where Flask serves as the Controller, HTML templates serve as the View, and SQLite database handles the data storage (Model).

This README provides setup instructions, usage outlines, and an overview of the project architecture for the Question and Answer App. Follow these instructions to set up and use the application effectively.



**Authors:**
Temple Eseigbe - templeeseigbe014@gmail.com
Okang Etta - okang.etta@gmail.com
Asunde Osiro
