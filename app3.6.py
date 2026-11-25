import streamlit as st
import math

# --- 1. データの定義 ---
# 実際の値はメーカーカタログ等で確認し、正確な値に置き換えてください。
# 例: '種類': 外径を元に計算された断面積(mm^2)
CABLE_AREAS = {

    'CVD8㎟': 240.406,       # より合わせ外径：17.5mm
    'CVD14㎟': 283.385,       # より合わせ外径：19mm
    'CVD22㎟': 379.94,       # より合わせ外径：22mm
    'CVD38㎟': 530.66,       # より合わせ外径：26mm
    'CVD60㎟': 754.385,       # より合わせ外径：31mm

    'CVT8㎟': 283.385,       # より合わせ外径：19mm
    'CVT14㎟': 346.185,       # より合わせ外径：21mm
    'CVT22㎟': 452.16,       # より合わせ外径：24mm
    'CVT38㎟': 615.44,       # より合わせ外径：28mm
    'CVT60㎟': 854.865,      # より合わせ外径：33mm
    'CVT100㎟': 1319.585,    # より合わせ外径：41mm
    'CVT150㎟': 1734.065,    # より合わせ外径：47mm
    'CVT200㎟': 2374.625,    # より合わせ外径：55mm
    'CVT250㎟': 2826,        # より合わせ外径：60mm

    'IV5.5㎟': 19.625,        # 外径：5.0mm
    'IV8㎟': 28.26,           # 外径：6.0mm
    'IV14㎟': 45.3416,        # 外径：7.6mm
    'IV22㎟': 66.4424,        # 外径：9.2mm
    'IV38㎟': 103.81625,      # 外径：11.5mm
    'IV60㎟': 153.86,         # 外径：14.0mm
    'IV100㎟': 226.865,       # 外径：17.0mm

    'FCPEV0.9mmx2P': 35.23865,     # 外径：6.7mm
    'FCPEV1.2mmx2P': 51.50385,     # 外径：8.1mm
    'FCPEV1.2mmx3P': 62.17985,     # 外径：8.9mm
    'FCPEV1.2mmx5P': 86.54625,     # 外径：10.5mm

    'CVV-S2㎟-3C': 94.985,         # 外径：11.0mm      
    'CVV-S2㎟-4C': 103.81625,      # 外径：11.5mm

    'CVV3.5㎟-3C': 113.04,         # 外径：12.0mm
    'CVV5.5㎟-3C': 165.04625,      # 外径：14.5mm

    'PV3.5㎟': 32.1536,              # 外径：6.4mm
    'PV4.0㎟': 34.1946,              # 外径：6.6mm
    'PV5.5㎟': 41.83265,              # 外径：7.3mm
    'PV6.0㎟': 32.65796,              # 外径：6.45mm
}

