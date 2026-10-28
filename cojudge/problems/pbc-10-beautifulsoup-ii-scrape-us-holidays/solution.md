## Reference solution

Paste this code above the supplied tests and runner.

```python
from collections import defaultdict
import base64 as _base64
import zlib as _zlib

HTML = _zlib.decompress(_base64.b85decode('c-qZbTT|OQ5Pt8k(D;QHOmHYI?SahnKskjH=p5QIePTAY5^Ew$9!VxmfBo5&?OY0Vl6K<5OeWT4C9U?`Z>6=59SkIAu>@;R0x7HueM`WE<5_NWeiDFjB9{DbolJw?3&xIP$eqxtcZK3i57{|SxB<yN6$2?^_CZULz|>OLm)mztDAwJNj*dI^IGV$y9FnqRs)pVfOpiPGoK+oPsMktDa!+ILUw4m!-Zu_raZI)L6T=M8z>ICsJJngnm9sOM4rxF&(&*R?aG#Z8)!3c1oOK6#lU`q|as^cX1vW72rjnlolN3!B+8kp3mMJ|kkeB9iBI9hqp4Op7X>$Qf@SnO*0<uuJAK@>kCrpIRB~0Hct@vL-Z!Upr<Cxwhr~=HC`3ABjDf5((O6%7mUMFCw;X~Y+bGd!n=}ab*Jv|(Xm{)tXd$G<su`ZM|g4@nW>H)}(;*<L++T7lw%wC@6JIru-5;(1;6M4X#aHM<CyXF%{=<HbLafO~YwO`&_C3%DlHditwCcgT=pb#CdLLoZ*2?gJ<Z4?R%olK4!4c{leDt1+%LmT!{s1ds~djtYo7li|pu+qRp-g<`(&=@{KVuRd1Hr+6K(~J#CRM?#Jfhoax(-Jtj;Z`IRURDs~orD2ou*<Mu$MiJf2bz!yV^9|CE;|J&hT15Bt*2UQ1Bs@RQar|xT)16!h9TI9*oR>hDY5|xe}D-HvCA$JNO8o4ltO8NGxk9!P7gDcpb{!s3vpUl?i}@tI29vMRKiuPc0fgI>6hoCtmwi}Nh=4W@HJYw+`~10fW$v1s6&?9R2W`XFS)UNT9&_QGscoO7@f~x>=(I71!{UTmZ&kA<py0!qaL5QQg$jIz+2%~qgSI{3?iUr^?HuaoOHIFQ}H`l@QZ_Vmwn|XLuIib%t-i&?f`XDBS%ZzaXiKrx~4kAuAuj6hULyCA#9mEwF~ayejNiT(Rb0M?ek#M%P@M?%qEhk*z_(pLNZ_74wdSPXHpX5BSgEZSmZ$WhLD2)(`=f<$<9uL-us17n?ScT4ZBeiVY}meOjyQJTXGbqS#1b(y#^F>e;Zmlv~G*-L3tQP2hC8DL<MCZH{>g=99Wu8qSZHszL(qVzR*<(E3Hao!);YOW2N<3rPi~!Rvd<C)fEVJj}{Q>9<_xK&$JOBS3^_@ZgiWt0;J76BKDi%Xqh&z!svA~C?rwe^$NwAueEgD9>RLmIfu=uL+8|-I<&Pv<jx&W@c7*tQm^qaYDS7AW=Kg)j9#|HAE6SSbNo{=Uy0Slg78K>dKN+KO}M|}m?4P@g<GEEoC8cl_S-sa@LH|SDhRGfXd~N4OCfB&ujg=!i}u6)=7YscRG8evPJ2Y!I$UC(mK5tJM0FyxQOffV*LZ=4CvqO-oA7zc>g1;}wOP(#`uw|y^<q9#W-!b7%D<^jIJ>arddt~Lm7C1-j>R;DUQ?B3+sIAnIy86F8tP{dH=-zvy3IaH5|xi$>xYtFzNHN(ec+B8OuO4j+PTC8oigKd>=((R`~EU@pSkgcp5Xt-YPpY?pBC{Lz4A&I!mjJ-ZKU~+DN?5V^Ys09UI9Essg_;{e65^hBTByi9^+}j?u3oCvdGGH+4wmvjNKw1yDRzFeZ<FZTYPjWsIeW12Q+-+QT};Ba9v1VqKnklr8qg;-rA@6xe?n$=3pf<2ak|x>w-0q5RdPN-T)2AEQY~f#XAj40j`W|vv~G6h&>gx){08ANc2<u+4Obe<9M=00ND%Z!xn=f1`oFAu4{*o`S9QI+~uHBY%fELx?#8ZyNQ>mJok*pmFFI|mruv3!P{d7t264;TJn#+UR6!APl_G?akcj!;Uu2J')).decode()

from html.parser import HTMLParser as _HTMLParser

class _Element:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def find_all(self, name, class_=None):
        result = []
        for child in self.children:
            if isinstance(child, _Element):
                if child.tag == name and (class_ is None or class_ in child.attrs.get('class', '').split()):
                    result.append(child)
                result.extend(child.find_all(name, class_))
        return result

    def find(self, name, class_=None):
        return next(iter(self.find_all(name, class_)), None)

    def get(self, key, default=None):
        return self.attrs.get(key, default)

    def get_text(self, strip=False):
        text = ''.join(child.get_text() if isinstance(child, _Element) else child for child in self.children)
        return text.strip() if strip else text

    @property
    def text(self):
        return self.get_text()

class _Parser(_HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = _Element()
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = _Element(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)

def BeautifulSoup(markup, parser='html.parser'):
    """Supplied subset: find/find_all(name, class_=...), get, get_text, text.

    This is a standard-library adapter, not the third-party BeautifulSoup package.
    Use it for the well-formed tables supplied in this exercise.
    """
    document = _Parser()
    document.feed(markup)
    return document.root

def get_us_bank_holidays(html=HTML):
    holidays = defaultdict(list)
    table = BeautifulSoup(html, 'html.parser').find('table', class_='list-table')
    if table is None:
        return holidays
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        time = row.find('time')
        if len(cells) >= 4 and time is not None:
            month = time.get('datetime')[5:7]
            holidays[month].append(cells[3].get_text(strip=True))
    return holidays
```
