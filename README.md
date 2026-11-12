# 아이파베스 · Aiphabess

레큐란 대륙의 마법학교이자 대도서관, **아이파베스**의 세계관을 소개하는 정적 웹사이트.

- **세계관 책** (`docs/index.html`): 책상 위의 3D 가죽 장정 책을 한 장씩 넘겨 읽는다 (DearFlip)
- **레큐란 석간** (`docs/news.html`): 세계관 속 신문 견본호
- **관광 안내** (`docs/map.html`): 대도시 3단 관광 팸플릿과 지도

## 보기
온라인: https://bowwow-wangwang.github.io/schoolproject/ (GitHub Pages, `main` 브랜치의 `docs/` 폴더)

로컬: 3D 책은 파일을 바로 열면 책장 이미지가 막히므로 간단한 서버로 연다.

```
cd docs
python -m http.server 8000
```

그다음 `http://localhost:8000/` 을 연다. 주소 끝에 `?page=10`을 붙이면 그 쪽이 바로 열린다. 폰트는 Google Fonts에서 불러오므로 인터넷 연결이 필요하다.

## 수정하고 다시 만들기
Python 3.11 이상, Pillow, Google Chrome.

```
python build/build_site.py      # HTML 생성
python build/render_pages.py    # 책장 32쪽을 이미지로 다시 찍기 (책 내용을 고쳤을 때)
```

3D 책의 쪽은 `docs/book-source.html`(평면 책 원본)을 한 쪽씩 찍은 이미지(`docs/assets/pages/`)다. 책 내용을 고치면 두 명령을 모두 실행한다. 크롬이 기본 위치에 없으면 `CHROME` 환경 변수로 경로를 지정한다.

`docs/`의 HTML과 `docs/assets/site.css`, `logo.svg`, `img/`는 이 스크립트가 만든다. 직접 고치지 말고 스크립트를 고친다.
`docs/assets/book.css`, `docs/assets/book.js`는 손으로 쓴 파일이라 빌드가 덮어쓰지 않는다.

내용을 고친 뒤에는 `docs/book-source.html?check`로 열어 넘치는 쪽이 없는지 확인한다.

## 폴더
| 경로 | 내용 |
|---|---|
| `build/` | 사이트 빌드 스크립트, 대도시 지도 생성기, BGM 목록 |
| `logo/` | 확정 로고(금박·단색), 책 표지용 문장(마름모+A), 생성 코드 |
| `images/` | 퍼블릭도메인 판화 원본과 출처 `_sources.json` |
| `docs/` | 완성된 웹사이트 (GitHub Pages가 이 폴더를 그대로 공개) |
| `worldbuilding/` | 세계관 진단, 대도시 설계, 용어집 (`[제안]`은 미확정) |
| `handoff_aipabes.md` | 작업 인수인계 (결정 사항, 하지 말 것, 미결) |

## 출처와 라이선스
- 삽화: Wikimedia Commons의 퍼블릭도메인 판화 (`images/_sources.json`)
- 질감: Poly Haven, ambientCG (CC0)
- 3D 책: [DearFlip Lite](https://github.com/dearhive/dearflip-js-flipbook) (CC BY-NC-ND 4.0, 비영리 개인 사용만 가능, 원본 그대로 `docs/assets/vendor/dflip/`)
- 평면 책 원본의 책장 넘김: [StPageFlip](https://github.com/Nodlik/StPageFlip) (MIT)
- 글꼴: Song Myung, Gowun Batang, Diphylleia, Hahmlet, IM Fell English (SIL OFL, Google Fonts)
