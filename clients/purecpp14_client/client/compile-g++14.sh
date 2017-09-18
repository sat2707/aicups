files=""

for i in *.cpp
do
    files="$files $i"
done

for i in csimplesocket/*.cpp
do
    files="$files $i"
done

g++ -std=c++14 -static -fno-optimize-sibling-calls -fno-strict-aliasing -D_LINUX -lm -s -x c++ -O2 -Wall -Wno-unknown-pragmas -o MyStrategy.out $files 2>compilation.log
