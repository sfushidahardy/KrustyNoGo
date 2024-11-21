## /ProjectCode/AutomatedProcessor
### The data
- The directory *Data* contains the raw data: over 70,000 go game records scraped from [gokifu](gokifu.com). These are in *Smart Game Format* (.sgf) which is not suitable for machine learning. Further, some of the game records may not be suitable anyway (for example if they are not labeled with the game result, or if they ended with close to no moves).
- The directories *Processed_Data_B* and *Processed_Data_W* contains the processed data, separated into two directories depending on which player (B or W) won the game. The processed data consists of the "state of the board" at a random move number between 0 and the total number of moves played in the given game. This provides a large variation of board-states, from early in the game to late in the game. In particular, no two games are repeated twice.

### The programs
- The program *get_process_set.py* carries out the data processing. It does the following:
  - (1) Read each file in Data.
  - (2) (Try to) parse it using pysgf.
  - (3) (Try to) determine the result of the game and the number of moves in the game.
  - (4) (Try to) choose a random move number and determine the board-state at that move as a 19 by 19 array.
- Note that each of the other scripts in the directory are called by *get_process_set.py*.
- The key processin file is *boardstate.py*. An interesting feature of the SGF format is that it doesn't encode the rules of the game it is describing, only the moves of the players. This means converting an SGF into a go board-state requires writing code to interpret the rules and apply them to the moves being played. This is the purpose of *boardstate.py*, and is thus by far the most involved program.

### Outcomes
The results of processing the data were as follows:

- success: 70117
- fail: 3744
   - corrupt file: 1904
   - indeterminate game: 1766
   - movecount error: 2
   - boardstate error: 72

This means 70,117 of the original data were sucessfully converted into a format suitable for ML. Of the failed processes, 1904 failed at the level of parsing the SGF. (This may also be an error on the side of the parser.) Next, 1766 of the parsed game records did not have a labeled winner. The remaining errors are likely due to the SGF files being corrupt, in the sense of not representing a valid game of go, but still parsable.

## Other Directories
The other directories were all for local testing as I incrementally wrote the code.
