-- Stadiums
INSERT INTO Stadium (StadiumID, Name, City, Capacity)
VALUES (1, 'Camp Nou', 'Barcelona', 99354);
INSERT INTO Stadium (StadiumID, Name, City, Capacity)
VALUES (2, 'Santiago Bernabeu', 'Madrid', 81044);

-- Referees
INSERT INTO Referee (RefereeID, Name, Nationality, Experience_Level)
VALUES (101, 'Antonio Mateu Lahoz', 'Spanish', 'FIFA International');
INSERT INTO Referee (RefereeID, Name, Nationality, Experience_Level)
VALUES (102, 'Michael Oliver', 'English', 'FIFA International');

-- Coaches
INSERT INTO Coach (CoachID, Name, Nationality)
VALUES (201, 'Hansi Flick', 'German');
INSERT INTO Coach (CoachID, Name, Nationality)
VALUES (202, 'Xabi Alonso', 'Spanish');

-- Teams
INSERT INTO Team (TeamID, Name, StadiumID, CoachID)
VALUES (301, 'FC Barcelona', 1, 201);
INSERT INTO Team (TeamID, Name, StadiumID, CoachID)
VALUES (302, 'Real Madrid CF', 2, 202);

-- Players
INSERT INTO Player (PlayerID, Name, TeamID, Position, Nationality)
VALUES (401, 'Lamine Yamal', 301, 'Right Winger', 'Spanish');
INSERT INTO Player (PlayerID, Name, TeamID, Position, Nationality)
VALUES (402, 'Pedri', 301, 'Central Midfielder', 'Spanish');
INSERT INTO Player (PlayerID, Name, TeamID, Position, Nationality)
VALUES (403, 'Joan Garcia', 301, 'Goalkeeper', 'Spanish');
INSERT INTO Player (PlayerID, Name, TeamID, Position, Nationality)
VALUES (404, 'Kylian Mbappe', 302, 'Striker', 'French');
INSERT INTO Player (PlayerID, Name, TeamID, Position, Nationality)
VALUES (405, 'Jude Bellingham', 302, 'Attacking Midfielder', 'English');
INSERT INTO Player (PlayerID, Name, TeamID, Position, Nationality)
VALUES (407, 'Thibaut Courtois', 302, 'Goalkeeper', 'Belgian');

-- Matches
INSERT INTO Match (MatchID, MatchDateTime, HomeScore, AwayScore, Attendance, StadiumID, RefereeID, HomeTeamID, AwayTeamID)
VALUES (501, '2025-09-28 20:00:00', 3, 1, 99000, 1, 101, 301, 302);
INSERT INTO Match (MatchID, MatchDateTime, HomeScore, AwayScore, Attendance, StadiumID, RefereeID, HomeTeamID, AwayTeamID)
VALUES (502, '2026-03-15 21:00:00', 0, 1, 80000, 2, 102, 302, 301);

-- Player Stats
INSERT INTO Player_Stats VALUES (401, 501, 1, 90, 3, 0, 0, 0, NULL, NULL); 
INSERT INTO Player_Stats VALUES (402, 501, 1, 90, 0, 1, 0, 0, NULL, NULL); 
INSERT INTO Player_Stats VALUES (403, 501, 1, 90, 0, 0, 0, 0, 1, 0); 
INSERT INTO Player_Stats VALUES (404, 501, 1, 90, 1, 0, 0, 0, NULL, NULL); 
INSERT INTO Player_Stats VALUES (405, 501, 1, 90, 0, 0, 0, 0, NULL, NULL); 
INSERT INTO Player_Stats VALUES (407, 501, 1, 90, 0, 0, 0, 0, 3, 0); 
INSERT INTO Player_Stats VALUES (401, 502, 1, 90, 1, 0, 0, 0, NULL, NULL); 
INSERT INTO Player_Stats VALUES (402, 502, 1, 90, 0, 0, 0, 0, NULL, NULL); 
INSERT INTO Player_Stats VALUES (403, 502, 1, 90, 0, 0, 0, 0, 0, 1); 
INSERT INTO Player_Stats VALUES (404, 502, 1, 90, 0, 0, 0, 0, NULL, NULL); 
INSERT INTO Player_Stats VALUES (405, 502, 1, 90, 0, 0, 0, 0, NULL, NULL); 
INSERT INTO Player_Stats VALUES (407, 502, 1, 90, 0, 0, 0, 0, 1, 0); 

-- Standings 
INSERT INTO Standings (TeamID, Matches_Played, Wins, Draws, Losses, Goals_For, Goals_Against)
VALUES (301, 2, 2, 0, 0, 4, 1);
INSERT INTO Standings (TeamID, Matches_Played, Wins, Draws, Losses, Goals_For, Goals_Against)
VALUES (302, 2, 0, 0, 2, 1, 4);