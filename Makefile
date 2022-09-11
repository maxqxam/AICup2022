all:
	#Options:
	#	DEBUG_NO_BRAINER


DEBUG_NO_BRAINER:
	python3 $(ANALYZOR) $(SERVER) 10 $(CLIENT_DEBUG) $(CLIENT_NO_BRAINER)

DEBUG_RANDOM_NAVIGATION:
	python3 $(ANALYZOR) $(SERVER) 10 $(CLIENT_DEBUG) $(CLIENT_RANDOM_NAVIGATION)

DEBUG_PATROL_PLUS_APPROACH:
	python3 $(ANALYZOR) $(SERVER) 10 $(CLIENT_DEBUG) $(CLIENT_PATROL_PLUS_APPROACH)




ANALYZOR=./analyzer.py
SERVER=./src/server.py

CLIENT_DEBUG=./Clients/Python/main.py
CLIENT_NO_BRAINER=./AIBank/0_no_brainer/main.py
CLIENT_RANDOM_NAVIGATION=./AIBank/1_random_navigation/main.py
CLIENT_PATROL_PLUS_APPROACH=./AIBank/2_patrol_plus_approach/main.py
