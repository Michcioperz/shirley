#!/usr/bin/env python3
import argparse, os, subprocess, json, requests, re, string

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_host", type=str)
    parser.add_argument("target_path", type=str)
    args = parser.parse_args()
    print("Now, what do we have here?")
    r = requests.get("http://%s/otaku/shirley" % args.source_host)
    database = json.loads(r.text)
    print("I see %i series with a total of %i episodes" % (len(database["series"]), len(database["videos"])))
    for a in database["series"]:
        print("Let's look for some %s" % a)
        r = requests.get("http://%s/otaku/api/series/%s/find" % (args.source_host, a))
        av = json.loads(r.text)
        print("There are %i episodes of it on the server" % len(av["videos"]))
        avd = os.path.join(args.target_path, "".join([x if x in frozenset(string.ascii_letters+string.digits) else "" for x in a]))
        if len(av["videos"]) > 0 and not os.path.exists(avd):
            os.mkdir(avd)
        for avi in av["videos"]:
            print("Maybe %s?" % avi)
            if not os.path.exists(os.path.join(avd, avi+".avi")):
                subprocess.call(["ffmpeg", "-hide_banner", "-i", "http://%s/anime/%s/videoplayback.avi" % (args.source_host, avi), "-s", "320x240", "-acodec", "libmp3lame", "-vcodec", "mpeg4", "-vtag", "XVID", "-qscale", "5", os.path.join(avd, avi+".avi")])
                print("Okay, what else...")
            else:
                print("Aha, it's already there.")
    print("Okay, I think it's done, bye.")
