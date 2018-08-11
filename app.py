from flask import *
import pandas as pd
import io
import requests


app = Flask(__name__)
@app.route('/')

def home():
    
        
    #     'https://www.fctables.com/england/premier-league/2017_2018/'
#      https://www.fctables.com/italy/serie-a/
    dfs_epl = pd.read_html(requests.get('https://www.fctables.com/england/premier-league/').text,header=0)
    table_epl = dfs_epl[0]
    table_epl.set_index('Team', inplace=True)
    table_epl_dict = table_epl.T.to_dict('list')
    
    dfs_sa = pd.read_html(requests.get('https://www.fctables.com/italy/serie-a/').text,header=0)
    table_sa = dfs_sa[0]
    table_sa.set_index('Team', inplace=True)
    table_sa_dict = table_sa.T.to_dict('list')
    
    
    leagues_dict = {}
    for d in [table_epl_dict, table_sa_dict]:
        leagues_dict.update(d)
    
    teams = {'Sean': ['Juventus', 'Torino', 'Everton', 'Cagliari', 'Bournemouth'],
            'Roham': ['Fiorentina', 'Sampdoria', 'Liverpool', 'Watford', 'Brighton'],
            'Omeid': ['Lazio', 'Inter', 'Southampton', 'Fulham', 'Cardiff'],
            'Farhan': ['Frosinone', 'Sassuolo', 'Tottenham', 'Chelsea', 'Genoa'],
            'Anooj': ['SSC Napoli', 'West Ham','Crystal Palace', 'Bologna', 'Huddersfield'],
            'Sarah': ['Atalanta', 'Burnley', 'Udinese', 'Chievo', 'Manchester City' ],
            'Ricardo': ['Roma', 'Leicester', 'Arsenal','Newcastle United' ,'SPAL 2013'],
            'Alex': ['SSD Parma', 'Manchester United', 'AC Milan', 'Wolverhampton Wanderers', 'Empoli']}
    leaderboard_dict = {}
    for name in teams:
        gp = int(0)
        pts = int(0)
        w = int(0)
        d = int(0)
        l = int(0)
        gd = int(0)
        for team in teams[name]:
            for table_team_name in leagues_dict:
                if team in table_team_name:
                    
                    values = leagues_dict[table_team_name]
            gp += values[1]
            pts += values[2]
            w += values[3]
            d += values[4]
            l += values[5]
            gd += values[8]
            
        leaderboard_dict[name] = [gp, pts, w, d, l, gd]
        
        
        
        
    leaderboard_df = pd.DataFrame.from_dict(leaderboard_dict, orient='index')
    leaderboard_df.columns= ['GP','PTS','W','D','L','GD']
    leaderboard_df = leaderboard_df.sort_values(by=['PTS', 'GD'], ascending=False)
    leaderboard_df = leaderboard_df.astype(int)
    
    return render_template('home.html',table=leaderboard_df.to_html())
    

    
if __name__ == '__main__':
    app.run(debug=True)