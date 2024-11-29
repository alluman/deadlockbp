from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'nickname', 'password']
        
    # 비밀번호 
    def validate_password(self, input_password):
        # 공백 확인
        if " " in input_password:
            raise serializers.ValidationError("비밀번호에는 공백을 포함할 수 없습니다.")
        
        # 유니코드문자확인
        if not re.match(r'^[A-Za-z0-9!@#$%^&*(),.?":{}|<>]+$', input_password):
            raise serializers.ValidationError("비밀번호에 허용되지 않은 문자가 포함되어 있습니다.")
        
        # 길이확인
        if len(input_password) < 8:
            raise serializers.ValidationError("비밀번호는 8자 이상이어야 합니다.")
        
        # 영문,숫자,특수문자 포함 확인
        if not re.search(r'[A-Za-z]', input_password):
            raise serializers.ValidationError("비밀번호는 하나 이상의 영문이 포함되어야 합니다.")
        if not re.search(r'[0-9]', input_password):
            raise serializers.ValidationError("비밀번호는 하나 이상의 숫자가 포함되어야 합니다.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', input_password):
            raise serializers.ValidationError("비밀번호는 하나 이상의 특수문자가 포함되어야 합니다.")

        return input_password

    # 닉네임 검증
    def validate_nickname(self, nickname):
        # 닉네임 중복확인
        if User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError("사용중인 닉네임입니다.")
        
        # '_' 확인(steam 사용자 닉네임을 _steam 쓸거라 중복방지용)
        if '_' in nickname:
            raise serializers.ValidationError("닉네임에는 '_'를 포함할 수 없습니다.")
        
        return nickname

    def validate_username(self, username):
        # id 중복확인
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("사용중인 id입니다.")
        
        return username

    def validate_email(self, email):
        # email 중복확인
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("사용중인 email입니다.")
        
        return email

    def create(self, validated_data):
        # 비밀번호 암호화 후 저장
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)
