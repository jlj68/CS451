----------------------
EnjoyChess Readme v1.0
----------------------

The program can be accessed via the following URL as of March 7, 2016:

    http://rpi.rawhat.net:8080

  this will send the user to the home page.

The user should then enter a username, and then can proceed to the game lobby.

The lobby will list all connected players, and the user can select another
player to invite to a game.  The series of dialog boxes will instruct the user
on how to send the invite.  If the invitation is accepted, both users will be
sent to the game screen.

On the game screen, each user can drag their pieces onto a valid position to
make a move, provided it is their turn.  The system will prompt the user for
various events.

Upon completion of the game, or a forfeit by one of the players, the user will
be returned to the lobby and can play another game if they wish.

----------------------
Installing the Software
----------------------

The following software is required to install the game server on your computer:

    Python >= 3.4
    pip3                    (requires python3-dev and python3-setuptools)
    tornado                 (can be installed using `pip3 install tornado`)

  after these programs are installed, the server can be run with the following:

    python3 webserver.py

The server will then listen on port 8080 of the local machine.  It can be
accessed from a browser with the URL `localhost:8080`.

NOTE:  It appears as though the Drexel network does not allow the use of the
       WebSocket protocol.  This functionality is integral to EnjoyChess.  The
       game may be run from a local machine, but it also uses cookies to save
       each username.  Therefore, it may be difficult to test on a single
       local machine.  One solution is to use two web browsers.  The program
       has been tested using Firefox 44.0.2 on Linux and Windows, as well as
       Chrome 48 on Windows.
