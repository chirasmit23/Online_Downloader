# Online_Downloader
It is a web-application by which we can download different types off videos,photos of different sites!
Supports **rate limiting with Redis**, **automated post downloads using Selenium**, and **video downloading using `yt_dlp`**.
HereYou can check out my application->[Online_Downloader](https://online-downloader-i7xi.onrender.com/)

## 🚀 Features

- ✅ Download  Photos and Videos
- ✅ Download videos from supported platforms (Facebook,instagram,Dailymotion)
- ✅ Rate limiting with Redis to prevent abuse
- ✅ Automated photo scraping via Selenium (headless Chrome)
- ✅ Quality selector for video downloads
- ✅ Simple HTML/CSS/JS frontend

---

## 🧑‍💻 Local Development Setup

### 1. Clone the Repository

git clone https://github.com/your-username/instagram-video-downloader.git

### 2. Open (http://127.0.0.1:10000) with browser to see the result
 ## Demo Video

https://github.com/user-attachments/assets/9fd6ee06-452d-49dc-b31f-bcd0485f76db

 ## Mobile_responsive

<img src="https://github.com/user-attachments/assets/0458267b-c1c9-4980-81bc-e984beef763e" width="100"/>
<img src="https://github.com/user-attachments/assets/a9f9ae9b-8859-495f-bc74-7d518e30040b" width="100"/>
🧭 Future Plans
Currently, this tool occasionally fails to download Instagram videos or posts, mainly due to rate-limiting and IP bans from Instagram and other platforms.

To solve this issue and ensure more reliable downloads, the following improvements are planned:

### IP Rotation with Proxies:
Integrate a proxy purchasing system and build IP rotation logic, so that every download request comes from a fresh IP address.

### Better Error Handling:
Add more robust fallback strategies to ensure download attempts automatically retry with alternate methods when one fails.

These upgrades will make the tool more stable and production-ready for heavy or consistent usage.
