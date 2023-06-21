import pandas as pd

date = '1101'


def convert_unique_idx(df, column_name):
    column_dict = {x: i for i, x in enumerate(df[column_name].unique())}
    df[column_name] = df[column_name].apply(column_dict.get)
    df[column_name] = df[column_name].astype('int')
    assert df[column_name].min() == 0
    assert df[column_name].max() == len(column_dict) - 1
    return df, column_dict


df = pd.read_csv('SQLAExport_date_{}.txt'.format(date), sep="\t", header=0)
df.columns = ["date", "call_arrive_time", "agent_id", "time_1", "time_2", "time_3", "rank", "score_call", "type_call",
              "score_agent", "type_agent"]
df = df.drop_duplicates(subset=['call_arrive_time', 'agent_id'], keep='last')
# get overall serve_time
df['serve_time'] = df['time_1'] + df['time_2'] + df['time_3']
df = df[["date", "call_arrive_time", "agent_id", "serve_time", "score_call", "type_call", "score_agent", "type_agent"]]
df['call_arrive_time'] = df['call_arrive_time'].astype(str).str[-8:]
# get categorical agent_id
df['agent_id'] = pd.Categorical(df['agent_id'])
# remove '?'
# df = df[df.type_call != '?']
# df = df[df.score_call != '?']
df = df.sort_values('call_arrive_time')

df = df.reset_index(drop=True)

df, agent_dict = convert_unique_idx(df, "agent_id")

print("df:", df)
df.to_csv('date_{}_preprocess_nan.csv'.format(date), sep=',')
