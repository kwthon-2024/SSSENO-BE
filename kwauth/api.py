import requests
from ninja import Router
from kwauth.schemas import UserAuthenticationRequestSchema
from kwauth.models import User
from ninja import NinjaAPI

api4 = NinjaAPI(urls_namespace="kwauth_api")

EXTERNAL_API_URL = "https://klas.kw.ac.kr/ext/out/SelectFindAllList.do"

@api4.post("/authenticate")
def authenticate(request, data: UserAuthenticationRequestSchema):
    try:
        response = requests.post(
            EXTERNAL_API_URL,
            json={"name": data.name, "birthday": data.birthday}  # API에 전달할 데이터
        )
        if response.status_code != 200:
            return {"status": "error", "message": "외부 API 호출 실패", "details": response.text}
    except requests.RequestException as e:
        return {"status": "error", "message": "외부 API 호출 중 오류 발생", "details": str(e)}

    external_data = response.json()
    if isinstance(external_data, list) and len(external_data) > 0:
        external_data = external_data[0]  # 첫 번째 요소 사용
    else:
        return {"status": "error", "message": "외부 API에서 적절한 데이터를 찾을 수 없음"}

    if (
            data.gubun != external_data.get("gubun")
            or data.codeName1 != external_data.get("codeName1")
            or data.sex != external_data.get("sex")
            or data.hakbun != external_data.get("hakbun")
    ):
        return {"status": "error", "message": "추가 인증 실패"}

    user, created = User.objects.get_or_create(
        name=data.name,
        birthday=data.birthday,
        defaults={
            "gubun": external_data.get("gubun"),
            "code_name1": external_data.get("codeName1"),
            "sex": external_data.get("sex"),
            "hakbun": external_data.get("hakbun"),
        },
    )

    if not created:
        return {
            "status": "success",
            "message": "인증 성공: 기존 사용자",
            "details": {
                "user_id": user.user_id,
                "gubun": external_data.get("gubun"),
                "codeName1": external_data.get("codeName1"),
                "sex": external_data.get("sex"),
                "hakbun": external_data.get("hakbun"),
            },
        }

    return {
        "status": "success",
        "message": "인증 성공: 새 사용자 추가",
        "details": {
            "user_id": user.user_id,
            "gubun": external_data.get("gubun"),
            "codeName1": external_data.get("codeName1"),
            "sex": external_data.get("sex"),
            "hakbun": external_data.get("hakbun"),
        },
    }
