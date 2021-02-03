.PHONY: examples clean

# Headers
API_INCLUDES = -Iinclude/api

# Sources
API_SOURCES = $(wildcard src/api/*.c)

CC = gcc
CFLAGS = -g -DLOG_USE_COLOR=1 -Wall

main:
	$(CC) $(CFLAGS) -pthread -lzmq $(API_INCLUDES) ${API_SOURCES} src/leptonic.c -o bin/leptonic
thermalread:
	@mkdir -p bin/main/
	$(CC) $(CFLAGS) $(API_INCLUDES) ${API_SOURCES} main/main.c -o bin/main/main
clean:
	@rm -f *.o
	@rm leptonic
