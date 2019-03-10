#!/usr/bin/env python3
import json
import os
import subprocess
from imgurpython import ImgurClient

SVG_PATH = "twemoji/svg/"
DENSITY = None

def do_init():
    global DENSITY

    auth = json.load(open("config.json"))

    # Read client ID and secret
    client_id = auth["client_id"]
    client_secret = auth["client_secret"]

    # Also read the imagemagick density
    DENSITY = auth["density"]

    # Check if there are access and refresh tokens
    access_token = None
    refresh_token = None
    if "access_token" in auth:
        access_token = auth["access_token"]

    if "refresh_token" in auth:
        refresh_token = auth["refresh_token"]

    if access_token and refresh_token:
        # If access and refresh tokens are available, just log in
        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    else:
        # Otherwise go through the authentication process
        client = ImgurClient(client_id, client_secret)

        # Get auth URL
        print("Go to: %s" % client.get_auth_url('pin'))
        print("Enter pin code: ")
        pin = input()

        credentials = client.authorize(pin, 'pin')
        client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

        print("Access token:  {0}".format(credentials['access_token']))
        print("Refresh token: {0}".format(credentials['refresh_token']))

        # Save the config back
        auth = json.load(open("config.json"))
        auth["access_token"] = credentials['access_token']
        auth["refresh_token"] = credentials['refresh_token']

        auth_cfg = open("config.json", "w")
        auth_cfg.write(json.dumps(auth, indent=4))

    return client

def do_upload(client):
    # Try loading the output json
    try:
        svg_urls = json.load(open("out.json"))
    except:
        svg_urls = {}
    # Create a folder where PNGs are stored
    os.makedirs("png", exist_ok=True)

    # Go through each SVG
    for svg in os.listdir(SVG_PATH):
        svg_name = svg.replace(".svg", "")

        # If already processed, skip it
        if svg_name in svg_urls:
            continue

        print("Processing %s" % svg)

        # Convert it from SVG to PNG
        png = "png/%s.png" % svg_name
        subprocess.run(["convert -density %s -background none %s %s" % (DENSITY, SVG_PATH + svg, png)], shell=True)

        # Upload it
        upload_json = client.upload_from_path(png)

        # Save the link
        svg_urls[svg_name] = upload_json["link"]

        # Save the JSON back
        out = open("out.json", "w")
        out.write(json.dumps(svg_urls, indent=4))

if __name__ == "__main__":
    do_upload(do_init())
