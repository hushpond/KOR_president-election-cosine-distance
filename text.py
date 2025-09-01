import pandas as pd
import re
from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import defaultdict, Counter
from concurrent.futures import ProcessPoolExecutor
import seaborn as sns

def get_korean_font():
    fonts = [f.name for f in fm.fontManager.ttflist if (
        'Gothic' in f.name or '돋움' in f.name or '굴림' in f.name or 'Apple' in f.name or '나눔' in f.name
    )]
    return fm.findfont(fonts[0]) if fonts else None

def extract_nouns(text):
    okt = Okt()
    stopwords = set(['안녕하세요'])
    nouns = [n for n in okt.nouns(text) if n not in stopwords and len(n) > 1]
    return nouns

def main():
    FONT_PATH = get_korean_font()
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

    FILE = 'boong.txt'
    pat_msg = re.compile(r"\[([^\[\]]+)\] \[([오전|오후]+ [0-9]{1,2}:[0-9]{2})\] (.+)")
    pat_date = re.compile(r"-{7,}\s*([0-9]{4})년 ([0-9]{1,2})월 ([0-9]{1,2})일 ([^ ]+)요일\s*-{7,}")

    def parse_talkstream(filename):
        with open(filename, encoding='utf-8') as f:
            curr_date, curr_weekday = None, None
            for line in f:
                line = line.strip()
                m_date = pat_date.match(line)
                if m_date:
                    curr_date = f"{m_date.group(1)}-{int(m_date.group(2)):02d}-{int(m_date.group(3)):02d}"
                    curr_weekday = m_date.group(4)
                    continue
                m_msg = pat_msg.match(line)
                if m_msg and curr_date:
                    name = m_msg.group(1).strip()
                    time = m_msg.group(2)
                    context = m_msg.group(3).replace('\u200b', '').strip()
                    ampm, hms = time.split(' ')
                    hour, minute = map(int, hms.split(':'))
                    if ampm == '오후' and hour != 12:
                        hour += 12
                    if ampm == '오전' and hour == 12:
                        hour = 0
                    yield (curr_date, curr_weekday, hour, minute, name, context)

    data_iter = parse_talkstream(FILE)
    df = pd.DataFrame(data_iter, columns=['date', 'weekday', 'hour', 'minute', 'name', 'message'])

    # date → datetime 변환 및 월 파생
    df['date_dt'] = pd.to_datetime(df['date'])
    df['ym'] = df['date_dt'].dt.to_period('M').astype(str)

    person_text_dict = defaultdict(list)
    all_text = []
    for msg, name in zip(df['message'], df['name']):
        person_text_dict[name].append(msg)
        all_text.append(msg)

    with ProcessPoolExecutor() as executor:
        people = list(person_text_dict.keys())
        person_concat_text = [' '.join(person_text_dict[name]) for name in people]
        result = list(executor.map(extract_nouns, person_concat_text))

    # 전체 워드클라우드
    all_nouns = extract_nouns(' '.join(all_text))
    all_freq = Counter(all_nouns)
    wc = WordCloud(font_path=FONT_PATH, background_color='white', width=800, height=400).generate_from_frequencies(all_freq)
    plt.figure(figsize=(12,6))
    plt.title('전체 대화 워드클라우드')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    input("전체 워드클라우드 확인 후 Enter...")

    # 요일-시간대별 대화량 히트맵
    pivot = df.pivot_table(index='weekday', columns='hour', values='message', aggfunc='count').fillna(0)
    weekday_order = ['월', '화', '수', '목', '금', '토', '일']
    pivot = pivot.reindex(weekday_order)
    plt.figure(figsize=(14, 6))
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu')
    plt.title('요일-시간대별 대화 빈도 히트맵')
    plt.ylabel('요일')
    plt.xlabel('시간')
    plt.show()
    input("요일-시간대별 히트맵 확인 후 Enter...")

    # 인물별 워드클라우드
    for pname, nouns in zip(people, result):
        if nouns:
            freq = Counter(nouns)
            wc = WordCloud(font_path=FONT_PATH, background_color='white', width=600, height=300).generate_from_frequencies(freq)
            plt.figure(figsize=(9,4))
            plt.title(f'{pname} 워드클라우드')
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.show()
            print(f"{pname} 주요 단어 Top 10:", freq.most_common(10))
            input(f"{pname} 워드클라우드 확인 후 Enter...")

    # 인물별 시간대별 대화량 히트맵
    pivot_people_hour = df.pivot_table(index='name', columns='hour', values='message', aggfunc='count').fillna(0)
    print('--- 인물별 시간대별 대화량 Top3 ---')
    top_hours = pivot_people_hour.apply(lambda row: row.nlargest(3), axis=1)
    print(top_hours)
    plt.figure(figsize=(15, max(4, len(pivot_people_hour)*0.7)))
    sns.heatmap(pivot_people_hour, annot=True, fmt='.0f', cmap='YlOrRd')
    plt.title('인물별 시간대별 대화 빈도 히트맵')
    plt.xlabel('시간')
    plt.ylabel('이름')
    plt.show()
    input("인물별 시간대별 히트맵 확인 후 Enter...")

    # 인물별 월별 대화건수 시각화 (추가)
    pivot_people_month = df.pivot_table(index='name', columns='ym', values='message', aggfunc='count').fillna(0)
    print('--- 인물별 월별 대화건수 ---')
    print(pivot_people_month.astype(int))

    plt.figure(figsize=(16, max(5, len(people)*0.5)))
    pivot_people_month.T.plot(kind='bar', stacked=True, figsize=(16,6))
    plt.title('인물별 월별 메시지 건수(누가 어느 달에 얼마나 활동?)')
    plt.xlabel('월')
    plt.ylabel('메시지 수')
    plt.legend(title='이름', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
    input("인물별 월별 메시지 건수 그래프 확인 후 Enter...")

    # (옵션) 한 인물의 월별 활동만 따로 바그래프로 보고 싶다면:
    person = people[0]
    person_month_counts = df[df['name'] == person]['ym'].value_counts().sort_index()
    plt.figure(figsize=(10, 4))
    person_month_counts.plot(kind='bar')
    plt.title(f"{person}의 월별 대화 빈도")
    plt.xlabel('월')
    plt.ylabel('메시지 수')
    plt.show()
    input(f"{person} 월별 바그래프 확인 후 Enter...")

if __name__ == "__main__":
    main()
