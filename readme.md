# opgg
## Member
### Front-end
* 문윤기
* 김기현

### Server
* 박성흠
* 강현석

### Game
* 김광현

## User
사용자 정보 데이터

데이터 명 | 타입 | 설명
------------ | ------------- | -------------
id | str | 사용자 아이디
email | str | 사용자 이메일
nickname | str | 사용자 닉네임
profile | url | 사용자 프로필 이미지 주소


## Rest API
### rest/getPost
게시글 및 기본 댓글(5개) 목록 가져옴
* GET DATA

    데이터 명 | 타입 | 설명
    ------------ | ------------- | -------------
    user_id | str | 가저올 게시글 사용자 아이디
    item_num | int | 한번에(한 페이지에) 가져올 게시글 개수 
    page | int | 가져올 페이지 번호

* REST DATA

    데이터 명 | 타입 | 설명
    ------------ | ------------- | -------------
    code | int | 요청 결과 코드 (0:정상)
    total_num | int | 전체 게시글 개수 
    total_page | int | 전체 페이지 개수
    now_page | int | 현재 페이지 번호
    data | arr({post,comment}) | 게시글 및 댓글 리스트
    
    * post DATA
    
        데이터 명 | 타입 | 설명
        ------------ | ------------- | -------------
        id | int | 게시글 고유번호
        content | str | 게시글 내용 
        date | date | 게시글 작성 내용
        
    * comment DATA
    
        데이터 명 | 타입 | 설명
        ------------ | ------------- | -------------
        content | str | 댓글 내용
        commenter | User | 댓글 작성자 
        date | date | 댓글 작성 내용
        
### rest/getComment
특정 게시글에 대한 댓글 목록 가져옴
* GET DATA

    데이터 명 | 타입 | 설명
    ------------ | ------------- | -------------
    post_id | str | 게시글 고유번호
    item_num | int | 한번에(한 페이지에) 가져올 댓글 개수 
    page | int | 가져올 페이지 번호

* REST DATA

    데이터 명 | 타입 | 설명
    ------------ | ------------- | -------------
    code | int | 요청 결과 코드 (0:정상)
    total_num | int | 전체 댓글 개수 
    total_page | int | 전체 페이지 개수
    now_page | int | 현재 페이지 번호
    data | arr({comment}) | 댓글 리스트

    * comment DATA
    
        데이터 명 | 타입 | 설명
        ------------ | ------------- | -------------
        content | str | 댓글 내용
        commenter | User | 댓글 작성자 
        date | date | 댓글 작성 내용
    
    
### rest/getUserList
키워드를 이용한 유저 목록 검색
* GET DATA

    데이터 명 | 타입 | 설명
    ------------ | ------------- | -------------
    keyword | str | 검색할 키워드

* REST DATA

    데이터 명 | 타입 | 설명
    ------------ | ------------- | -------------
    data | arr(User) | 유저 리스트
    
### rest/writePost
게시글 등록
* GET DATA

    데이터 명 | 타입 | 설명
    ------------ | ------------- | -------------
    id | str | 작성자 아이디
    token | str | 로그인 세션 토큰값
    content | str | 게시글 내용(120자 이내)

* REST DATA

    데이터 명 | 타입 | 설명
    ------------ | ------------- | -------------
    code | int | 요청 결과 코드 (0:정상)
    msg | str | 요청 결과 메시지
    
### rest/auth/login
아이디와 비밀번호를 이용한 로그인
* POST DATA

    데이터 명 | 타입 | 설명
    ------------ | ------------- | -------------
    id | str | 사용자 아이디
    pw | str | 사용자 비밀번호

* REST DATA

    데이터 명 | 타입 | 설명
    ------------ | ------------- | -------------
    code | int | 요청 결과 코드 (0:정상)
    msg | int | 에러 메시지(code가 0이 아닌경우)
    id | str | 사용자 아이디
    token | str | 사용자 세션 로그인 토큰
    
### rest/auth/logout
아이디와 비밀번호를 이용한 로그아웃
* GET/POST DATA

    없음
    
* REST DATA

    없음
    