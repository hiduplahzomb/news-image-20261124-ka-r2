#!/usr/bin/env python3
"""Render entry.png: a one-page broadsheet summing up Tuesday 24 November 2026.

Run once:  python3 draw.py
Writes entry.png (1024x1024) next to this file. All artwork is drawn here;
main.py only copies the finished PNG (never renders).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
GREY = (90, 90, 86)
NAVY = (26, 42, 74)
NAVY_LIGHT = (52, 74, 116)
RULE = (40, 40, 40)
MARGIN = 36
CW = W - 2 * MARGIN  # 952


def font(name, size):
    path = "/usr/share/fonts/truetype/dejavu/" + name
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by measured pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, leading, fill=INK, align="left"):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        if align == "center":
            lx = x + (width - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, w, weight=2, fill=RULE):
    draw.rectangle([x, y, x + w, y + weight - 1], fill=fill)
    return y + weight


def kicker(draw, x, y, text, size=14, fill=NAVY):
    draw.text((x, y), text, font=SANS_B(size), fill=fill)
    return y + size + 8


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    y = 22
    y = rule(d, MARGIN, y, CW, 3)
    y += 6
    mast_size = 84
    mast = SERIF_B(mast_size)
    title = "THE WORLD HERALD"
    tw = d.textlength(title, font=mast)
    while tw > CW and mast_size > 40:
        mast_size -= 2
        mast = SERIF_B(mast_size)
        tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, y), title, font=mast, fill=INK)
    y += mast_size + 12
    y = rule(d, MARGIN, y, CW, 2)
    y += 2
    y = rule(d, MARGIN, y, CW, 1)
    y += 8
    # Dateline row
    df = SANS_B(15)
    d.text((MARGIN, y), "Tuesday, November 24, 2026", font=df, fill=INK)
    mid = "EST. 1898  •  VOL. CXXVIII — No. 328"
    mw = d.textlength(mid, font=SANS(15))
    d.text(((W - mw) / 2, y), mid, font=SANS(15), fill=GREY)
    right = "PRICE $2.50"
    rw = d.textlength(right, font=df)
    d.text((W - MARGIN - rw, y), right, font=df, fill=INK)
    y += 26
    y = rule(d, MARGIN, y, CW, 2)

    # ---- Lead story: NATO / European security ---------------------------
    y += 14
    y = kicker(d, MARGIN, y, "EUROPE  •  SECURITY", 15)
    lead_head = ("NATO SENDS AWACS TO POLAND AFTER "
                 "RUSSIAN MISSILES BREACH ITS AIRSPACE")
    hf = SERIF_B(36)
    y = draw_wrapped(d, MARGIN, y, lead_head, hf, CW, 43)
    y += 5
    deck = ("Alliance bolsters its eastern flank as a Russian drone strays into "
            "Polish skies overnight — and its chief warns Moscow may launch a "
            "nuclear-armed satellite as early as December.")
    y = draw_wrapped(d, MARGIN, y, deck, SERIF(17), CW, 23)
    y += 5
    byf = SANS(12)
    d.text((MARGIN, y), "By STAFF REPORTERS  —  BRUSSELS AND WARSAW", font=byf, fill=GREY)
    y += 24
    # Lead body, three columns
    col_w = (CW - 2 * 24) / 3
    lead_paras = [
        "BRUSSELS — NATO has authorised the forward deployment of an AWACS "
        "early-warning aircraft to Poland, alliance officials said on Monday, "
        "after three Russian Kh-101 cruise missiles crossed into Polish "
        "airspace during a mass strike on Ukraine on 20 November.",
        "The decision followed a meeting of the North Atlantic Council in "
        "Brussels. Polish Deputy Defence Minister Pawel Zalewski said Warsaw "
        "would have use of the aircraft and a stronger chance to react to "
        "threats. A Russian drone also briefly crossed into Poland overnight "
        "before it turned back east.",
        "NATO Secretary General Mark Rutte, speaking in Berlin, said Russia's "
        "war machine was running at full capacity and urged allies to sustain "
        "support for Ukraine and raise defence spending. Mr Rutte is due to "
        "meet President Donald Trump in Florida on Wednesday.",
    ]
    body_f = SERIF(13)
    lead_text = "  ".join(lead_paras)
    # Split the joined text across three columns by word count.
    words = lead_text.split()
    n = len(words)
    chunks = [words[: n // 3 + 8], words[n // 3 + 8: 2 * n // 3 + 4],
              words[2 * n // 3 + 4:]]
    y0 = y
    y_end = y0
    for i, chunk in enumerate(chunks):
        cx = MARGIN + i * (col_w + 24)
        yy = draw_wrapped(d, cx, y0, " ".join(chunk), body_f, col_w, 17.5)
        y_end = max(y_end, yy)
    y = y_end + 10
    y = rule(d, MARGIN, y, CW, 2)

    # ---- Middle row: markets (left) + sport (right) ---------------------
    y += 10
    mid_top = y
    left_w = 560
    right_x = MARGIN + left_w + 32
    right_w = W - MARGIN - right_x

    y = kicker(d, MARGIN, y, "MARKETS", 14)
    m_head = "STOCKS RALLY AS FED SIGNALS RATE CUTS; S&P 500 HITS RECORD HIGH"
    y = draw_wrapped(d, MARGIN, y, m_head, SERIF_B(23), left_w, 28)
    y += 4
    m_body = ("NEW YORK — Wall Street rallied on Monday after minutes from the "
              "Federal Reserve's latest meeting strengthened bets on an "
              "interest-rate cut in December, sending the S&P 500 up 1.2 per cent "
              "to a record close of 6,874.15. The Nasdaq gained 1.6 per cent and "
              "the Dow added 0.9 per cent, while the yield on the 10-year "
              "Treasury fell to 4.03 per cent. Brent crude eased 0.8 per cent to "
              "$61.40 a barrel and gold rose 0.4 per cent to $4,120 an ounce. In "
              "deal news, France's Sanofi agreed to buy US drugmaker Insmed for "
              "$41bn in cash, at $175 a share.")
    y = draw_wrapped(d, MARGIN, y, m_body, SERIF(13), left_w, 17.5)
    left_end = y

    y = mid_top
    y = kicker(d, right_x, y, "SPORT", 14)
    s_head = "ENGLAND LEVEL T20 SERIES WITH EIGHT-WICKET WIN OVER AUSTRALIA"
    y = draw_wrapped(d, right_x, y, s_head, SERIF_B(23), right_w, 28)
    y += 4
    s_body = ("England levelled their five-match T20 series against Australia "
              "with an eight-wicket victory in the second match, chasing down a "
              "target of 185 with room to spare. Jake Fraser-McGurk struck 27 "
              "from 13 balls for the hosts before England's chase sealed the win.")
    y = draw_wrapped(d, right_x, y, s_body, SERIF(13), right_w, 17.5)
    right_end = y

    y = max(left_end, right_end) + 10
    # Vertical divider between the two middle stories (ends at the rule below)
    d.line([(right_x - 16, mid_top), (right_x - 16, y - 1)], fill=GREY, width=1)
    y = rule(d, MARGIN, y, CW, 1)

    # ---- In brief band ----------------------------------------------------
    y += 10
    y = kicker(d, MARGIN, y, "IN BRIEF", 14)
    briefs = [
        ("WASHINGTON — ", "Democrats have secured at least 258 seats in the US "
         "House of Representatives, their largest majority since 1992."),
        ("WASHINGTON — ", "The Pentagon has delayed the transfer of about 60 "
         "Patriot interceptors already allocated to Ukraine, officials said."),
        ("BERLIN — ", "Germany and Ukraine reached preliminary agreement on "
         "additional interceptor missiles ahead of winter, officials said."),
    ]
    bw = (CW - 2 * 24) / 3
    y0 = y
    y_end = y0
    for i, (lead, rest) in enumerate(briefs):
        bx = MARGIN + i * (bw + 24)
        yy = draw_wrapped(d, bx, y0, lead + rest, SERIF(12), bw, 16)
        y_end = max(y_end, yy)
    y = y_end + 10

    # ---- Bottom strip: climate --------------------------------------------
    strip_h = 104
    d.rectangle([MARGIN, y, W - MARGIN, y + strip_h], fill=NAVY)
    sy = y + 12
    sy = kicker(d, MARGIN + 18, sy, "CLIMATE", 14, fill=(168, 190, 230))
    c_head = "COP31 ENDS WITHOUT A DEAL AS 1.5°C LIMIT SLIPS AWAY"
    draw_wrapped(d, MARGIN + 18, sy, c_head, SERIF_B(23),
                 CW - 36, 28, fill=(255, 255, 255))
    sy += 30
    c_sub = ("UN climate talks in Antalya collapse after the EU and vulnerable nations "
            "reject a text with no mention of fossil fuels; global temperatures ran "
            "1.46°C above pre-industrial levels over the past year.")
    draw_wrapped(d, MARGIN + 18, sy, c_sub, SANS(13), CW - 36, 17,
                 fill=(214, 222, 238))
    y += strip_h + 8

    # ---- Footer -------------------------------------------------------------
    ff = SANS(11)
    foot = "© 2026 The World Herald  •  Printed in London  •  All stories reported on Tuesday, 24 November 2026"
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, y), foot, font=ff, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
