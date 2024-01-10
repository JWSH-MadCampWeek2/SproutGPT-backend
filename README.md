# Sprout GPT

![2.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/f6cb388f-3934-47d6-9928-26d2e10eb0fc/067f0828-0849-4c57-82b4-de735a04c247/2.png)

# Sprout GPT

## 운동 새싹들을 위한 GPT 기반 운동 추천앱

---

- Kakao SDK를 이용하여 카카오 로그인이 가능합니다.
- Langchain을 통해 불러온 openai의 Chat model로 사용자의 상황에 맞는 운동 추천이 가능합니다.
- 사용자의 운동 기록을 기반으로 캘린더에 잔디를 심고, 자체 로직을 통해 커뮤니티 내의 자신의 랭킹을 확인할 수 있습니다.

---

### a. 개발 팀원

Madcamp Week2 1분반

- 서재원 - 한양대학교 컴퓨터소프트웨어학부 22학번
- 안시현 - KAIST 전기및전자공학부 20학번

---

### b. 개발 환경

- Language : React Native, Flask
- DB : MongoDB
- OS : Ios , Android
- IDE : Visual Studio Code

---

### c. 어플리케이션 소개

### Login
![login](https://github.com/JWSH-MadCampWeek2/week2-frontend/assets/79096116/8725ede8-fb08-4462-91ff-49cb08d2aaa0)


### Major Features

- 로그인 하기 버튼을 누르면 kakao 로그인 창으로 넘어갑니다.
- 로그인 과정을 거치면 앱으로 이동합니다.

### 기술 설명

- kakao서버와의 통신으로 autorization_code를 받습니다.
- autorization_code를 Kakao 서버에 보내 access_token을 받고, 이를 다시 Kakao 서버에 보내 U를 받습니다. 받은 User_info를 DB내에 저장합니다.

### Info
![info](https://github.com/JWSH-MadCampWeek2/week2-frontend/assets/79096116/a6520e6e-83a3-4f1b-81e5-ad7195a8a779)

### Major Features

- 앱의 초기 화면에서 운동 추천을 위해 필요한 정보인 나이, 성별, 키, 몸무게, 운동 목표등을 입력 받습니다.

### 기술 설명

- 사용자의 정보를 입력받아 DB에 저장합니다. 이때 이미 DB에 저장된 사용자에게는 사용자 정보가 update 됩니다.
- 운동 목표는 DB의 다른 collection으로 따로 관리됩니다.이때도 마찬가지로 이미 저장된 사용자에게는 운동 목표가 update 됩니다.

### recommend

![recommend](https://github.com/JWSH-MadCampWeek2/week2-frontend/assets/79096116/cd1cb70d-ec57-4e79-8abd-79a73d6fcfe7)

### Major Features

- 추천 버튼을 누르면 운동 추천을 시작합니다.
- 추천이 완료될 때까지 로딩창을 보여줍니다.
- 추천이 완료되면, FlatList로 추천 운동을 보여줍니다.
- 추천운동 탭을 클릭하면 comment창으로 넘어갑니다.
- comment창에서는 Sprout GPT가 운동을 추천해준 이유와 유의사항등을 comment로 보여줍니다.
- 링크버튼를 클릭하면, 해당 운동의 유튜브 링크로 이동합니다.
- 운동을 다시 추천받거나 운동목표를 재설정할 수 있습니다.

### 기술 설명

- langchain을 통해 chat model을 불러옵니다.
- DB에 저장된 많은 운동들을 사용자 정보와 함께 chat model의 prompt로 넘겨줍니다.
- chat model가 추천해준 운동과, 이에 대한 comment 받아 화면에 보여줍니다.
- 운동 목표를 재설정하면 재설정한 정보가 DB에 update되고, 이를 운동을 재추천받을 수 있습니다.

### Grass

![grass](https://github.com/JWSH-MadCampWeek2/week2-frontend/assets/79096116/5ca1fe93-a7b8-4373-9502-63dc27506e44)

### Major Features

- 오늘한 운동을 기록할 수 있습니다.
- 기록한 운동은 calendar에서 해당 날짜에 반영됩니다. 운동한 시간이 많아질수록 날짜의 색깔이 짙어집니다. 이를 잔디를 심는것에 비유하겠습니다.
- 캘린더에 다른 날을 클릭하면, 그날에 했었던 운동이 나타납니다.

### 기술 설명

- 운동 정보를 date형식으로 캘린더에 보여줍니다.
- 운동을 기록하면, 기록한 정보를 DB에 저장합니다. 정보는 사용자,운동 날짜별로 저장됩니다.
- 다른 날짜를 클릭하면, DB에서 해당 날짜의 정보를 불러옵니다.

### Ranking

![ranking](https://github.com/JWSH-MadCampWeek2/week2-frontend/assets/79096116/d92b5e35-f2dc-4bf9-bbdf-2401ff2b968f)

### Major Features

- 그 달의 전체 사용자들의 이름과, 그 달의 운동 점수를 점수가 높은사람부터로 FlatList로 보여줍니다.

### 기술 설명

- 사용자들의 랭킹을 FlatList로 보여줍니다.
- 사용자별로 기록된 운동기록을 DB에서 참조해서 사용자별로 그달의 운동 score를 계산합니다.
- score는 사용자가 얼마나 운동을 많이했는지, 얼마나 꾸준히 운동을 했는지를 반영하도록 계산됩니다.
- 사용자별로 score를 DB에 저장할때 score를 내림차순으로 sort해서 저장합니다.

### Setting

![setting](https://github.com/JWSH-MadCampWeek2/week2-frontend/assets/79096116/83ad8ed8-1c61-40b2-8e68-90dd7c8a1d03)

### Major Features

- 사용자정보를 수정할 수 있습니다.
- 로그아웃을 할 수 있습니다.

### 기술 설명

- 사용자정보를 수정하면, 이를 DB에 반영하도록 구현했습니다.
