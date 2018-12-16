#include <iostream>
#include <string>

using std::cin;
using std::cout;
using std::endl;

using std::string;

int getSum(const string input, int offset)
{
    int length = input.length(), sum = 0;
 
    for (int i = 0; i < length; i++) {
        if (input[i] == input[(i + offset) % length]) {
            sum += input[i] - '0';
        }
    }
 
    return sum;
}

int main(void)
{
    string input;

    cin >> input;

    cout << "The solution to the first captcha is: " << getSum(input, 1) << endl;
    cout << "The solution to the second captcha is: " << getSum(input, input.length() / 2) << endl;
}
