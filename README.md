### **Gallery**

#### **1. Overview**

This project is a web-based media gallery built with the Flask framework. It is designed to efficiently serve a directory of images and videos. The core design philosophy is to perform expensive operations like scanning for media and generating thumbnails offline via command-line scripts. The web application then reads from a pre-generated "manifest" file and a cache of thumbnails, ensuring fast page loads and minimal processing during user requests.

The application is served in production using Gunicorn.

#### **2. Project Structure**

The project is organized into several key directories and files:

  * `$app/$`: The main Flask application module.
      * `$static/$`: Contains static assets like CSS, JavaScript, and fonts.
      * `$templates/$`: Contains Jinja2 HTML templates for rendering pages.
      * `$__init__.py$`: Initializes the Flask application instance.
      * `$config.py$`: Handles loading configuration from the environment.
      * `$manifest.py$`: Contains logic for reading and processing the media manifest file.
      * `$models.py$`: Defines data structures used within the application.
      * `$routes.py$`: Defines the application's URL endpoints and view functions.
      * `$utils.py$`: A module for shared utility functions.
  * `$bin/$`: A collection of executable shell scripts for managing the application.
  * `$media/$`: The directory where user-uploaded images and videos should be placed.
  * `.cache/`: A directory for storing cached data, primarily generated thumbnails.
  * `.venv/`: The Python virtual environment for project dependencies.
  * `.env`: The environment configuration file.
  * `$requirements.txt$`: A list of Python packages required for the project.

#### **3. Core Components**

##### **Management Scripts (\`$bin/$)**

These scripts are the primary tools for managing the gallery's content and running the server.

  * `$run$`: Starts the production server using Gunicorn.
      * `-H <ADDR>`: Binds the server to a specific address.
      * `-P <PORT>`: Binds the server to a specific port.
      * `-S <PATH>`: Binds to a Unix socket.
  * `$run-dev$`: (Inferred) A script to run the Flask development server, likely with hot-reloading enabled.
  * `$update-manifest$`: Scans the `$MEDIA_DIR$` directory and updates a JSON manifest file (`$manifest.json$`). This file serves as a quick-to-read database of all available media, which the Flask app uses to build the gallery pages.
      * `-p <PID>`: After updating, it can signal a running server to reload its configuration.
  * `$update-cache$`: Generates thumbnails for media files to ensure the gallery front-end loads quickly.
      * `-i`: Generate thumbnails for images only.
      * `-v`: Generate thumbnails for videos only.
      * `-f`: Force regeneration of thumbnails even if they already exist.
      * `-p <PID>`: Signal a running server to reload after the cache is updated.
  * `$reload-server$`: A utility to gracefully reload one or more running server processes, identified by their Process ID (PID). This is useful for applying changes without downtime.

##### **Configuration (\`$.env$)**

The application's behavior is controlled by environment variables defined in the `.env` file.

  * `$MEDIA_DIR$`: The path to the directory containing your source media files (default: `'media'`).
  * `$IMAGE_EXTS$`: A comma-separated list of allowed image file extensions.
  * `$VIDEO_EXTS$`: A comma-separated list of allowed video file extensions.
  * `$CACHE_DIR$`: The path to the directory where cache files, like thumbnails, are stored (default: `'.cache'`).
  * `$MANIFEST_FILE$`: The name of the manifest file that lists all media (default: `'manifest.json'`).
  * `$THUMBNAILS_FILE$`: The name of the subdirectory within `$CACHE_DIR$` to store thumbnails (default: `'thumbnails'`).
  * `$THUMBNAILS_EXT$`: The file extension to use for all generated thumbnails (default: `'.jpg'`).

#### **4. Setup and Installation**

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```
2.  **Create Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment:**
      * Copy the `.env.example` to `.env` (if one exists) or create a new `.env` file.
      * Adjust the variables inside `.env` to match your desired paths.
5.  **Create Directories:**
    ```bash
    mkdir media .cache
    ```

#### **5. Usage and Workflow**

The typical workflow for adding new content and running the server is as follows.

1.  **Add Media:** Place your new image and video files into the directory specified by `$MEDIA_DIR$` (e.g., `media/`).

2.  **Update the Manifest:** Run the `$update-manifest$` script to make the application aware of the new files.

    ```bash
    bin/update-manifest
    ```

3.  **Generate Thumbnails:** Run the `$update-cache$` script to create thumbnails for the new files.

    ```bash
    bin/update-cache
    ```

4.  **Run the Server:**

      * **For development:** Use the `$run-dev$` script.
        ```bash
        bin/run-dev
        ```
      * **For production:** Use the `$run$` script.
        ```bash
        bin/run -P 8000
        ```

##### **Updating a Live Server**

To add new media to a running production server without restarting it:

1.  Add your new files to the `media/` directory.
2.  Find the PID of the running Gunicorn server (e.g., using `ps aux | grep gunicorn`).
3.  Run the update scripts with the `-p` flag to automatically reload the server.
    ```bash
    # Let's say the PID is 12345
    bin/update-manifest -p 12345
    bin/update-cache -p 12345
    ```
    This ensures the server picks up the new manifest and can serve the new thumbnails without any downtime.