# 例: '種類_呼び径': 内側断面積(mm^2)
CONDUIT_AREAS = {
    'G管_16': 211.1336,        # 内径：16.4mm、外径：21.3mm
    'G管_22': 376.49335,       # 内径：21.9mm、外径：26.8mm
    'G管_28': 628.69865,       # 内径：28.3mm、外径：33.6mm
    'G管_36': 1068.86385,      # 内径：36.9mm、外径：42.2mm
    'G管_42': 1437.9944,       # 内径：42.8mm、外径：48.1mm
    'G管_54': 2289.06,         # 内径：54.0mm、外径：59.9mm
    'G管_70': 3802.6656,       # 内径：69.6mm、外径：75.5mm
    'G管_82': 5317.03265,      # 内径：82.3mm、外径：88.2mm
    'G管_92': 6892.05665,      # 内径：93.7mm、外径：101.1mm

    'PFD管_16': 200.96,      # 内径：16mm、外径：23mm
    'PFD管_22': 379.94,      # 内径：22mm、外径：30.5mm
    'PFD管_28': 615.44,      # 内径：28mm、外径：36.5mm
    'PFD管_30': 706.5,       # 内径：30mm、外径：39mm
    'PFD管_36': 1017.36,     # 内径：36mm、外径：45.5mm
    'PFD管_42': 1256,        # 内径：40mm、外径：52mm

    '防水プリカ_24': 444.6554,      # 内径：23.8mm、外径：30.4mm
    '防水プリカ_30': 673.91465,     # 内径：29.3mm、外径：36.5mm
    '防水プリカ_38': 1080.48185,    # 内径：37.1mm、外径：44.9mm
    '防水プリカ_50': 1892.48585,    # 内径：49.1mm、外径：56.9mm^
    '防水プリカ_63': 3076.2266,     # 内径：62.6mm、外径：71.5mm
    '防水プリカ_76': 4534.16,       # 内径：76.0mm、外径：85.3mm
    '防水プリカ_83': 5150.385,      # 内径：81.0mm、外径：90.9mm
    '防水プリカ_101': 7881.4314,    # 内径：100.2mm、外径：110.1mm

    'FEP管_30': 706.5,        # 内径：30.0mm、外径：40mm
    'FEP管_40': 1384.74,      # 内径：42.0mm、外径：54mm
    'FEP管_50': 1962.5,       # 内径：50.0mm、外径：65mm
    'FEP管_65': 3419.46,      # 内径：66.0mm、外径：85mm
    'FEP管_80': 5024,         # 内径：80.0mm、外径：102mm
    'FEP管_100': 7850,        # 内径：100.0mm、外径：130mm
    'FEP管_125': 12265.625,   # 内径：125.0mm、外径：160mm

}
# 配管の外径データ（mm）
CONDUIT_OUTER_DIAMETERS = {
    'G管_16': 21.3,
    'G管_22': 26.8,
    'G管_28': 33.6,
    'G管_36': 42.2,
    'G管_42': 48.1,
    'G管_54': 59.9,
    'G管_70': 75.5,
    'G管_82': 88.2,
    'G管_92': 101.1,

    'PFD管_16': 23.0,
    'PFD管_22': 30.5,
    'PFD管_28': 36.5,
    'PFD管_30': 39.0,
    'PFD管_36': 45.5,
    'PFD管_42': 52.0,

    '防水プリカ_24': 30.4,
    '防水プリカ_30': 36.5,
    '防水プリカ_38': 44.9,
    '防水プリカ_50': 56.9,
    '防水プリカ_63': 71.5,
    '防水プリカ_76': 85.3,
    '防水プリカ_83': 90.9,
    '防水プリカ_101': 110.1,

    'FEP管_30': 40.0,
    'FEP管_40': 54.0,
    'FEP管_50': 65.0,
    'FEP管_65': 85.0,
    'FEP管_80': 102.0,
    'FEP管_100': 130.0,
    'FEP管_125': 160.0,
}
# 占有率の上限 (48%)⇒45%に変更
FILL_FACTOR_LIMIT = 0.45

# --- 2. 処理ロジックの定義 ---
def select_conduit_size(total_cable_area, conduit_type):
    """
    ケーブルの総断面積と配管の種類に基づいて、占有率45%以下で   # 48% ⇒ 45%に変更
    最小の配管サイズを選定します。
    """
    if total_cable_area <= 0:
        return (False, "エラー: ケーブルの総断面積がゼロまたは負の値です。")

    # 必要な配管の最小断面積を計算 (mm^2)
    required_conduit_area = total_cable_area / FILL_FACTOR_LIMIT

    # 該当する配管の種類で、必要な断面積を満たす最小のサイズを選定
    matching_conduits = {k: v for k, v in CONDUIT_AREAS.items() if k.startswith(conduit_type)}
    
    if not matching_conduits:
        return (False, f"エラー: 配管 '{conduit_type}' のデータが見つかりません。")

    selected_size = None
    min_sufficient_area = float('inf')

    # 最小の適切なサイズを探索
    for name, area in matching_conduits.items():
        if area >= required_conduit_area:
            if area < min_sufficient_area:
                min_sufficient_area = area
                selected_size = name
    
    if selected_size:
        # 選定された配管での実際の占有率を計算
        actual_fill_factor = total_cable_area / min_sufficient_area
        
        # 選定された配管の外径を取得
        outer_diameter = CONDUIT_OUTER_DIAMETERS[selected_size]

        # 結果メッセージ
        message = (
            f"✅ 選定された配管: **{selected_size}**\n"
            f"- 配管外径: {outer_diameter:.1f} mm\n"
            f"- 配管断面積: {min_sufficient_area:.2f} mm²\n"
            f"- ケーブル総断面積: {total_cable_area:.2f} mm²\n"
            f"- **実際の占有率**: **{actual_fill_factor*100:.1f} %** (基準: 45.0 %)"   # 48% ⇒ 45%に変更
        )
        return (True, message)
    else:
        max_area_in_type = max(matching_conduits.values())
        return (False, f"❌ エラー: {conduit_type} の最大サイズ "
                       f"({max_area_in_type:.2f} mm²) でも断面積が不足しています。より大きな配管が必要です。")

