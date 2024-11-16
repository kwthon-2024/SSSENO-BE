# 광평

# **🏫 광운대 종합 평가 서비스 🏫**

![KakaoTalk_Photo_2024-11-16-16-24-48](https://github.com/user-attachments/assets/1c615935-3870-4cc3-afc7-54b8f44829fb)


사이트 도메인: [**https://kwangpyung.kro.kr**](https://kwangpyung.kro.kr/)

Kwthon 2024 : 광운대학교 동아리 연합 해커톤

## 🔎 Pain Point(문제점)

![KakaoTalk_Photo_2024-11-16-16-19-41](https://github.com/user-attachments/assets/a2b8c499-8f85-42d1-9ad4-738502f906c9)
![KakaoTalk_Photo_2024-11-16-16-19-43](https://github.com/user-attachments/assets/d676b8e9-4df9-4519-9ca1-d95b7db91c8f)
![KakaoTalk_Photo_2024-11-16-16-19-44](https://github.com/user-attachments/assets/a0aa42cc-87b5-4fe4-8719-0d142a89f8d4)

1) 기존 게시판의 문제
   * 사람들이 잘 모른다
   * 로그인을 해야만 조회가 가능하다.
   * 인지도가 많이 부족하고, 로그인을 해야만 서비스 이용이 가능하다.

2) 장소대여의 문제
   * 각 건물마다 예약 시스템이 다름.
   * 예약이 얼마나 되어있는지 알 수 없다.
   * 단과대별 강의실 대여 기준이 다름.
   * 각 강의실 수용인원이나 설비를 모름.
   
3) 교수 정보에 대한 문제
   * 교수님의 공개정보를 찾기 어려움.
   * 각 교수님별 수업 스타일을 알기 힘듦.


## ✓ 해결책 (Solution)
   * 간편화된 청원 게시판 제작 - /kwsmg
   * 교수정보/스타일 조회 서비스 제작 - /kwpr
   * 강의실 정보 조회 서비스 제작 - /kwopgg


## 🗒️ 서비스 특징

![KakaoTalk_Photo_2024-11-16-16-38-08](https://github.com/user-attachments/assets/f1fd12a6-29eb-4197-9265-2d7aa745e198)

![KakaoTalk_Photo_2024-11-16-16-38-10](https://github.com/user-attachments/assets/b6daa817-3912-449c-a3fa-c2feddc47a06)

![KakaoTalk_Photo_2024-11-16-16-38-11](https://github.com/user-attachments/assets/172444d3-2a8a-4182-a43a-300c28740540)

![KakaoTalk_Photo_2024-11-16-16-38-13](https://github.com/user-attachments/assets/d7e73ee2-4cf1-43aa-b408-a8aea74df23e)

![KakaoTalk_Photo_2024-11-16-16-50-18](https://github.com/user-attachments/assets/237ecc7a-989c-4419-a373-fe127ae82933)

![KakaoTalk_Photo_2024-11-16-16-50-23](https://github.com/user-attachments/assets/def7800f-4e3c-479f-b0c9-3d2634ca6c25)

![KakaoTalk_Photo_2024-11-16-16-50-25](https://github.com/user-attachments/assets/62de71aa-90aa-418a-8ca9-efbba18cd096)

![KakaoTalk_Photo_2024-11-16-16-50-29](https://github.com/user-attachments/assets/dde327e5-9585-43a2-966c-56a602a11faa)


## **📜 아키텍쳐(Architecture)**

![KakaoTalk_Photo_2024-11-16-16-27-14](https://github.com/user-attachments/assets/e31f2b89-c7a3-45c0-889e-02b6d93b5d1a)

## 💾 ERD

<img width="808" alt="erd" src="https://github.com/user-attachments/assets/f5ae3d1e-47de-408b-9966-67823b895d43">

## 📢 API 

#### 🚨 청원게시판(kwsmg)

| Method | Endpoint                  | Description                                   |
|--------|---------------------------|-----------------------------------------------|
| POST    | `/petition/complaint/add`  | 청원을 접수(이하, 생성)하는 기능입니다. |
| POST   | `/petition/complaint/delete`  | 작성한 청원을 삭제하는 기능입니다.             |
| PUT    | `/petition/complaint/modify`  | 작성한 청원을 수정하는 기능입니다.              |
| POST | `/petition/complaint/read`  | 청원을 조회하는 기능입니다.                   |
| GET    | `/petition/complaint/detail`  | 청원의 세부정보를 조회하는 기능입니다. |
| POST   | `/petition/complaint/search`  | 청원을 검색하는 기능입니다.             |
| PUT    | `/petition/complaint/gachu`  | 특정 청원을 추천하는 기능입니다.              |
| PUT | `/petition/answer/modify`  | 작성한 청원에 대한 답변을 하는 기능입니다.                   |

#### 🧑‍🏫 교수 평가(kwpr)

| Method | Endpoint                  | Description                                   |
|--------|---------------------------|-----------------------------------------------|
| POST    | `/total/professor/search`  | 교수님을 검색하는 기능입니다. |
| PUT   | `/total/professor/evaluate`  | 교수님을 평가하는 기능입니다.             |
| GET    | `/total/professor/detail`  | 교수님의 세부정보를 검색하는 기능입니다.               |
| POST | `/total/professor/add`  | 교수님 및 교수님 정보를 추가하는 기능입니다.                   |
| DELETE    | `total/professor/delete`  | 교수님 및 교수님 정보를 삭제하는 기능입니다. |
| PUT   | `/total/professor/modify`  | 교수님 및 교수님 정보를 수정하는 기능입니다.             |
| POST    | `/total/lecture/search`  | 과목단위로 강의를 검색하는 기능입니다.              |


#### ✓ 강의실 평가(kwopgg)

| Method | Endpoint                  | Description                                   |
|--------|---------------------------|-----------------------------------------------|
| POST    | `/classroom/room/search`  | 강의실을 검색하는 기능입니다. |
| POST   | `/classroom/room/filter`  | 강의실의 특정조건으로 검색하는 기능입니다.             |
| POST    | `/classroom/room/list`  | 등록된 강의실을 조회하는 기능입니다.               |
| POST | `/classroom/room/detail`  | 강의실의 특정 조건을 조회하는 기능입니다.                   |
| POST    | `/classroom/room/create`  |강의실을 생성하는 기능입니다. |
| PUT   | `/classroom/room/update`  | 강의실을 수정하는 기능입니다.            |
| DELETE    | `/classroom/room/delete`  | 강의실을 삭제하는 기능입니다.              |
| POST   | `/classroom/room/detail-page`  | 강의실의 상세 조건을 조회하는 기능입니다.            |
| POST    | `/classroom/room/review`  | 강의실의 평을 조회하는 기능입니다.              |
| POST    | `/classroom/room/review/create`  | 강의실의 평가를 추가하는 기능입니다.              |
| PUT   | `/classroom/room/review/update`  | 강의실의 평가를 수정하는 기능입니다.            |

#### 💾 로그인/회원가입 관련 (kwopgg)

| Method | Endpoint                  | Description                                   |
|--------|---------------------------|-----------------------------------------------|
| POST    | `/api/authenticate`  | Klas에서 사용자의 정보를 반환하여 회원가입 및 로그인하는 기능입니다. |




## 🖥️ 기술 스택

- 프론트 파트(Front part): react, Figma
- 백엔드 파트(Backend part): Django, Mysql
- 배포(Deployment): Amazon Cloud AWS, Nginx, Github Actions
- 이 외(Other): Figma, Notion

## **📌** 깃허브 주소
- 프론트 레포지토리(Frontend Repository): [https://github.com/kwthon/SSSENO-FE](https://github.com/kwthon-2024/SSSENO-FE)
- 백엔드(Django) 레포지토리(Backend(Django) Repository): [https://github.com/kwthon-2024/SSSENO-BE](https://github.com/kwthon-2024/SSSENO-BE)


## 😎 Team
|                                                           [이주석](https://github.com/DDuckyee)                                                           |                           [유아름](https://github.com/yooaknow)                           |                           [최세인](https://github.com/sein12)                           |                         [장원준](https://github.com/jangwonjun)                          |                                                      [송희수](https://github.com/DSdevsong)                                                      |                          [이정우](https://github.com/wjddn4502)                          |
|:----------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------:|
| <img width = "300" src ="https://avatars.githubusercontent.com/DDuckyee"> | <img width = "300" src ="https://avatars.githubusercontent.com/yooaknow"> | <img width = "300" src ="https://avatars.githubusercontent.com/sein12"> | <img width = "300" src ="https://avatars.githubusercontent.com/jangwonjun"> | <img width = "300" src ="https://avatars.githubusercontent.com/DSdevsong"> | <img width = "300" src ="https://avatars.githubusercontent.com/wjddn4502"> |
|                                                               Project Manager                                                                 |                                  Frontend Developer                                  |                                  Fronted Developer                                   |                                  Backend Developer CI/CD                                 |                                                               Backend Developer                                                                |                                  Backend Developer                                   |

