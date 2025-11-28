import time
import random
from mattermostdriver import Driver

# ==========================================
# [설정 구간]
# ==========================================

SERVER_URL = 'meeting.ssafy.com'
# [주의] 로그인용 새 토큰을 넣어주세요

# 달고 싶은 이모지 리스트
EMOJI_LIST = ['taco', 'kkh_clones', 'cute_taco', 'hangyotaco', 'kkh_taco_eat', 'kkh_taco_evolution', 'egen_taco', 'kkh_5taco', 'tacoblin', 'kkh_double', 'kkh_four', 'kkh_eight', 'kkh_seven', 'kkh_six', 'kkh_two', 'kkh_sleep2', 'kkh_sleep', 'kkh_three', 'kkh_positive', 'kkh', 'kkh_smart', 'sensitive_kkh', 'aggro_kkh', 'kkh_pet', 'kkh_yakitori', 'kkh_ani', 'kkh_lurk', 'kkh_zoom', 'kkh_goblin', 'insensitive_taco', 'taco_ddack', 'kyungho11masterintensifies', 'daekyungho', 'kyungho11mastershake']

# ==========================================

def main():
    USER_TOKEN = input("🔑 토큰(Token)을 입력해주세요: ").strip()	

    # 웹소켓 옵션 싹 다 제거하고 가장 기본 설정으로 갑니다.
    my_driver = Driver({
        'url': SERVER_URL, 
        'token': USER_TOKEN, 
        'scheme': 'https', 
        'port': 443,
        'verify': False, # REST API(로그인/이모지달기)용 인증서 무시
    })
    
    print(f"서버({SERVER_URL}) 접속 중...")
    
    try:
        my_driver.login()
        me = my_driver.users.get_user(user_id='me')
        my_id = me['id']
        print(f"✅ 로그인 성공! (계정: {me['username']})")
    except Exception as e:
        print(f"❌ 로그인 실패: {e}")
        return

    while True:
        print("\n" + "="*40)
        # 사용자에게 Post ID를 직접 입력받습니다.
        link = input("🎯 이모지를 달 Post ID를 입력하세요 (종료: q): ").strip()
        target_post_id = link.split('/')[-1]
        print(target_post_id)
        
        if target_post_id.lower() == 'q':
            print("종료합니다.")
            break
        
        if not target_post_id:
            continue

        print(f"🚀 Post ID [{target_post_id}]에 이모지 폭격 시작!")
        
        success_count = 0
	# -----------------------------------------------------
        # [핵심] 이모지 리스트를 복사해서 순서를 섞는 과정
        # -----------------------------------------------------
        target_emojis = EMOJI_LIST[:] # 원본 보존을 위해 복사본 생성
        random.shuffle(target_emojis) # 복사본을 무작위로 섞음 (Shuffle)

        for emoji in target_emojis:
            try:
                my_driver.reactions.create_reaction({
                    'user_id': my_id,
                    'post_id': target_post_id,
                    'emoji_name': emoji
                })
                print(f"  -> :{emoji}: 성공")
                success_count += 1
                time.sleep(0.1) # 너무 빠르면 서버가 놀라니까 살짝 텀
            except Exception as e:
                # 이미 달린 이모지거나, ID가 틀렸을 때
                if "Resource not found" in str(e):
                    print(f"  ❌ 실패: 잘못된 Post ID입니다.")
                    break # ID가 틀렸으니 더 시도 안 함
                else:
                    print(f"  -> :{emoji}: 이미 있거나 실패함 (Pass)")

        if success_count > 0:
            print("✨ 작업 완료!")

if __name__ == "__main__":
    main()