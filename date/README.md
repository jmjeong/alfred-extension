## date ([Download](https://raw.github.com/jmjeong/alfred-extension/master/date/date.alfredworkflow))

오늘의 양력, 음력 날짜 출력과 양력, 음력 변환하는 workflow

![Screenshot](https://raw.github.com/jmjeong/alfred-extension/master/date/screenshot.png)

###  Usage

```
 date                 :: 오늘의 양력, 음력을 출력            
 date 1/1             :: 양력 2013년 1월 1일을 음력으로 변환
 date 2012/1/1        :: 양력 2012년 1월 1일을 음력으로 변환
 date -1/1            :: 음력 2013년 1월 1일을 양력으로 변환
 date -2012/3/1 leap  :: 음력 윤달 2013년 3월 1일을 양력으로 변환
```

### Version History 

#### 1.2 - October 17, 2013

- 음력변환에 오류 수정 (오타로 인한)
- 년도에 100 이하의 숫자가 들어오면 1900년대로 간주하여 계산

#### 1.1 - April 19, 2013

- Alfred 2.0.3 release 대응 : UUID를 optional 처리 

#### 1.0 - March 31, 2013

- Initial release
