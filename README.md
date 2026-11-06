# 아이파베스 · Aiphabess

레큐란 대륙의 마법학교이자 대도서관, **아이파베스**의 세계관을 소개하는 정적 웹사이트.

- **세계관 책** (`site/index.html`): 책상 위의 가죽 장정 책을 한 장씩 넘겨 읽는다
- **레큐란 석간** (`site/news.html`): 세계관 속 신문 견본호
- **관광 안내** (`site/map.html`): 대도시 3단 관광 팸플릿과 지도

## 보기
`site/index.html`을 브라우저로 연다. 폰트는 Google Fonts에서 불러오므로 인터넷 연결이 필요하다.

## 수정하고 다시 만들기
Python 3.11 이상.

```
python build/build_site.py
```

`site/`의 HTML과 `site/assets/site.css`, `logo.svg`, `img/`는 이 스크립트가 만든다. 직접 고치지 말고 스크립트를 고친다.
`site/assets/book.css`, `site/assets/book.js`는 손으로 쓴 파일이라 빌드가 덮어쓰지 않는다.

내용을 고친 뒤에는 `site/index.html?check`로 열어 넘치는 쪽이 없는지 확인한다.

## 폴더
| 경로 | 내용 |
|---|---|
| `build/` | 사이트 빌드 스크립트, 대도시 지도 생성기, BGM 목록 |
| `logo/` | 확정 로고(금박·단색)와 생성 코드 |
| `images/` | 퍼블릭도메인 판화 원본과 출처 `_sources.json` |
| `site/` | 완성된 웹사이트 |
| `worldbuilding/` | 세계관 진단, 대도시 설계, 용어집 (`[제안]`은 미확정) |
| `handoff_aipabes.md` | 작업 인수인계 (결정 사항, 하지 말 것, 미결) |

## 출처와 라이선스
- 삽화: Wikimedia Commons의 퍼블릭도메인 판화 (`images/_sources.json`)
- 질감: Poly Haven, ambientCG (CC0)
- 책장 넘김: [StPageFlip](https://github.com/Nodlik/StPageFlip) (MIT, `site/assets/vendor/page-flip.LICENSE.txt`)
- 글꼴: Song Myung, Gowun Batang, Diphylleia, Hahmlet, IM Fell English (SIL OFL, Google Fonts)
