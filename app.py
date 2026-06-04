import streamlit as st
import json
import os

# 設定網頁標題與 RWD 手機優化
st.set_page_config(page_title="團長投票系統", page_icon="🗳️", layout="centered")

# --- 設定檔案路徑（用 JSON 模擬資料庫儲存結果） ---
DATA_FILE = "vote_data.json"

# --- 你提供的 67 人完整可投票者名單 ---
VOTER_WHITELIST = [
    "洪郁宸", "唐譽宸", "吳霜", "陳又榆", "張哲維", "陳俞安", "王玉霈", "林軒宇", 
    "謝佳晉", "林子馨", "戴宜婷", "黃翌瑄", "陳勤雅", "王歆瑜", "樋口和香", "吳紹安", 
    "黎芯宇", "游沛妤", "鐘巧伶", "莊毓婕", "蕭丞希", "連昱臻", "簡愷瑢", "趙侗欣", 
    "謝玗潔", "陳芓涵", "黃宥慈(窩心組)", "黃宥慈(樂活組)", "陳宓彤", "陳湉昕", "陳欣妤", "李奉燕", "楊言諾", 
    "劉宛蓁", "張善源", "林沛妤", "郭易昀", "曹若忻", "李響", "陳振棋", "謝靜華", 
    "蔡佩穎", "許詠約", "林姿妤", "蔡慈恩", "吳子瑄", "簡昱佳", "謝思賢", "江旻儒", 
    "游幸璇", "丘迺盈", "楊承澤", "胡桂禎", "陳嘉萱", "歐芝妤", "李立中", "蘇勇誠", 
    "丁垚鈞", "廖薇薇", "謝心媞", "葉宣彣", "賴祫翎", "陳鈺冺", "黃庭萱", "詹惠竹", 
    "楊淑雯", "鄭詩蓉"
]

# --- 初始化資料庫 ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # 所有人初始狀態都是「未投票(False)」，同意與不同意票數為 0
        voted_status = {voter: False for voter in VOTER_WHITELIST}
        return {
            "voted_status": voted_status,
            "results": {"同意": 0, "不同意": 0}
        }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 載入當前投票狀態
data = load_data()

# --- 網頁介面設計 ---
st.title("🗳️ 下一屆團長不記名投票系統")
st.write("本系統採用分離式設計，僅紀錄『誰投過票』與『票數總計』，兩者無關聯，確保絕對匿名。")
st.markdown("---")

# 1. 身份驗證區
st.header("第一步：驗證投票資格")
user_name = st.text_input("請輸入您的真實姓名以驗證身份:").strip()

if user_name:
    if user_name not in data["voted_status"]:
        st.error("❌ 您輸入的姓名不在本次投票的名單中，請檢查是否有錯字，或連繫管理員。")
    elif data["voted_status"][user_name]:
        st.warning("⚠️ 系統紀錄顯示：此姓名已經完成過投票，無法重複投票！")
    else:
        st.success("✅ 資格驗證成功！請在下方投下您神聖的一票。")
        
        # 2. 投票區
        st.markdown("---")
        st.header("第二步：不記名表決")
        st.subheader("⚠️ 請問您是否同意由候選人擔任下一屆團長？")
        
        vote_choice = st.radio("請選擇您的意向：", ["請選擇...", "同意", "不同意"], index=0)
        
        submit_button = st.button("確認送出選票 (送出後無法修改)")
        
        if submit_button:
            if vote_choice == "請選擇...":
                st.error("請先選擇『同意』或『不同意』再點擊送出。")
            else:
                # 執行投票邏輯（防重複 + 匿名累加）
                data["voted_status"][user_name] = True
                data["results"][vote_choice] += 1
                
                # 儲存回 JSON 檔案
                save_data(data)
                
                st.balloons()
                st.success("🎉 投票成功！感謝您的參與，您現在可以關閉此網頁了。")
                st.rerun()

# --- 管理員後台 ---
st.markdown("---")
with st.expander("📊 管理員檢視投票進度與結果 (點擊展開)"):
    total_voters = len(VOTER_WHITELIST)
    voted_count = sum(1 for v in data["voted_status"].values() if v)
    
    st.write(f"**目前投票率：** {voted_count} / {total_voters} 人已投票")
    
    # 顯示未投票名單（方便催票，但不會洩漏大家投什麼）
    unvoted_list = [name for name, voted in data["voted_status"].items() if not voted]
    if unvoted_list:
        st.write(f"**尚未投票的人員：** {', '.join(unvoted_list)}")
    else:
        st.write("🎉 所有人皆已投票完畢！")
        
    st.markdown("---")
    st.write("**當前開票結果：**")
    st.json(data["results"])
