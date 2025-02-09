# filepath: /vercify_prototype_2/vercify_prototype_2/README.md
# Vercify Prototype

## Overview
Vercify is a web application designed for fact-checking content and managing user-generated posts and comments. It allows users to verify the accuracy of information, engage in discussions through comments, and upvote or downvote posts and comments.

## Features
- **Fact-Checking**: Users can submit content for verification, and the application will return a status, score, and explanation.
- **Post Management**: Users can create posts, view all posts, and interact with them through comments.
- **Comment System**: Users can add comments to posts, and each comment can be upvoted or downvoted.
- **User Authentication**: Users can register and log in to manage their posts and comments.

## Project Structure
```
vercify_prototype_2
├── src
│   ├── comments.py        # Functions for managing comments and posts
│   ├── models.py          # Data models for Post and Comment
│   ├── posts.py           # In-memory implementation for posts and comments
│   └── auth.py            # User authentication functionality
├── static
│   ├── script.js          # JavaScript for frontend interactions
│   └── styles.css         # Styles for the web application
├── templates
│   └── index.html         # Main HTML template for the web application
├── .gitattributes          # Git configuration for line endings
├── .gitignore              # Files and directories to ignore by Git
├── app.py                 # Entry point of the application
├── gemini.py              # Logic for fact-checking using an external API
├── requirements.txt       # Project dependencies
├── routes.py              # API routes for the application
├── supabase_client.py     # Initializes the Supabase client
├── testconfig
│   └── testing.py         # Example tests for the application
├── vercel.json            # Configuration for deploying on Vercel
└── README.md              # Documentation for the project
```

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd vercify_prototype_2
   ```

2. **Install Dependencies**:
   Make sure you have Python and pip installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your Supabase credentials:
   ```
   SUPABASE_URL=<your-supabase-url>
   SUPABASE_KEY=<your-supabase-key>
   DEEPSEEK_API_KEY=<your-deepseek-api-key>
   ```

4. **Run the Application**:
   Start the application using:
   ```bash
   python app.py
   ```

5. **Access the Application**:
   Open your web browser and go to `http://localhost:5000` to access the application.

## Usage
- To create a post, enter your content in the provided text area and click "Create Post".
- To verify content, enter it in the verification section and click "Check".
- You can add comments to posts and interact with them using upvote and downvote buttons.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.