#include <iostream>
#include <string>
#include <sstream>
#include <vector>

using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::istringstream;
using std::vector;

vector<int> lineToVector(const string line)
{
    istringstream is(line);
    int i;
    vector<int> v;

    while (is >> i)
        v.push_back(i);

    return v;
}

int getChecksum(const vector<int> line)
{
    int min = 10000, max = 0;

    for (int i : line) {
        if (i < min) min = i;
        if (i > max) max = i;
    }

    return max - min;
}

int getResult(const vector<int> line)
{
    int i, j, size = line.size();

    for (i = 0; i < size; i++) {
        for (j = i + 1; j < size; j++) {
            if (line[i] >=  line[j] && line[i] % line[j] == 0) {
                return line[i] / line[j];
            }
            if (line[i] < line[j] && line[j] % line[i] == 0) {
                return line[j] / line[i];
            }
        }
    }

    return 0;
}

int main(void)
{
    string line;
    int sumOfChecksums = 0, sumOfResults = 0;
    vector<int> v;

    while (getline(cin, line)) {
        v = lineToVector(line);
        sumOfChecksums += getChecksum(v);
        sumOfResults += getResult(v);
    }

    cout << "The sum of the checksums is: " << sumOfChecksums << endl;
    cout << "The sum of the results is: " << sumOfResults << endl;

    return 0;
}
