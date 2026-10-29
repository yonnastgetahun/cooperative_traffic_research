#!/usr/bin/env python3
"""Publish M3 evidence graphic and approved text through existing X OAuth credentials."""
import os,sys,io
from PIL import Image,ImageDraw,ImageFont
from requests_oauthlib import OAuth1Session

DEFAULT="We checked the predictions behind our slower cooperative routing results. Across 30 held-out SUMO simulations, time-aware forecasts cut road-entry timing error by 9–20% vs. free-flow estimates. But systematic timing bias remains. Next: diagnose and recalibrate. https://github.com/yonnastgetahun/cooperative_traffic_research"
VALUES=[(200,5.323933,9.2),(600,3.865924,16.9),(1200,3.444368,20.5)]
def graphic():
    im=Image.new("RGB",(1200,675),"#0b2038")
    d=ImageDraw.Draw(im)
    reg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    bold="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    f=lambda size,b=False:ImageFont.truetype(bold if b else reg,size)
    d.text((55,42),"COOPERATIVE TRAFFIC RESEARCH  /  M3 HELD-OUT",font=f(23,True),fill="#91d8ff")
    d.text((55,96),"Better predictions. Unresolved bias.",font=f(46,True),fill="white")
    d.text((55,165),"Reduction in road-entry timing MAE vs. free-flow baseline",font=f(24),fill="#d4e5f2")
    for i,(w,val,pct) in enumerate(VALUES):
        y=242+i*105
        d.text((55,y+5),f"{w:,}s window",font=f(25,True),fill="white")
        d.rounded_rectangle((300,y,960,y+52),radius=12,fill="#294862")
        d.rounded_rectangle((300,y,300+int(660*val/6),y+52),radius=12,fill=["#147ac8","#36a7db","#70c7ea"][i])
        d.text((987,y+5),f"{val:.2f}s",font=f(26,True),fill="white")
        d.text((1080,y+35),f"{pct:.1f}%",font=f(17),fill="#a8d5ee")
    d.line((55,563,1145,563),fill="#5a7892",width=2)
    d.text((55,582),"10 independent seeds  |  30 scenarios  |  fixed synthetic SUMO network",font=f(21),fill="#d4e5f2")
    d.text((55,622),"Timing bias remains. Improved accuracy is not proven network-wide benefit.",font=f(19),fill="#f3bd80")
    b=io.BytesIO();im.save(b,format="PNG");return b.getvalue()
def main():
    post=os.environ.get("POST_TEXT","").strip() or DEFAULT
    if len(post)>280:sys.exit(f"X text exceeds 280 characters: {len(post)}")
    keys=["X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET"]
    if any(not os.environ.get(k) for k in keys):sys.exit("Missing X OAuth secrets")
    session=OAuth1Session(os.environ["X_API_KEY"],client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],resource_owner_secret=os.environ["X_ACCESS_TOKEN_SECRET"])
    image=graphic()
    upload=session.post("https://upload.twitter.com/1.1/media/upload.json",
        files={"media":("m3-heldout-results.png",image,"image/png")},timeout=60)
    if not upload.ok:sys.exit(f"X media upload failed: HTTP {upload.status_code} {upload.text[:300]}")
    media_id=upload.json().get("media_id_string")
    if not media_id:sys.exit("No media ID returned; tweet not attempted")
    response=session.post("https://api.x.com/2/tweets",json={"text":post,"media":{"media_ids":[media_id]}},timeout=40)
    if not response.ok:sys.exit(f"X tweet failed: HTTP {response.status_code} {response.text[:300]}")
    tweet_id=response.json().get("data",{}).get("id")
    if not tweet_id:sys.exit("No tweet ID returned")
    print("Published: https://x.com/yonnastgetahun/status/"+str(tweet_id))
if __name__=="__main__":main()
