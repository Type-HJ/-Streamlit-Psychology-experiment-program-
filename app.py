import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import os
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="심리학 실험 프로그램",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터 디렉토리 생성
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# CSS 스타일
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .header-title {
        text-align: center;
        color: #667eea;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .stButton > button {
        width: 100%;
        padding: 0.75rem;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 0.5rem;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'participant_data' not in st.session_state:
    st.session_state.participant_data = {}
if 'experiment_type' not in st.session_state:
    st.session_state.experiment_type = None
if 'trial_data' not in st.session_state:
    st.session_state.trial_data = []
if 'current_trial' not in st.session_state:
    st.session_state.current_trial = 0
if 'settings' not in st.session_state:
    st.session_state.settings = {}

# 데이터 저장 함수
def save_data(df):
    """데이터를 CSV로 저장"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = DATA_DIR / f"experiment_{st.session_state.participant_data.get('participant_id', 'unknown')}_{timestamp}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    return filename

def load_all_data():
    """모든 저장된 데이터 로드"""
    csv_files = list(DATA_DIR.glob("*.csv"))
    if not csv_files:
        return pd.DataFrame()
    
    dfs = [pd.read_csv(f) for f in csv_files]
    return pd.concat(dfs, ignore_index=True)

# ===== 메인 화면 =====
def page_main():
    st.markdown("<h1 class='header-title'>🧠 심리학 실험 프로그램</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666;'>스트룹 과제 & 클릭 반응 테스트</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🚀 실험 시작", key="start_btn", use_container_width=True):
            st.session_state.page = 'participant_info'
            st.rerun()

# ===== 참가자 정보 입력 =====
def page_participant_info():
    st.title("참가자 정보 입력")
    
    with st.form("participant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            participant_id = st.text_input("참가자 ID *", placeholder="예: P001")
            age = st.number_input("나이 *", min_value=1, max_value=120, step=1)
        
        with col2:
            gender = st.selectbox("성별 *", ["선택하세요", "남성", "여성", "기타"])
        
        submitted = st.form_submit_button("다음", use_container_width=True)
        
        if submitted:
            if not participant_id or gender == "선택하세요":
                st.error("모든 필드를 입력해주세요.")
            else:
                st.session_state.participant_data = {
                    'participant_id': participant_id,
                    'age': age,
                    'gender': gender,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.page = 'experiment_select'
                st.rerun()

# ===== 실험 선택 =====
def page_experiment_select():
    st.title("실험 선택")
    st.write(f"참가자: **{st.session_state.participant_data['participant_id']}** (나이: {st.session_state.participant_data['age']}, 성별: {st.session_state.participant_data['gender']})")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎨 스트룹 과제", use_container_width=True, key="stroop"):
            st.session_state.experiment_type = 'Stroop'
            st.session_state.page = 'experiment_settings'
            st.rerun()
    
    with col2:
        if st.button("⚡ 클릭 반응 테스트", use_container_width=True, key="click"):
            st.session_state.experiment_type = 'Click Reaction'
            st.session_state.page = 'experiment_settings'
            st.rerun()
    
    if st.button("← 뒤로", use_container_width=True):
        st.session_state.page = 'main'
        st.rerun()

# ===== 실험 설정 =====
def page_experiment_settings():
    st.title("실험 설정")
    st.write(f"**실험 유형:** {st.session_state.experiment_type}")
    
    with st.form("settings_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            difficulty = st.selectbox("난이도", ["Easy", "Normal", "Hard"])
        
        with col2:
            reward = st.selectbox("보상", ["있음", "없음"])
        
        with col3:
            trial_count = st.number_input("시도 횟수", min_value=1, max_value=100, value=10, step=1)
        
        submitted = st.form_submit_button("실험 시작", use_container_width=True)
        
        if submitted:
            st.session_state.settings = {
                'difficulty': difficulty,
                'reward': reward == "있음",
                'trial_count': trial_count
            }
            st.session_state.trial_data = []
            st.session_state.current_trial = 0
            
            if st.session_state.experiment_type == 'Stroop':
                st.session_state.page = 'stroop_test'
            else:
                st.session_state.page = 'click_reaction_test'
            st.rerun()
    
    if st.button("← 뒤로", use_container_width=True):
        st.session_state.page = 'experiment_select'
        st.rerun()

# ===== 스트룹 과제 =====
def page_stroop_test():
    st.title("🎨 스트룹 과제")
    
    progress = st.session_state.current_trial / st.session_state.settings['trial_count']
    st.progress(progress, text=f"시도 {st.session_state.current_trial}/{st.session_state.settings['trial_count']}")
    
    if st.session_state.current_trial >= st.session_state.settings['trial_count']:
        page_results()
        return
    
    # 자극 생성
    words = ['빨강', '초록', '파랑', '노랑', '보라', '민트']
    colors_hex = {
        '빨강': '#FF0000',
        '초록': '#00AA00',
        '파랑': '#0066FF',
        '노랑': '#FFD700',
        '보라': '#9370DB',
        '민트': '#00CED1'
    }
    
    # 난이도에 따른 자극 조정
    if st.session_state.settings['difficulty'] == 'Easy':
        if np.random.random() < 0.7:
            word = np.random.choice(words)
            display_color = word
        else:
            word = np.random.choice(words)
            display_color = np.random.choice([w for w in words if w != word])
    else:
        word = np.random.choice(words)
        if st.session_state.settings['difficulty'] == 'Normal':
            if np.random.random() < 0.5:
                display_color = word
            else:
                display_color = np.random.choice([w for w in words if w != word])
        else:
            display_color = np.random.choice([w for w in words if w != word])
    
    # 자극 표시
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem; background-color: #f5f5f5; border-radius: 1rem;'>
            <div style='font-size: 4rem; font-weight: bold; color: {colors_hex[display_color]}; word-break: break-all;'>
                {word}
            </div>
            <p style='color: #999; margin-top: 1rem;'>글자의 <strong>색상</strong>을 선택하세요 (단어 의미 아님)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # 색상 버튼
    col1, col2, col3, col4 = st.columns(4)
    buttons = [
        (col1, '빨강', '#FF0000'),
        (col2, '초록', '#00AA00'),
        (col3, '파랑', '#0066FF'),
        (col4, '노랑', '#FFD700')
    ]
    
    col5, col6 = st.columns(2)
    buttons.extend([
        (col5, '보라', '#9370DB'),
        (col6, '민트', '#00CED1')
    ])
    
    start_time = time.time()
    
    for col, button_text, color in buttons:
        with col:
            if st.button(button_text, use_container_width=True, key=f"color_{button_text}"):
                reaction_time = (time.time() - start_time) * 1000
                is_correct = button_text == display_color
                
                trial_record = {
                    'participant_id': st.session_state.participant_data['participant_id'],
                    'age': st.session_state.participant_data['age'],
                    'gender': st.session_state.participant_data['gender'],
                    'date': st.session_state.participant_data['date'],
                    'experiment_type': 'Stroop',
                    'trial_number': st.session_state.current_trial + 1,
                    'stimulus_word': word,
                    'stimulus_color': display_color,
                    'correct_color': display_color,
                    'response_color': button_text,
                    'reaction_time_ms': round(reaction_time, 2),
                    'accuracy': 1 if is_correct else 0,
                    'difficulty': st.session_state.settings['difficulty'],
                    'reward': st.session_state.settings['reward']
                }
                
                st.session_state.trial_data.append(trial_record)
                st.session_state.current_trial += 1
                st.rerun()

# ===== 클릭 반응 테스트 =====
def page_click_reaction_test():
    st.title("⚡ 클릭 반응 테스트")
    
    progress = st.session_state.current_trial / st.session_state.settings['trial_count']
    st.progress(progress, text=f"시도 {st.session_state.current_trial}/{st.session_state.settings['trial_count']}")
    
    if st.session_state.current_trial >= st.session_state.settings['trial_count']:
        page_results()
        return
    
    st.write("준비하세요... 화면의 색이 녹색으로 바뀌면 최대한 빠르게 '클릭!' 버튼을 누르세요!")
    
    delay = np.random.uniform(1, 3)
    time.sleep(delay)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background-color: #90EE90; border-radius: 1rem;'>
            <div style='font-size: 2rem; color: #000;'>🟢 클릭!</div>
        </div>
        """, unsafe_allow_html=True)
    
    start_time = time.time()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🖱️ 클릭!", use_container_width=True, key="click_btn"):
            reaction_time = (time.time() - start_time) * 1000
            
            trial_record = {
                'participant_id': st.session_state.participant_data['participant_id'],
                'age': st.session_state.participant_data['age'],
                'gender': st.session_state.participant_data['gender'],
                'date': st.session_state.participant_data['date'],
                'experiment_type': 'Click Reaction',
                'trial_number': st.session_state.current_trial + 1,
                'stimulus_word': 'N/A',
                'stimulus_color': 'Green',
                'correct_color': 'N/A',
                'response_color': 'N/A',
                'reaction_time_ms': round(reaction_time, 2),
                'accuracy': 1,
                'difficulty': st.session_state.settings['difficulty'],
                'reward': st.session_state.settings['reward']
            }
            
            st.session_state.trial_data.append(trial_record)
            st.session_state.current_trial += 1
            st.rerun()