# --- 3. Streamlit UIと状態管理 ---
st.title('🔩 配管太さ選定アプリ (複数ケーブル対応・占有率45%)')   # 48% ⇒ 45%に変更
st.markdown('複数のケーブルの組み合わせと配管の種類に基づき、最小の配管サイズを選定します。')
st.markdown('**注意**: 占有率45%は、3本以上の電線を収める場合の基準値です。')    # 48% ⇒ 45%に変更

# セッションステートの初期化
if 'cables' not in st.session_state:
    st.session_state.cables = []

cable_options = list(CABLE_AREAS.keys())
conduit_options = sorted(list(set([k.split('_')[0] for k in CONDUIT_AREAS.keys()])))

# ケーブル追加関数
def add_cable():
    cable_type = st.session_state.new_cable_type
    cable_count = st.session_state.new_cable_count
    
    # 入力値の検証
    if cable_count < 1:
        st.warning('本数は1以上である必要があります。')
        return

    cable_area = CABLE_AREAS[cable_type]
    
    st.session_state.cables.append({
        'type': cable_type,
        'count': cable_count,
        'area': cable_area
    })
    # 入力フィールドをリセット（Streamlitの仕様上、再描画で自動リセットされるため不要なことが多いが、明示的にクリアする場合は使う）
    # st.session_state.new_cable_type = cable_options[0]
    # st.session_state.new_cable_count = 1

# ケーブル削除関数
def remove_cable(index):
    st.session_state.cables.pop(index)

# --- ステップ 1: ケーブルの追加 ---
st.header('ステップ 1: ケーブルの追加')

with st.form('add_cable_form', clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.selectbox(
            '線種を選択',
            cable_options,
            key='new_cable_type'
        )
    with col2:
        st.number_input(
            '本数',
            min_value=1,
            value=3,
            step=1,
            key='new_cable_count'
        )
        
    st.form_submit_button('➕ ケーブルを追加', on_click=add_cable)

# --- ステップ 2: 選択されたケーブルの確認 ---
st.header('ステップ 2: 選択されたケーブルの確認')

if st.session_state.cables:
    
    # DataFrame形式で表示（見やすくするため）
    data = []
    total_area_sum = 0
    for cable in st.session_state.cables:
        total_cable_area = cable['area'] * cable['count']
        total_area_sum += total_cable_area
        data.append({
            '線種': cable['type'],
            '本数': cable['count'],
            '単体断面積 (mm²)': f"{cable['area']:.2f}",
            '合計断面積 (mm²)': f"{total_cable_area:.2f}"
        })

    st.dataframe(data, hide_index=True, use_container_width=True)
    st.success(f"**総断面積**: **{total_area_sum:.2f} mm²**")

    # 削除ボタンの配置 (ループで動的に生成)
    st.markdown("---")
    st.caption("個別削除:")
    cols = st.columns(len(st.session_state.cables))
    for i, cable in enumerate(st.session_state.cables):
        cols[i].button(
            f"❌ {cable['type']} ({cable['count']}本)", 
            key=f"remove_{i}", 
            on_click=remove_cable, 
            args=(i,)
        )
        
else:
    st.info('ケーブルが追加されていません。上記フォームから追加してください。')
    total_area_sum = 0

# --- ステップ 3: 配管の選定 ---
st.header('ステップ 3: 配管の選定')

if st.session_state.cables:
    
    # 配管の種類の選択
    selected_conduit = st.selectbox(
        '管種を選択:',
        conduit_options,
        key='selected_conduit_type'
    )

    if st.button('🚀 配管サイズを選定する'):
        # 計算実行
        success, result_message = select_conduit_size(
            total_area_sum, 
            selected_conduit
        )
        
        # 結果表示
        if success:
            st.success('選定完了！')
            st.code(result_message)
            
            # 詳細情報の表示
            required_area = total_area_sum / FILL_FACTOR_LIMIT
            st.info(f"""
            **選定基準:**
            - ケーブル総断面積: {total_area_sum:.2f} mm²
            - 占有率の上限: {FILL_FACTOR_LIMIT*100:.0f} %
            - 必要な最小配管断面積: {required_area:.2f} mm²
            """)

        else:
            st.error(result_message)
            
else:
    st.warning('ケーブルが追加されていません。ステップ1でケーブルを追加してから実行してください。')