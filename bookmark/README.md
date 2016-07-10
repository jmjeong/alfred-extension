# 북마크

Browser의 북마크를 alfred로 관리하고 검색하는 workflow입니다.

[![youtube](http://img.youtube.com/vi/ImXADq0mBRM/0.jpg)](http://www.youtube.com/watch?v=ImXADq0mBRM)

단축키를 이용하여 URL을 북마킹, 태그 부여, 검색, 실행할 수 있습니다. 

pinboard.in 검색하고 관리하는
[alfred-pinboard](https://github.com/jmjeong/alfred-extension/tree/master/alfred-pinboard)를 만들어
사용하다가, 버전업을 하면서 pinboard.in 계정이 없더라도 사용할 수 있도록 확장했습니다. 

pinboard.in 계정 연동 후에는 pinboard.in에서 수정한 내용을 `pbreload` 명령을 통해 읽어올 수 있습니다. 

다음 기능을 제공합니다. 

- 북마크 등록 - safari, chrome에서 보고 있는 페이지를 hotkey로 등록 
	- 등록 시 북마크에 여러  태그를 부여할 수 있습니다
- 북마크 검색 - 부분검색 지원 
- 북마크 삭제
- 북마크마다  [private], [star] 속성을 지정할 수 있습니다 
	- 검색 시  [private], [star]로 조건을 부여할 수 있습니다. 
- 태그 별 북마크 검색
- 다양한 정렬 옵션 
	- 최근 사용
	- 자주 사용
	- 등록 순서 별 
- pinboard 연동 
	- **첫 연동 시에 pinboard 데이타로 교체되며 local 저장된 북마크는 지워집니다**
	- 연동 후에는 등록, 삭제가 pinboard와 연동하여 동작합니다. 
	- `pbreload` 명령으로 pinboard에서 내용을 local db에 반영합니다. 


### 인스톨 

Workflow를 인스톨하고 난 후, 초기화된 키 설정을 다시 합니다. 저는 다음과 같은 키 설정으로 사용합니다.

- Cmd-Shift-Ctrl-P : Workflow launch (검색 조건은 설정에 따릅니다)
- Cmd-Shift-Ctrl-K : 모든 북마크를 검색에 포함(private, mark 설정 무시)
- Cmd-Shift-Ctrl-L : Mark 설정된 북마크만 검색
- Cmd-Shift-Ctrl-; : 북마크 추가 (**브라우저가 활성화된 상태에서만 동작합니다**)

### 북마크 속성 별 검색

북마크는 private, mark 속성을 지정할 수 있습니다. 기본 검색은 private 지정되지 않는 북마크만 검색합니다. 검색 조건은 설정 메뉴에서 변경 가능합니다. 

- private : [shift] modifier로 변경할 수 있습니다. 
- star : [ctrl] modifier로 변경할 수 있습니다. 
- [태그 검색] 메뉴에서 해당 태그 속성을 가진 모든 북마크를 private, mark on/off 가능합니다. 
	- ctrl: set mark, shift: unset mark, alt: set private, cmd: unset private

### 설정 

- mark[filter] - mark 속성을 지닌 북마크를 검색에 포함시킬 것인지 지정. all - 모두 검색, on - mark 만 검색, off - mark 지정되지 않는 것만 검색 
- private[filter] - private 속성을 지닌 북마크를 검색에 포함시킬 것이지 지정. all - 모두 검색, on - private 만 검색, off - private 지정되지 않는 것만 검색 
- sort - 정렬 옵션 
	- accessed, launch_count, time - 최근 호출 booker 별 정렬 (default)
	- launch_count, accessed, time - 북마크 호출 횟수 별 정렬
	- time, accessed - 북마크 등록 순서별 정렬

### 명령어 

- bm (ctrl-shift-cmd-p) - 메인 검색. 설정의 검색 조건을 기반으로 검색합니다. 

- bm으로 구동된 후 명령어
	- ! (ctrl-shift-cmd-k) - private 지정된 북마크 도 검색에 포함 
	- \* (ctrl-shift-cmd-l) - start 지정된 북마크 만 검색 
	- \+ (ctrl-shift-cmd-;) - 웹 브라우저가 활성화 되었을 경우에만 동작합니다. 북마크 추가 단축키.
	- \# - 태그 검색. tab이나 enter 누르면 해당 태그에 속한 북마크만 검색

alfred-bookmark의 각 북마크에 다음과 같은 명령을 내릴 수 있습니다. 

- Enter : 북마크를 구동합니다
- Ctrl : mark 설정을 on/off 바꿉니다
- Shift : private 설정을 on/off 바꿉니다
- Alt : 북마크를 지웁니다
- Cmd : URL을 복사합니다

Mark, Private 설정은 tag 검색 메뉴에서 소속된 모든 북마크에 적용 가능합니다.
예를 들어 #mac tag에 포함된 북마크 모두를 private로 변경가능합니다. 