# ===== 결과 화면 =====
def page_results():
    st.title("📊 실험 완료 - 결과")
    
    if not st.session_state.trial_data:
        st.warning("데이터가 없습니다.")
        return
    
    df = pd.DataFrame(st.session_state.trial_data)
    
    valid_trials = df[df['reaction_time_ms'].notna()]
    avg_reaction_time = valid_trials['reaction_time_ms'].mean() if len(valid_trials) > 0 else 0
    accuracy = (df['accuracy'].sum() / len(df) * 100) if len(df) > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("평균 반응시간", f"{avg_reaction_time:.0f}ms")
    with col2:
        st.metric("정확도", f"{accuracy:.1f}%")
    with col3:
        st.metric("시도 횟수", len(df))
    with col4:
        st.metric("총 소요 시간", f"{valid_trials['reaction_time_ms'].sum()/1000:.1f}초")
    
    st.subheader("반응시간 추이")
    fig = px.line(
        df,
        x='trial_number',
        y='reaction_time_ms',
        title='시도별 반응시간',
        labels={'trial_number': '시도', 'reaction_time_ms': '반응시간 (ms)'},
        markers=True
    )
    fig.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.experiment_type == 'Stroop':
        st.subheader("정확도")
        accuracy_counts = df['accuracy'].value_counts()
        fig = px.pie(
            values=accuracy_counts.values,
            names=['오답' if i == 0 else '정답' for i in accuracy_counts.index],
            title='정답 vs 오답',
            color_discrete_map={'정답': '#00AA00', '오답': '#FF0000'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("상세 데이터")
    st.dataframe(df, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 CSV 다운로드",
            data=csv,
            file_name=f"experiment_{st.session_state.participant_data['participant_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔄 다시 실험", use_container_width=True):
            st.session_state.page = 'experiment_select'
            st.session_state.trial_data = []
            st.session_state.current_trial = 0
            st.rerun()
    
    with col3:
        if st.button("🏠 메인으로", use_container_width=True):
            st.session_state.page = 'main'
            st.session_state.trial_data = []
            st.session_state.current_trial = 0
            st.session_state.participant_data = {}
            st.rerun()
    
    save_data(df)

# ===== 전체 결과 분석 =====
def page_results_analysis():
    st.title("📈 전체 실험 결과 분석")
    
    all_data = load_all_data()
    
    if all_data.empty:
        st.info("저장된 데이터가 없습니다.")
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_participant = st.selectbox(
            "참가자 선택",
            ["전체"] + list(all_data['participant_id'].unique())
        )
    with col2:
        selected_experiment = st.selectbox(
            "실험 유형 선택",
            ["전체"] + list(all_data['experiment_type'].unique())
        )
    
    filtered_data = all_data.copy()
    if selected_participant != "전체":
        filtered_data = filtered_data[filtered_data['participant_id'] == selected_participant]
    if selected_experiment != "전체":
        filtered_data = filtered_data[filtered_data['experiment_type'] == selected_experiment]
    
    st.subheader("📊 통계")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 실험 수", len(filtered_data['participant_id'].unique()))
    with col2:
        st.metric("총 시도 횟수", len(filtered_data))
    with col3:
        avg_rt = filtered_data['reaction_time_ms'].mean()
        st.metric("평균 반응시간", f"{avg_rt:.0f}ms")
    with col4:
        avg_accuracy = (filtered_data['accuracy'].sum() / len(filtered_data) * 100) if len(filtered_data) > 0 else 0
        st.metric("평균 정확도", f"{avg_accuracy:.1f}%")
    
    st.subheader("참가자별 평균 반응시간")
    participant_stats = filtered_data.groupby('participant_id')['reaction_time_ms'].agg(['mean', 'std', 'count'])
    fig = px.bar(
        participant_stats.reset_index(),
        x='participant_id',
        y='mean',
        error_y='std',
        title='참가자별 평균 반응시간',
        labels={'participant_id': '참가자', 'mean': '평균 반응시간 (ms)'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("실험 유형별 비교")
    experiment_stats = filtered_data.groupby('experiment_type')['reaction_time_ms'].agg(['mean', 'std', 'count'])
    fig = px.bar(
        experiment_stats.reset_index(),
        x='experiment_type',
        y='mean',
        error_y='std',
        color='experiment_type',
        title='실험 유형별 평균 반응시간',
        labels={'experiment_type': '실험 유형', 'mean': '평균 반응시간 (ms)'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("전체 데이터")
    st.dataframe(filtered_data, use_container_width=True)
    
    csv = filtered_data.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 필터된 데이터 CSV 다운로드",
        data=csv,
        file_name=f"filtered_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ===== 메인 라우팅 =====
def main():
    st.sidebar.title("🧭 네비게이션")
    
    pages = {
        "🏠 메인": "main",
        "📋 참가자 정보": "participant_info",
        "🧪 실험 선택": "experiment_select",
        "⚙️ 실험 설정": "experiment_settings",
        "🎨 스트룹 과제": "stroop_test",
        "⚡ 클릭 반응": "click_reaction_test",
        "📊 결과": "results",
        "📈 전체 분석": "results_analysis"
    }
    
    selected_page = st.sidebar.selectbox("페이지 선택", list(pages.keys()))
    st.session_state.page = pages[selected_page]
    
    if st.session_state.page == "main":
        page_main()
    elif st.session_state.page == "participant_info":
        page_participant_info()
    elif st.session_state.page == "experiment_select":
        page_experiment_select()
    elif st.session_state.page == "experiment_settings":
        page_experiment_settings()
    elif st.session_state.page == "stroop_test":
        page_stroop_test()
    elif st.session_state.page == "click_reaction_test":
        page_click_reaction_test()
    elif st.session_state.page == "results":
        page_results()
    elif st.session_state.page == "results_analysis":
        page_results_analysis()

if __name__ == "__main__":
    main()
