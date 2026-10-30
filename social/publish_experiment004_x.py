#!/usr/bin/env python3
"""One-time Experiment 004 X post with verified results and original OAuth path."""
import io,os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from requests_oauthlib import OAuth1Session
def graphic():
    im=Image.new("RGB",(1200,675),"#0b2038");d=ImageDraw.Draw(im)
    base="/usr/share/fonts/truetype/dejavu/"
    def font(size,bold=False):return ImageFont.truetype(base+("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),size)
    d.text((54,38),"COOPERATIVE TRAFFIC RESEARCH  /  EXPERIMENT 004",font=font(22,True),fill="#85cfff")
    d.text((54,92),"Better predictions. Worse traffic.",font=font(43,True),fill="white")
    d.text((54,171),"Controlled SUMO simulation  |  120 scenario-arm runs  |  3 congestion regimes",font=font(20),fill="#c4d8e8")
    d.rounded_rectangle((48,229,565,474),radius=20,fill="#143953")
    d.rounded_rectangle((588,229,1152,474),radius=20,fill="#143953")
    d.text((76,255),"EXPERIMENT 003",font=font(22,True),fill="#8fdcf1")
    d.text((76,308),"34.2%",font=font(74,True),fill="#55d1a7")
    d.text((76,410),"less timing prediction error",font=font(22),fill="white")
    d.text((615,255),"EXPERIMENT 004",font=font(22,True),fill="#8fdcf1")
    d.text((615,308),"+18.53s",font=font(70,True),fill="#ff9b75")
    d.text((615,410),"longer average trips",font=font(22),fill="white")
    d.text((54,509),"High congestion  |  Calibrated cooperative routing vs. same adapter without calibration",font=font(19),fill="#d4e5f2")
    d.line((54,560,1146,560),fill="#51708b",width=2)
    d.text((54,582),"NO-GO for tested policy. Broader cooperation hypothesis remains open.",font=font(21,True),fill="#f5c4a9")
    d.text((54,630),"github.com/yonnastgetahun/cooperative_traffic_research",font=font(17),fill="#8fdcf1")
    output=io.BytesIO();im.save(output,format="PNG");return output.getvalue()
def main():
    text=Path("social/experiment004-x-post.txt").read_text().strip()
    if len(text)>280:raise SystemExit("Post exceeds 280 characters")
    names=("X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET")
    if any(not os.environ.get(n) for n in names):raise SystemExit("Missing X OAuth secret")
    s=OAuth1Session(os.environ["X_API_KEY"],client_secret=os.environ["X_API_SECRET"],resource_owner_key=os.environ["X_ACCESS_TOKEN"],resource_owner_secret=os.environ["X_ACCESS_TOKEN_SECRET"])
    media=s.post("https://upload.twitter.com/1.1/media/upload.json",files={"media":("experiment004-results.png",graphic(),"image/png")},timeout=60)
    if not media.ok:raise SystemExit(f"Media upload failed: HTTP {media.status_code}")
    media_id=media.json()["media_id_string"]
    result=s.post("https://api.x.com/2/tweets",json={"text":text,"media":{"media_ids":[media_id]}},timeout=40)
    if not result.ok:raise SystemExit(f"X publication failed: HTTP {result.status_code}: {result.text[:250]}")
    print("Published https://x.com/yonnastgetahun/status/"+str(result.json()["data"]["id"]))
if __name__=="__main__":main()
