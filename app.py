
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, 
    get_jwt_identity, jwt_required,
    set_access_cookies, set_refresh_cookies, 
    unset_jwt_cookies, create_refresh_token,
    # jwt_refresh_token_required,
)
from config import CLIENT_ID, REDIRECT_URI
from controller import Oauth
from model import UserModel, UserData


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['JWT_SECRET_KEY'] = "I'M IML."
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 30
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 100
jwt = JWTManager(app)


@app.route("/",methods=['POST'])
def index():
    data = request.get_json()
    code = data.get('code') 
    print(code)
    return render_template('index.html')


@app.route("/oauth", methods=['POST'])
def oauth_api():
    data = request.get_json()
    code = data.get('code')  # 'code' 키로 인가 코드를 받음
    
    # Kakao OAuth 처리 로직
    oauth = Oauth()
    auth_info = oauth.auth(code)
    user_info = oauth.userinfo("Bearer " + auth_info['access_token'])
    
    # 사용자 데이터 처리
    user_data = UserData(user_info)
    UserModel().upsert_user(user_data)
    
    # 사용자 식별 id로 서비스 전용 access_token 생성
    access_token = create_access_token(identity=user_data.id)
    refresh_token = create_refresh_token(identity=user_data.id)
    
    # 프론트엔드로 응답을 전송
    response_data = {
        'access_token': access_token,
        'user_info': user_info
    }
    
    return jsonify(response_data)


@app.route('/token/refresh',methods=['POST'])
@jwt_required(refresh=True)
def token_refresh_api():
    """
    Refresh Token을 이용한 Access Token 재발급
    """
    user_id = get_jwt_identity()
    resp = jsonify({'result': True})
    access_token = create_access_token(identity=user_id)
    set_access_cookies(resp, access_token)
    return resp


@app.route('/token/remove')
def token_remove_api():
    """
    Cookie에 등록된 Token 제거
    """
    resp = jsonify({'result': True})
    unset_jwt_cookies(resp)
    resp.delete_cookie('logined')
    return resp


@app.route("/userinfo")
@jwt_required
def userinfo():
    """
    Access Token을 이용한 DB에 저장된 사용자 정보 가져오기
    """
    user_id = get_jwt_identity()
    userinfo = UserModel().get_user(user_id).serialize()
    print(userinfo)
    return jsonify(userinfo)


@app.route('/oauth/url')
def oauth_url_api():
    """
    Kakao OAuth URL 가져오기
    """
    return jsonify(
        kakao_oauth_url="https://kauth.kakao.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code" \
        % (CLIENT_ID, REDIRECT_URI)
    )


@app.route("/oauth/refresh", methods=['POST'])
def oauth_refesh_api():
    """
    # OAuth Refresh API
    refresh token을 인자로 받은 후,
    kakao에서 access_token 및 refresh_token을 재발급.
    (% refresh token의 경우, 
    유효기간이 1달 이상일 경우 결과에서 제외됨)
    """
    refresh_token = request.get_json()['refresh_token']
    result = Oauth().refresh(refresh_token)
    return jsonify(result)


@app.route("/oauth/userinfo", methods=['POST'])
def oauth_userinfo_api():
    """
    # OAuth Userinfo API
    kakao access token을 인자로 받은 후,
    kakao에서 해당 유저의 실제 Userinfo를 가져옴
    """
    access_token = request.get_json()['access_token']
    result = Oauth().userinfo("Bearer " + access_token)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host = "143.248.219.4", port = 8080)