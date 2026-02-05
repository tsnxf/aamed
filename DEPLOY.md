# Step-by-Step Deployment Guide for AAMed.tech

Follow these steps exactly to deploy your websites.

## Part 1: Push to GitHub (On Your Local Machine)

I have already initialized the git repository and added the remote for you. 
Open your terminal in **this workspace** and run:

1.  **Add all files and commit:**
    ```bash
    git add .
    git commit -m "Complete website build"
    ```

2.  **Push to GitHub:**
    (You might be asked for your GitHub username and password/token)
    ```bash
    git push -u origin main
    ```

---

## Part 2: Deploy on VPS (On Your Server)

SSH into your VPS (replace `user@your-vps-ip` with your actual login):
```bash
ssh user@your-vps-ip
```

Then run these commands one by one:

1.  **Navigate to web root:**
    ```bash
    cd /var/www
    ```
    *(If this folder doesn't exist, create it: `sudo mkdir -p /var/www`)*

2.  **Clone the Repository:**
    ```bash
    sudo git clone https://github.com/tsnxf/aamed.git
    ```
    *(If you already cloned it before, go into the folder `cd aamed` and run `sudo git pull origin main` instead)*

3.  **Update Nginx Configuration:**
    Open the Nginx config file:
    ```bash
    sudo nano /etc/nginx/sites-available/aamed
    ```
    
    Paste the following block into it (delete anything else in that file):

    ```nginx
    # 1. Main Domain: aamed.tech
    server {
        listen 80;
        server_name aamed.tech www.aamed.tech;
        root /var/www/aamed/main;
        index index.html;
        location /shared/ { alias /var/www/aamed/shared/; }
        location / { try_files $uri $uri/ =404; }
    }

    # 2. Subdomain: deu.aamed.tech
    server {
        listen 80;
        server_name deu.aamed.tech;
        root /var/www/aamed/deu;
        index index.html;
        location /shared/ { alias /var/www/aamed/shared/; }
        location / { try_files $uri $uri/ =404; }
    }

    # 3. Subdomain: trade.aamed.tech
    server {
        listen 80;
        server_name trade.aamed.tech;
        root /var/www/aamed/trade;
        index index.html;
        location /shared/ { alias /var/www/aamed/shared/; }
        location / { try_files $uri $uri/ =404; }
    }
    ```
    Press `Ctrl+O`, `Enter`, then `Ctrl+X` to save and exit.

4.  **Enable the Site & Test:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/aamed /etc/nginx/sites-enabled/
    sudo nginx -t
    ```
    *(If `nginx -t` returns success, proceed)*

5.  **Restart Nginx:**
    ```bash
    sudo systemctl restart nginx
    ```

6.  **Secure with SSL (HTTPS):**
    First, install the Certbot Nginx plugin (if missing):
    ```bash
    sudo apt update
    sudo apt install python3-certbot-nginx
    ```

    Then generate the certificates:
    ```bash
    sudo certbot --nginx -d aamed.tech -d deu.aamed.tech -d trade.aamed.tech
    ```

## Optional: Setup SSH for Password-less Git Pull
To avoid typing your password every time you run `git pull`, set up an SSH key on your VPS:

1.  **Generate an SSH key** (Run on VPS):
    ```bash
    ssh-keygen -t ed25519 -C "vps@aamed"
    ```
    (Press Enter 3 times to accept defaults and empty passphrase)

2.  **Get your Public Key**:
    ```bash
    cat ~/.ssh/id_ed25519.pub
    ```
    Copy the entire output (starts with `ssh-ed25519 ...`).

3.  **Add to GitHub**:
    - Go to [GitHub Settings > SSH and GPG keys](https://github.com/settings/keys).
    - Click **New SSH key**.
    - Title: "AAMed VPS"
    - Key: Paste the copied text.
    - Click **Add SSH key**.

4.  **Switch Remote to SSH** (Run on VPS inside `/var/www/aamed`):
    ```bash
    git remote set-url origin git@github.com:tsnxf/aamed.git
    ```

Now you can run `git pull` without a password!

**Done!** Your sites should now be live.
