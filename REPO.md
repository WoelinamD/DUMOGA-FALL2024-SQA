1. Git hooks\
In workshop 8 Git hooks were introduced as a way to check for changes in C files using cppcheck. In workshop 6 bandit was used to identify security weaknesses in python files so I learned to implement these two things together to check for changes in
python files with git hooks. Any potential weaknesses are placed in weaknesses.csv\
\
2. fuzzing\
Utilized fuzzing with 5 python methods in fuzz.py. Random values were inputted into the methods 10 times for each method and I put the results in fuzzreport.txt. Added a github action to run fuzz.py on push\
\
3. forensics\
added logs to 5 of the functions in git.repo.miner.py in the mining directory\
\
4. continuous integration using github actions\
Added continuous integration just like it was done in the workshop.\
\
Overall, combining all of these methods in one assignment gave me more insight into software quality assurance as a whole.
