# MyAnimeList-Web-Scraping

#### Setting up the chromedriver
1. Installing chrome
```
sudo apt-get update
sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb


google-chrome --version
```

2. Install chromedriver
- Find the latest chromedriver from [this list](https://googlechromelabs.github.io/chrome-for-testing/)
```
wget https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.98/linux64/chromedriver-linux64.zip

unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver

rm chromedriver-linux64.zip
rm google-chrome-stable_current_amd64.deb
rm -r chromedriver-linux64
```


