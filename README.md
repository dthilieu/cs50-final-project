# CS50 Final Project - Quote Generator

## Overview

The Quote Generator application is a Flask-based web project designed to allow users to browse, save, and manage inspirational quotes with dynamically generated images. Registered users can save their favorite quotes, return later to access their saved quotes, and interact with the app's features, such as deleting saved quotes or viewing quotes in a responsive and user-friendly interface. The application also supports user authentication, session management, and regular updates using APIs.

## Features

- **Dynamic Quote Generation**: Quotes and images are fetched from external APIs, combined and displayed at homepage.
- **User Authentication**: Allows users to register and log in, ensuring saved quotes are tied to individual accounts.
- **Quote Management**: Logged-in users can save quotes, delete quotes, and revisit their saved collections.
- **API and Clean Up Scheduling**: Automates the process of refreshing quotes and images in SQL database, also clear all unused quote images periodically via an every 30-minute schedule request.
- **Responsive Design**: The application is optimized for various screen sizes using a mobile-first approach with CSS media queries.
- **Flash Messaging and Alerts**: Provides immediate feedback to users for actions like saving quotes, logging in, or deleting items.

This README provides an overview of the project structure, details about individual files, and explanations for major design decisions.

---

## File Structure and Functionality

### 1. Application Files

- `app.py`
    This is the main entry point of the application. It includes:
    - Flask app setup and configuration.
    - Routes for handling user authentication (`/login`, `/register`), browsing quotes (`/`, `/save`), and managing saved quotes.
    - Integration with the SQLite database for persistent storage.
    - Scheduling logic for automated API requests.
    - Implementation of flash messages and session handling.

- `helpers.py`
    A utility file containing helper functions like:
    - Make API requests for quotes and images
    - Write quote on image
    - Clears unnecessary files in the `static/images/saved_quotes` directory.
    - Other reusable logic to keep app.py clean and modular

### 2. Templates
Contains all HTML templates for the application:
- `templates/layout.html`: Defines the overall structure and design, ensuring consistent styling and layout across all pages.
- `templates/index.html*`: The homepage of the application. Includes the interface for generating quotes, saving them, and displaying saved quotes for logged-in users.
- `templates/login.html`: The login page where users can authenticate. Provides feedback on errors such as invalid credentials.
- `templates/register.html`: The registration page where new users can sign up. Includes validation for ensuring secure and proper inputs.
- `templates/saved_quotes.html`: Displays the user's saved quotes.

### 3. Static

#### 3.1. `static/css`
Contains the CSS files for styling:
- `static/css/general.css`: Defines general styling rules and foundational styles for the application.
- `static/css/home.css`: Contains specific styling rules tailored to the homepage of the application.
- `static/css/saved-quotes.css`: Defines the styling for the saved-quotes page of the application. It includes rules for displaying the layout of saved quote images, managing heart icon used to remove quotes, and ensuring responsiveness across different screen sizes.
- `static/css/auth-form.css`: Defines the styling for the login and registration pages of the application. It includes rules for form layout, input fields, labels, buttons, and error message displays.
  
#### 3.2. `static/images/`
Stores image files for the quotes, including temporary generated quotes and saved user-specific images. Files are managed dynamically, with unused images cleared every 30 minutes.

#### 3.3. `static/js/`
Contains JavaScript for client-side interactions:
- `static/js/dashboard.js`: Event listeners for navigating between saved quotes page and generate quote page.
- `static/js/home.js`: Event listeners for generate next quote image (next button), go back to previous quote image (previous button), and save current quote image (like and save button).
- `static/js/saved-quotes.js`: Event listeners for deleting and re-saving saved quote image (heart button).

### 4. Database `database.db`
The SQLite database that stores:
- `users`: User account information (`username`, `hash`).
- `saved_quotes`: Saved quotes information (`user_id`, `image_id`, `image_path`, `is_deleted`).
- `image_urls`: Image urls data from API request (`url`), updated every 30 minutes.
- `quotes`: Quote data from API request (`quote`, `author`), updated every 30 minutes.

### 5. Configuration and Utilities

- `requirements.txt`: Lists all dependencies required for the project, including Flask, SQLite, and Schedule. This file ensures the application can be set up easily in new environments.
- `README.md`: The documentation file you’re reading now. It describes the project, its structure, and key considerations.

---

## Key Design Decisions

1. **User Authentication with Flask Sessions**  
   The user authentication system was designed to prioritize security and simplicity. Passwords are hashed using a robust algorithm before storage. Sessions are used to maintain user state without relying on cookies directly. 

2. **API Integration**  
   The external quote API is scheduled to refresh every 30 minutes to avoid overwhelming the external API and ensure fresh data. The `schedule` library was selected for its ease of integration with Flask and Python scripts.

3. **Responsive Design**  
   A mobile-first approach ensures the app remains visually appealing and functional across devices. CSS media queries simplify this adaptability.

4. **File Management**  
   The `helpers.py` script includes a function to clear unused images, ensuring efficient file storage. This was implemented to prevent server clutter as users save and delete quotes.

4. **Flash Messages and User Notifications**  
   Flash messages are used to inform users about actions like successful logins or errors. These messages are displayed prominently and styled to match the application’s theme. 

6. **Database Schema**  
   Each saved quote has an `is_deleted` flag rather than being physically removed, enabling easy recovery and tracking.

## Future Enhancements

Potential improvements includes:

- Allowing users to customize and share their saved quotes on social media.   
- Adding search functionality to filter saved quotes/ random quotes by keywords or authors.
- Adding customize function to allow user customize their own quote image.

## Conclusion

This project, Quote Generator, provides a dynamic and interactive platform to generate, save, and manage inspiring quotes. 

It is a project I developed using the knowledge gained from CS50x and other short courses, leveraging Flask, SQLite, JavaScript, and CSS as the primary technologies.

Also, I would like to give credit to [Unplash Image API](https://unsplash.com/) for providing images via requests, [ZenQuotes.io](ZenQuotes.io) for providing quotes via requests, [ChatGPT](https://chatgpt.com) for helping organizing my thoughts and providing suggestions, thank you!

This README serves as a comprehensive guide to understanding the project's structure, functionality, and design decisions, ensuring a solid foundation for future development and enhancements.
