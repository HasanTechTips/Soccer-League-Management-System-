import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, g

# --- Configuration ---
DATABASE_FILE = "league.db"

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Change this to a random string

# --- Database Helper Functions ---
def get_db():
    """Gets a database connection for the current request."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_FILE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """Closes the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- === MENU: DATABASE SETUP BUTTONS === ---
@app.route('/run_sql/<string:action>')
def run_sql_file(action):
    """
    Runs a specific SQL file based on the action provided.
    This replaces the old /setup route.
    """
    
    # Map actions to filenames
    sql_files = {
        'drop': ('01_drop_tables.sql', 'Drop Tables'),
        'create': ('02_create_tables.sql', 'Create Tables'),
        'populate': ('03_populate_tables.sql', 'Populate Tables (Insert Data)')
    }
    
    if action not in sql_files:
        return "Invalid operation", 404

    file_name, operation_name = sql_files[action]

    try:
        # Check if the database file exists for dropping tables
        if action == 'drop' and not os.path.exists(DATABASE_FILE):
             message = "Database file does not exist. Nothing to drop."
             return render_template('_operation_complete.html', message=message, operation=operation_name)

        # Read the SQL file
        with open(file_name, 'r') as f:
            sql_script = f.read()
        
        # Connect and execute the script
        conn = get_db()
        conn.executescript(sql_script)
        conn.commit()
        
        message = f"Successfully executed: {operation_name}"

    except FileNotFoundError:
         message = f"Error: SQL file '{file_name}' not found."
    except sqlite3.Error as e:
        message = f"An error occurred during {operation_name}: {e}"
    except Exception as e:
        message = f"An unexpected error occurred: {e}"

    return render_template('_operation_complete.html', message=message, operation=operation_name)


# --- === MENU: QUERY TABLES (Homepage) === ---
@app.route('/')
def index():
    """
    Main page - Fetches all data and renders it on the homepage.
    This is our "Query Tables" menu option.
    """
    conn = get_db()
    query_results = {}

    try:
        # 5. Team Win Percentage (Standings)
        query_results['win_percentage'] = conn.execute("""
            SELECT
                ROW_NUMBER() OVER (
                    ORDER BY 
                        (S.Wins * 3 + S.Draws * 1) DESC,  -- Points
                        (S.Goals_For - S.Goals_Against) DESC -- Goal Difference
                ) AS Rank,
                T.Name AS Team_Name, S.Matches_Played, S.Wins, S.Draws, S.Losses,
                S.Goals_For, S.Goals_Against,
                (S.Goals_For - S.Goals_Against) AS Goals_Difference,
                (S.Wins * 3 + S.Draws * 1) AS Points,
                ROUND((CAST(S.Wins AS FLOAT) / S.Matches_Played) * 100, 2) AS Win_Percentage
            FROM Team T
            JOIN Standings S ON T.TeamID = S.TeamID
            ORDER BY Rank ASC;
        """).fetchall()

        # 1. Avg Goals Conceded
        query_results['avg_goals_conceded'] = conn.execute("SELECT P.Name AS Goalkeeper_Name, T.Name AS Team_Name, COUNT(PS.MatchID) AS Matches_Played_GK, ROUND(AVG(PS.Goals_Conceded), 2) AS Avg_Goals_Conceded_Per_Match FROM Player P JOIN Team T ON P.TeamID = T.TeamID JOIN Player_Stats PS ON P.PlayerID = PS.PlayerID WHERE P.Position = 'Goalkeeper' AND PS.Goals_Conceded IS NOT NULL GROUP BY P.Name, T.Name ORDER BY Avg_Goals_Conceded_Per_Match ASC;").fetchall()
        # 2. Matches Hosted
        query_results['matches_hosted'] = conn.execute("SELECT S.Name AS Stadium_Name, S.City, COUNT(M.MatchID) AS Total_Matches_Hosted FROM Stadium S JOIN Match M ON S.StadiumID = M.StadiumID GROUP BY S.Name, S.City ORDER BY Total_Matches_Hosted DESC;").fetchall()
        # 3. Players with More Assists than Goals
        query_results['assists_vs_goals'] = conn.execute("SELECT P.Name AS Player_Name, T.Name AS Team_Name, SUM(PS.Goals) AS Total_Goals, SUM(PS.Assists) AS Total_Assists FROM Player P JOIN Team T ON P.TeamID = T.TeamID JOIN Player_Stats PS ON P.PlayerID = PS.PlayerID GROUP BY P.Name, T.Name HAVING SUM(PS.Assists) > SUM(PS.Goals) ORDER BY Total_Assists DESC, Player_Name;").fetchall()
        # 4. Coaches
        query_results['coaches'] = conn.execute("SELECT Name, Nationality FROM Coach WHERE Nationality = 'Spanish' UNION SELECT Name, Nationality FROM Coach WHERE Nationality = 'German' ORDER BY Nationality, Name;").fetchall()
        
    except sqlite3.Error as e:
        # This error happens if tables don't exist
        if "no such table" in str(e):
             message = "Database tables not found. Please create and populate them using the buttons in the navbar."
             return render_template('_operation_complete.html', message=message, operation="Database Error")
        else:
            return f"Database query error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

    return render_template('index.html', results=query_results)


