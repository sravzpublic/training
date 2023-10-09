CXX=g++
CXXFLAGS=-pthread -Wall -Wno-switch -Wno-unused-function -std=c++11 #-shared # -fPIC
ROOT_DIR=.
BASE_SRC_DIR=${ROOT_DIR}
INCLUDES=-I${ROOT_DIR}
TARGET=libTwsSocketClient.so

# https://stackoverflow.com/questions/75051115/tws-api-linux-segmentation-fault-bid64-to-string
$(TARGET):
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(BASE_SRC_DIR)/*.cpp /usr/lib/x86_64-linux-gnu/libbidgcc000.a -o$(TARGET)

clean:
	rm -f $(TARGET) *.o

