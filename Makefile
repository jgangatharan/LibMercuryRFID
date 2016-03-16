OBJS = build/lib/libmercuryrfid.o build/lib/enums.o
CC = gcc
IFLAGS = -Isrc/lib/mercury/api/lib/LTK/LTKC/Library -Isrc/lib/mercury/api/lib/LTK/LTKC/Library/LLRP.org -Isrc/lib/mercury/api
CFLAGS = -fPIC -Wall -Werror -c
LFLAGS = -shared -Wall -Wl,-soname,libmercuryrfid.so.1
LIBS = src/lib/mercury/api/libmercuryapi.so.1 -lpthread  src/lib/mercury/api/lib/LTK/LTKC/Library/libltkc.so.1 src/lib/mercury/api/lib/LTK/LTKC/Library/LLRP.org/libltkctm.so.1

.PHONY: all
all: build/lib/libmercuryrfid.so.1.0

build/lib/libmercuryrfid.so.1.0: $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) -o build/lib/libmercuryrfid.so.1.0  $(IFLAGS) $(LIBS)

build/lib/libmercuryrfid.o: src/lib/libmercuryrfid.c
	$(CC) $(CFLAGS) $(IFLAGS) src/lib/libmercuryrfid.c -o build/lib/libmercuryrfid.o

build/lib/enums.o: src/lib/enums.c
	$(CC) $(CFLAGS) $(IFLAGS) src/lib/enums.c -o build/lib/enums.o

.PHONY: clean
clean:
	@rm -rf build
	@rm -rf *~

