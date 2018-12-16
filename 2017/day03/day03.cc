#include <iostream>
#include <cmath>

using std::cin;
using std::cout;
using std::endl;

int getMaxForTier(int n)
{
    n = 2 * n + 1;
    return n * n;
}

int getTier(int n)
{
    return ceil(.5 * (sqrt(n) - 1));
}

int getDistanceFromOrigin(int n)
{
    int tier = getTier(n);
    n -= getMaxForTier(tier - 1);
    return abs((n % (tier * 2)) - tier) + tier;
}

int main(void)
{
    int n;

    cin >> n;
    cout << getDistanceFromOrigin(n) << endl;

    return 0;
}
