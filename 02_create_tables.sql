-- Stadiums
CREATE TABLE Stadium ( 
    StadiumID INT PRIMARY KEY, 
    Name VARCHAR(100) NOT NULL, 
    City VARCHAR(75), 
    Capacity INT CHECK (Capacity >= 0) 
); 

-- Referees
CREATE TABLE Referee ( 
    RefereeID INT PRIMARY KEY, 
    Name VARCHAR(100) NOT NULL, 
    Nationality VARCHAR(50), 
    Experience_Level VARCHAR(30) 
);

-- Coaches
CREATE TABLE Coach ( 
    CoachID INT PRIMARY KEY, 
    Name VARCHAR(100) NOT NULL, 
    Nationality VARCHAR(50) 
);

-- Teams
CREATE TABLE Team ( 
    TeamID INT PRIMARY KEY, 
    Name VARCHAR(100) NOT NULL UNIQUE, 
    StadiumID INT NOT NULL, 
    CoachID INT NOT NULL UNIQUE, 
    FOREIGN KEY (StadiumID) REFERENCES Stadium(StadiumID), 
    FOREIGN KEY (CoachID) REFERENCES Coach(CoachID) 
); 

-- Players
CREATE TABLE Player ( 
    PlayerID INT PRIMARY KEY, 
    Name VARCHAR(100) NOT NULL, 
    TeamID INT NOT NULL, 
    Position VARCHAR(30), 
    Nationality VARCHAR(50), 
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID) 
); 

-- Matches
CREATE TABLE Match (
    MatchID INT PRIMARY KEY,
    MatchDateTime TIMESTAMP NOT NULL,
    HomeScore INT CHECK (HomeScore >= 0),
    AwayScore INT CHECK (AwayScore >= 0),
    Attendance INT CHECK (Attendance >= 0),
    StadiumID INT NOT NULL,
    RefereeID INT NOT NULL,
    HomeTeamID INT NOT NULL,
    AwayTeamID INT NOT NULL,
    FOREIGN KEY (StadiumID) REFERENCES Stadium (StadiumID),
    FOREIGN KEY (RefereeID) REFERENCES Referee (RefereeID),
    FOREIGN KEY (HomeTeamID) REFERENCES Team (TeamID),
    FOREIGN KEY (AwayTeamID) REFERENCES Team (TeamID),
    CONSTRAINT CHK_DistinctTeams CHECK (HomeTeamID <> AwayTeamID)
);

-- Player Stats
CREATE TABLE Player_Stats ( 
    PlayerID INT NOT NULL, 
    MatchID INT NOT NULL, 
    Appearances INT CHECK (Appearances >= 0), 
    Minutes_Played INT CHECK (Minutes_Played >= 0), 
    Goals INT CHECK (Goals >= 0), 
    Assists INT CHECK (Assists >= 0), 
    Yellow_Cards INT CHECK (Yellow_Cards >= 0), 
    Red_Cards INT CHECK (Red_Cards >= 0), 
    Goals_Conceded INT CHECK (Goals_Conceded >= 0), 
    Clean_Sheets INT CHECK (Clean_Sheets >= 0), 
    PRIMARY KEY (PlayerID, MatchID), 
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID), 
    FOREIGN KEY (MatchID) REFERENCES Match(MatchID) 
); 

-- Standings 
CREATE TABLE Standings ( 
    TeamID INT NOT NULL, 
    Matches_Played INT DEFAULT 0 NOT NULL CHECK (Matches_Played >= 0), 
    Wins INT DEFAULT 0 NOT NULL CHECK (Wins >= 0), 
    Draws INT DEFAULT 0 NOT NULL CHECK (Draws >= 0), 
    Losses INT DEFAULT 0 NOT NULL CHECK (Losses >= 0), 
    Goals_For INT DEFAULT 0 NOT NULL CHECK (Goals_For >= 0), 
    Goals_Against INT DEFAULT 0 NOT NULL CHECK (Goals_Against >= 0), 
    CONSTRAINT PK_Standings PRIMARY KEY (TeamID), 
    CONSTRAINT FK_Standings_Team FOREIGN KEY (TeamID) REFERENCES Team(TeamID) 
);