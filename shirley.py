#!/usr/bin/env python3
import argparse, os, subprocess, json, requests

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_host", type=str)
    parser.add_argument("target_path", type=str)
    args = parser.parse_args()
    r = requests.get("http://%s/otaku/shirley" % args.source_host)
    database = json.loads(r.text)
    for a in database["videos"]:
        print("%i;%i;%s" % (database["videos"].index(a)+1, len(database["videos"]), a))
        if not os.path.exists(os.path.join(args.target_path, a+".avi")):
            subprocess.call(["ffmpeg", "-i", "http://%s/anime/%s/videoplayback.avi" % (args.source_host, a), "-s", "320x240", "-acodec", "libmp3lame", "-vcodec", "mpeg4", "-vtag", "XVID", "-qscale", "5", os.path.join(args.target_path, a+".avi")])
        else:
            print("found")