# --- === MENU: C.R.U.D. & SEARCH === ---
@app.route('/players', methods=['GET', 'POST'])
def manage_players():
    """
    Page to list all players and handle search.
    """
    conn = get_db()
    search_term = ""
    
    try:
        if request.method == 'POST':
            search_term = request.form['search']
            query = """
                SELECT P.PlayerID, P.Name, P.Position, P.Nationality, T.Name AS Team_Name
                FROM Player P
                JOIN Team T ON P.TeamID = T.TeamID
                WHERE P.Name LIKE ? OR P.Position LIKE ? OR T.Name LIKE ?
                ORDER BY P.Name
            """
            players = conn.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")).fetchall()
        else:
            query = """
                SELECT P.PlayerID, P.Name, P.Position, P.Nationality, T.Name AS Team_Name
                FROM Player P
                JOIN Team T ON P.TeamID = T.TeamID
                ORDER BY P.Name
            """
            players = conn.execute(query).fetchall()
            
    except sqlite3.Error as e:
        if "no such table" in str(e):
             message = "Player table not found. Please create and populate the database."
             return render_template('_operation_complete.html', message=message, operation="Database Error")
        else:
            return f"Database query error: {e}"

    return render_template('players.html', players=players, search_term=search_term)

@app.route('/player/add', methods=['GET', 'POST'])
def add_player():
    """
    Page with a form to add a new player (CREATE).
    """
    conn = get_db()
    
    if request.method == 'POST':
        player_id = request.form['player_id']
        name = request.form['name']
        team_id = request.form['team_id']
        position = request.form['position']
        nationality = request.form['nationality']
        
        try:
            conn.execute(
                "INSERT INTO Player (PlayerID, Name, TeamID, Position, Nationality) VALUES (?, ?, ?, ?, ?)",
                (player_id, name, team_id, position, nationality)
            )
            conn.commit()
        except sqlite3.Error as e:
            return f"Error adding player: {e}"
            
        return redirect(url_for('manage_players')) 

    teams = conn.execute("SELECT TeamID, Name FROM Team ORDER BY Name").fetchall()
    return render_template('add_player.html', teams=teams)

@app.route('/player/edit/<int:player_id>', methods=['GET', 'POST'])
def edit_player(player_id):
    """
    Page to edit an existing player (UPDATE).
    """
    conn = get_db()
    
    if request.method == 'POST':
        name = request.form['name']
        team_id = request.form['team_id']
        position = request.form['position']
        nationality = request.form['nationality']
        
        try:
            conn.execute(
                "UPDATE Player SET Name = ?, TeamID = ?, Position = ?, Nationality = ? WHERE PlayerID = ?",
                (name, team_id, position, nationality, player_id)
            )
            conn.commit()
        except sqlite3.Error as e:
            return f"Error updating player: {e}"
            
        return redirect(url_for('manage_players'))

    player = conn.execute("SELECT * FROM Player WHERE PlayerID = ?", (player_id,)).fetchone()
    if player is None:
        return "Player not found", 404
        
    teams = conn.execute("SELECT TeamID, Name FROM Team ORDER BY Name").fetchall()
    return render_template('edit_player.html', player=player, teams=teams)

@app.route('/player/delete/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    """
    Route to handle deleting a player (DELETE).
    """
    conn = get_db()
    try:
        conn.execute("DELETE FROM Player_Stats WHERE PlayerID = ?", (player_id,))
        conn.execute("DELETE FROM Player WHERE PlayerID = ?", (player_id,))
        conn.commit()
    except sqlite3.Error as e:
        return f"Error deleting player: {e}"
        
    return redirect(url_for('manage_players'))

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)