# Django Portfolio Website

by Edward Zou | 6 October 2023



![forepage](static/images/forepage.png)



## Intro

This is a simple, but beautiful personal Portfolio website utilizing the technologies below:

* Python - Django
* Database with SQLite3 (can switch to PostgreSQL, MySQL)
* Bootstrap with localized CSS files
* JavaScript
* Docker deployment



## Future plan

Thinking about re-writing the webapp using `React/MaterialUI + Express + SQLite3/PostgreSQL + Tailwind` in the future.



## How to run the Webapp locally

1. Pull down the GitHub repo and extract to a local folder, then run the command:

   ```
   cd digiCV2Django
   ```

2. Install the libraries in `requirement.txt` locally.

   ```
   pip install -r requirements.txt
   ```

3. Open the terminal in VS Code and type in:

   ```
   python3 manage.py runserver
   ```

4. then open a browser and point to https://localhost:8000.



## Run the Webapp in Docker Container locally

1. Start your Docker Desktop (Windows or macOS or Linux), then build the image

   ```
   docker build -t <yourDockerAccount>/digicv2dj:0.1 .
   ```

2. Docker run:

   ```
   docker run -d -p 127.0.0.1:8000:800 --name DigiCV2dj <yourDockerAccount>/digicv2dj:0.1
   ```

3. Open a browser and point to https://127.0.0.1:8000.



## Deploy the Webapp to your GitHub

1. Create a repo on your GitHub account, say `digicv2dj`.

2. Push the webapp to the GitHub:

   ```
   git init
   git add .
   git commit -m "DigiCV2dj-1st-commit"
   git branch -M main
   git remote add origin https://github.com/<YourGitHubAccount>/DigiCV2dj.git
   git push -u origin main
   ```



## Env. of Dockerizing the Webapp on render.com

```
PYTHON_VERSION: 3.10.11
NODE_VERSUIN: 18.16.0
PORT: 8000
```



## License

\- GPL
