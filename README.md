# ☕ Happy Herbivore Kiosk Server

Happy Herbivore 키오스크 주문 시스템의 백엔드를 담당하는 Django 서버입니다. 주문 접수, 상품 관리, 그리고 핵심 기능인 일별 매출 및 통계 분석 기능을 제공합니다.

## ✨ 주요 기능

주문 관리 시스템 (OMS): 키오스크에서 들어오는 주문을 실시간으로 접수 및 상태(Started, Ready, Completed) 관리.

상품 및 카테고리 관리: Product 및 Categorie 모델을 통한 유연한 상품 정보 관리.

핵심 데이터 분석: Order 테이블의 datetime 필드를 활용한 정확한 일별 매출 그래프 및 통계 생성. (과거 데이터 강제 입력 기능 포함!)

안전한 데이터 처리: default=timezone.now 설정을 통해 유연하고 정확한 시간 기반 데이터 관리.

## 🛠️ 개발 환경 설정

1. 전제 조건

   - Python 3.10+
   - pip, virtualenv
   - MySQL 또는 기타 관계형 데이터베이스

2. 환경 설정

```
# 1. 가상 환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 2. 필수 라이브러리 설치
pip install -r requirements.txt
# (혹은 pip install django mysqlclient pytz 등)

# 3. .env 또는 settings.py 파일에 DB 연결 정보 설정
# DATABASES = {...}
```

3. 데이터베이스 및 마이그레이션

최근 복잡한 마이그레이션 충돌을 해결했으므로, DB 테이블이 비어있다면 다음 순서로 깨끗하게 시작하는 것을 권장합니다.

```
# DB가 완전히 비어있을 경우 (테이블이 없다면)
python manage.py makemigrations
python manage.py migrate

# DB에 테이블은 있으나 데이터가 없는 경우
# (Order Status 등 필수 기본 데이터를 생성해야 합니다. 외래 키 오류 방지!)
python manage.py shell
>>> from orders.models import OrderStatus
>>> OrderStatus.objects.get_or_create(pk=1, description='Started')
>>> OrderStatus.objects.get_or_create(pk=2, description='Ready')
>>> # 필요한 기본 데이터(상품, 카테고리 등)를 생성하거나 Fixture를 로드합니다.
```

4. 서버 실행

```
python manage.py runserver
```

서버는 기본적으로 http://127.0.0.1:8000/에서 실행됩니다.

## 💡 개발 시 주의사항

- 시간대(Time Zone) 처리: settings.py에서 USE_TZ=True가 설정되어 있으며, 모든 시간 데이터는 UTC 기준으로 저장됩니다. 코드를 작성할 때는 항상 django.utils.timezone.now()를 사용하고, pytz.utc를 통해 명시적인 시간대 정보를 포함해야 합니다. (과거 데이터 입력 시 특히 중요!)

- 픽업 번호: pickup_number는 자동 증가 필드가 아닙니다. 다음 주문 시퀀스를 유지하려면 코드를 통해 현재 DB의 최대값 + 1로 설정해야 합니다. (수동 지정 시 데이터 누락 발생 가능)
