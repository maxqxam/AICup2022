all:
	#Options:
	#	DEBUG_NO_BRAINER


DEBUG_0:
	python3 $(ANALYZOR) $(SERVER) 10 $(CLIENT_DEBUG) $(CLIENT_0)

DEBUG_1:
	python3 $(ANALYZOR) $(SERVER) 10 $(CLIENT_DEBUG) $(CLIENT_1)

DEBUG_2:
	python3 $(ANALYZOR) $(SERVER) 10 $(CLIENT_DEBUG) $(CLIENT_2)

DEBUG_3:
	python3 $(ANALYZOR) $(SERVER) 100 $(CLIENT_DEBUG) $(CLIENT_3)

DEBUG_4:
	python3 $(ANALYZOR) $(SERVER) 100 $(CLIENT_DEBUG) $(CLIENT_4)


ANALYZOR=./analyzer.py
SERVER=./src/server.py

CLIENT_DEBUG=./Clients/Python/main.py
CLIENT_0=./AIBank/0_no_brainer/main.py
CLIENT_1=./AIBank/1_random_navigation/main.py
CLIENT_2=./AIBank/2_patrol_plus_approach/main.py
CLIENT_3=./AIBank/3_better_ppa/main.py
CLIENT_4=./AIBank/4_retriever_1/main.py

