from flask import render_template, request, jsonify, send_file
from .rate_limited import rate_limit
from .video_downloader import download_video
from .photo_downloder import download_photo
import os
def all_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")
@app.route("/video",methods=["GET","POST"])
def video_downloader():
    if request.method=="GET":
        return render_template("index.html")
    client_ip=request.remote_addr
    if rate_limit(client_ip):
        return jsonify(["error:rate limit exceed ,try again later"]),429
    url=request.form.get("url")
    quality = request.form.get("quality", "best")
    if not url:
        return jsonify(["no url found, try again otherwise please enter a valid url"]),400
    file_path=download_video(url,quality)
    if file_path and os.path.exists(file_path):
        return send_file(
            file_path,
            as_attachment=True,
            mimetype="video/mp4",
            download_name=os.path.basename(file_path)
        )
    else:
        return jsonify(["some error occuers to download video please retry"])
@app.route("/photo", methods=["GET", "POST"])
def photo_downloader():
    if request.method == "GET":
        return render_template("photo_downloader.html")
    
    client_ip = request.remote_addr
    if rate_limit(client_ip):
        return jsonify({"error": "rate limit exceeded, try again later"}), 429
    
    post_url = request.form.get("url")
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not post_url:
        return jsonify({"error": "No URL provided, please enter a valid Instagram post URL"}), 400
    
    file_path = download_photo(post_url, username, password)
    
    if file_path and os.path.exists(file_path):
        mimetype = "video/mp4" if file_path.endswith(".mp4") else "image/jpeg"
        return send_file(
            file_path,
            as_attachment=True,
            mimetype=mimetype,
            download_name=os.path.basename(file_path)
        )
    else:
        return jsonify({"error": "Failed to download media"}), 400
    
        
        
