import streamlit as st
import json
import os

# 設定網頁標題與 RWD 手機優化
st.set_page_config(page_title="諮商中心志工團 團長投票系統", page_icon="🧡", layout="centered")

# --- 設定檔案路徑（用 JSON 儲存匿名結果） ---
DATA_FILE = "vote_data.json"

# --- ⚙️ 幹部專區密碼設定 ⚙️ ---
# 你可以把下面的 "1234" 改成任何你想設定的密碼
ADMIN_PASSWORD = "1234"

# --- 67 人完整志工夥伴名單 ---
VOTER_WHITELIST = [
    "洪郁宸", "唐譽宸", "吳霜", "陳又榆", "張哲維", "陳俞安", "王玉霈", "林軒宇", 
    "謝佳晉", "林子馨", "戴宜婷", "黃翌瑄", "陳勤雅", "王歆瑜", "樋口和香", "吳紹安", 
    "黎芯宇", "游沛妤", "鐘巧伶", "莊毓婕", "蕭丞希", "連昱臻", "簡愷瑢", "趙侗欣", 
    "謝玗潔", "陳芓涵", "黃宥慈(窩心組)", "黃宥慈(樂活組)", "陳宓彤", "陳湉昕", "陳欣妤", "李奉燕", "楊言諾", 
    "劉宛蓁", "張善源", "林沛妤", "郭易昀", "曹若忻", "李響", "陳振棋", "謝靜華", 
    "蔡佩穎", "許詠約", "林姿妤", "蔡慈恩", "吳子瑄", "簡昱佳", "謝思賢", "江旻儒", 
    "游幸璇", "丘迺盈", "楊承澤", "胡桂禎", "陳嘉萱", "歐芝妤", "李立中", "蘇勇誠", 
    "丁垚鈞", "廖薇薇", "謝心媞", "葉宣彣", "賴祫翎", "陳鈺冺", "黃庭萱", "詹惠竹", 
    "楊淑雯", "鄭詩蓉", "楊雅婷", "吳雅慧", "賴姳臻", "李雅惠", "李翠華", "林奕嫺", "高祺淳", "張歆昀", "許宜琳", "陳美如", "謝慧馨", "鍾文琳", "劉晴雯", "游佳蓁", "陳彥穎", "曾詩惠", "楊素瑄"
]

# --- 初始化資料庫（含自動防錯修正） ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        
        # 自動修正：確保名單變更時舊的 JSON 紀錄能同步更新，避免系統崩潰
        for voter in VOTER_WHITELIST:
            if voter not in existing_data["voted_status"]:
                existing_data["voted_status"][voter] = False
                
        return existing_data
    else:
        voted_status = {voter: False for voter in VOTER_WHITELIST}
        return {
            "voted_status": voted_status,
            "results": {"同意": 0, "不同意": 0}
        }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# --- 網頁介面設計 ---
st.title("🧡 諮商中心志工團：下一屆團長不記名投票")
st.write("親愛的志工夥伴，謝謝你過去這段日子的付出與陪伴。這裡永遠是最溫暖的地方。")
st.write("為了團隊的延續，請花一分鐘為我們的新團隊投下神聖的一票。本系統採用『絕對匿名設計』，你可以安心並真誠地表達想法。")
st.markdown("---")

# 1. 身份驗證區
st.header("✨ 夥伴，請先驗證身份")

st.info("📢 **名字輸入小提醒**：\n如果是**宥慈**要投票，請依照格式輸入：`黃宥慈(窩心組)` 或 `黃宥慈(樂活組)` 唷！（括號請用半形括號 `()`）")

user_name = st.text_input("請輸入您的完整姓名:").strip()

if user_name:
    if user_name not in data["voted_status"]:
        if user_name == "黃宥慈":
            st.error("❌ 哎呀！團內有兩位宥慈夥伴唷，請幫我們在名字後面加上組別，例如：`黃宥慈(窩心組)` 或 `黃宥慈(樂活組)`")
        else:
            st.error("❌ 哎呀，名單上找不到這個名字！請檢查有沒有錯字，或是戳一下幹部幫你確認。")
    elif data["voted_status"][user_name]:
        st.warning("⚠️ 系統紀錄顯示你已經投過囉！謝謝你的熱心參與～")
    else:
        st.success("🎉 認證成功！很高興看見你，請在下方留下你的溫暖心聲。")
        
        # 2. 投票區
        st.markdown("---")
        st.header("🗳️ 團長表決")
        st.subheader("💡 請問你是否同意由「林姿妤」擔任諮商中心志工團下一屆團長？")
        
        vote_choice = st.radio("請選擇您的意向：", ["請選擇...", "同意，支持姿妤帶領大家！", "不同意，我有其他想法。"], index=0)
        
        st.markdown("---")
        submit_button = st.button("💝 確認送出選票 (送出後就不能修改囉)")
        
        if submit_button:
            if vote_choice == "請選擇...":
                st.error("請先選擇對「林姿妤」擔任團長的投票意向，再點擊送出唷！")
            else:
                final_vote = "同意" if "同意" in vote_choice else "不同意"
                
                data["voted_status"][user_name] = True
                data["results"][final_vote] += 1
                
                save_data(data)
                
                st.balloons()
                st.success("🥰 投票成功！謝謝你為志工團付出的每一份心力，可以關閉這個網頁囉。")
                st.rerun()

# --- 管理員後台（全功能加密鎖定） ---
st.markdown("---")
with st.expander("📊 幹部專區：密碼驗證解鎖 (點擊展開)"):
    
    st.write("#### 🔒 請輸入密碼解鎖後台資訊")
    input_pwd = st.text_input("請輸入幹部管理密碼：", type="password")
    
    if input_pwd == ADMIN_PASSWORD:
        st.success("🔓 密碼正確！已為您載入即時後台數據。")
        st.markdown("---")
        
        # 計算投票進度
        total_voters = len(VOTER_WHITELIST)
        voted_count = sum(1 for v in data["voted_status"].values() if v)
        
        # 1. 顯示投票進度
        st.write(f"### 📈 目前投票進度：{voted_count} / {total_voters} 位夥伴已參與")
        
        # 2. 顯示催票名單
        unvoted_list = [name for name, voted in data["voted_status"].items() if not voted]
        if unvoted_list:
            st.write(f"**💡 還沒投票的夥伴（可以悄悄去提醒他們唷）：**\n{'、'.join(unvoted_list)}")
        else:
            st.write("🎉 太棒了！所有夥伴都投票完畢囉！")
            
        st.markdown("---")
        
        # 3. 顯示開票結果
        st.write("### 📢 團長開票結果")
        st.json(data["results"])
        
    elif input_pwd != "":
        st.error("❌ 密碼錯誤，無法解鎖進度與結果。")
