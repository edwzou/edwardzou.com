# Dockerize Django Portfolio Project and Deploy to Synlogy NAS Server

by Edward Zou | 4 January 2024



## A) Business Needs

1. Need to deploy the Django based Portfolio website to Synology NAS Server (Container Manager app).



## B) Pre-requisites

1. a Docker Hub account - can be signed up at https://hub.docker.com.
2. a Docker Desktop app - can be downloaded from http://docker.io and installed on Windows/Mac computer.
4. a Domain registered from Godaddy or Wordpress.com or any webhosting services.
5. a Synology NAS server supporting Docker/VM, luckily we have DS920+.
6. Passion to explore and trouble-shoot, plus some hands-on of Linux commands.



## C) Create Django based Portfolio Website locally

1. Make sure the Dev Environment is up-to-date by installing the following apps/modules on to our lovely iMac 2021 (M1 chip) or M2 MacBook.

   - Node: 18.16.0

   - Python: __3.11.6__

   - Django: __4.0.0+, currently 5.0.0__

   - Port: __8010__ (default port of Django App is 8000, we customize it to be 8010, to avoid conflicting with future Django app)

   

   __Note__: On Windows client, the execution of PowerShell scripts is disabled by default. To allow the execution of PowerShell scripts, which is needed for npm global binaries, you must set the following [execution policy](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies):

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```

2. Clone my website

   ```shell
   git clone https://github.com/edwzou/edwardzou.com.git
   cd edwardzou.com #(feel free to rename it as you like)
   # install the required modules of Python3
   pip3 install -r requirements.txt
   # test run the website
   python3 manage.py runserver
   ```
   
3. Open a browser and type in the following in the address bar. 

   ```
   http://127.0.0.1:8010/
   ```
   
   Note: Press `Ctrl+C` to stop the web server.



## D) Dockerize the project

1. Create the Dockerfile

   ```bash
   ### Project Env ###
   ##  node@18.16.0
   ##  django@5.0.0
   ##  Python@3.11.6
   ##  Port: 8010 (customized port)
   
   FROM python:3.11.6-slim
   WORKDIR /app
   RUN apt-get update 
   COPY . .
   RUN pip3 install -r requirements.txt
   
   EXPOSE 8010
   
   ENTRYPOINT ["python3", "manage.py"] 
   CMD ["runserver", "0.0.0.0:8010"]
   ```

   Please note: 

   - Don't forget to `EXPOSE 8010` port (line 13).

   - The file `Dockerfile` shall be placed in the root folder of "edwardzou.com".

     

2. Build the Docker Image from M-chip based MacBook/iMac/Mac Mini or any other ARM based Linux/Windows system to target architecture system (Intel/AMD64 for Synology NAS DS920+)

   ```bash
   docker buildx build --platform linux/amd64 -t <dockerhub-id>/edspace:2.1.6 -f Dockerfile .
   ```

   * The reason to add "__--platform linux/amd64__" is due to the target Synology NAS (DS920+) is Intel/AMD CPU while building platform is a M2 MacBook (ARM based).
   * If you build the image from an Intel/AMD CPU based Linux or Windows OS, such parameter can be ignored.

   

   The Docker image shall be presented at `Image` page of `Docker Desktop` app and you can verify the inventory of docker images as below:

   ```
   docker images
   ```

3. Test run the Docker image into a Container (Optional)

   - __Running an Intel/AMD64 image/container on M1/M2 MacBook/iMac may lead to issue!!!__
   - __Better ensure the Docker Image/Container and the Running OS share the same architecture.__

   ```shell
   docker run -d -p 8010:8010 --name edspace <dockerhub-id>/edspace:2.1.6
   ```

   Then click the link of http://localhost:8010 to visit my website. 

   Note: Press the `Stop` button at `Container` page of `Docker Desktop` app to stop the web server.



## E) Publish the Docker Image

1. Tag the image which is locally stationed if you have not done such

   ```shell
   # docker tag LOCAL_IMAGE_NAME:<VERSION> DOCKER_USER_NAME/IMAGE_NAME:<VERSION>
   docker tag edspace:2.1.6 <dockerhub-id>/edspace:2.1.6
   ```

2. Publish the image to the Docker Hub - under our own channel

   ```shell
   # docker login (username/password needed)
   docker login
   # docker push DOCKER_USER_NAME/IMAGE_NAME:<VERSION>
   docker push <dockerhub-id>/edspace:2.1.6
   ```

   Wait for a minute or two, we will be able to find such image in the Docker Hub repositories.



## F) Deploy Docker Image to Synology NAS Server

1. Verify the docker image in Synology NAS DS920+

   - Please login into Synology NAS server with administor privilege and launch `Container Manager` app from `Package Center`, then 
- Switch to `Registry` panel, type "**edspace**" into the search box at top-right corner, then you shall see `edwzou/edspace` repo. 
   - click/select `edwzou/edspace` and click `Download` button to download the very image from Docker Repos (it's called `Registry` in Synology NAS system) to your local drive of NAS server. During the process, you shall get a chance to pick up the version, select the version: `2.1.6`.
- Once downloaded, the image shall be presented at `Image` panel.
  
- Select that image and click `Run` button to configure/create the Container:
  
  - At "__General Settings__" page, name the Container as "**edspace-2.1.6**" and check the checkbox of "__Enable auto-start__".
     - At __Advanced Settings__ page, Divert __local port 8010__ to __container port 8010__  with "TCP" type; Keep other settings unchanged.
  - At __Summary__ page, simply click the `Done` button.
   - Once the container starts, Open the Container's "__Log__" sub-page, you shall see no error, but regular information.




## G) Forward/Divert Domain to our local Synology NAS Server

1. Find the Publish IP address for Synology NAS while staying on the same __Intranet__ as the Synology NAS server and Google out

   ```string
   What's my IP Address?
   ```

   Then we should be able to find out our `public IP address`: __68.146.19.151__.

2. Divert the Domain to your local Synology NAS server

   This can be done by going to the `Manage DNS` app of your web hosting service provider, 

   * Add a few DNS records (`A record`) for future use as below:
     * `Type=A, Name=@, Value=68.146.19.151` ## for edwardzou.com
     * `Type=A, Name=*, Value=68.146.19.151` ## *.edwardzou.com
   
   * The CNAME record for www subdomain of edwardzou.com shall be in place by default.
   
   
   

## H) Configure Reverse Proxy on Synology NAS

1. Login to Synology NAS server with administrative user, open `Control Panel` --> `Login Portal`, then 
2. Switch to `Advanced` page, click `Reverse Proxy` button to open up the `Reverse Proxy` window
3. Configure `Reverse Proxy Rules` of __HTTPS__ 
   - Reverse Proxy Name: www_edwardzou_com_ssl
   - Source
     - Protocol: HTTPS
     - Hostname: www.edwardzou.com
     - Port: 443
     - Enable HSTS: Checked

   - Destination
     - Protocol: HTTP
     - Hostname: localhost
     - Port: 8010


4. Configure another `Reverse Proxy Rules` of __HTTP__
   - Reverse Proxy Name: www_edwardzou_com
   - Source
     - Protocol: HTTP
     - Hostname: www.edwardzou.com
     - Port: 80
   - Destination
     - Protocol: HTTP
     - Hostname: localhost
     - Port: 8010

5. Create another 2 Reverse Proxy rules for edwardzou_com_ssl, and edwardzou_com, the same way as step 3 & 4 above with `Hostname: edwardzou.com`.
6. If you have other sub domains, for instance, dev.edwardzou.com, you could mimick the step 3 and 4 above.



## I) Configure SSL Connections for the new Domain

Some websites or ISPs forbid the unencrypted connections, thus an encrypted connection (or certified SSL) must be established in place. Fortunately `Let's Encrypt` provides a free certificate for us.

1. Prior to the steps below, please ensure our domain has been diverted to our Public IP address by typing in the commands in terminal:

   ```
   ping www.edwardzou.com
   ```

   **Note**: If the public IP address outputted from the above command does not match the one of our Synology NAS server, then wait for some time till the change of Step H) is implemented.

2. Login into Synology NAS with Administrator privilege,

3. Open `Control Panel` --> `Security` --> `Certificate` page,

4. Click "Add" button to add a new certificate,

5. On next window, select "`Add a new certificate`";

6. On next window, select "`Get a certificate from Let's Encrypt`" and name it as "`edwardzou.com`";

7. On the window of "Get a Certificate from", make sure yo type in the followings:

   * Domain name: `edwardzou.com`

   * Email: youremail@gmail.com

   * Subject Alternative Name: `edwardzou.com;www.edwardzou.com;dev.edwardzou.com`

8. After a few minutes, the new item "`edwardzou.com `" shall be in place in the Certificate page.




## J) Conclusions

1. The Step B) to Step I) established a fully workflow of Dev-Test-Prod and software development.
2. The Docker system on Synology NAS differs from the regular Docker at docker.io, then some efforts are needed to facilitate the challenge.



## The End
