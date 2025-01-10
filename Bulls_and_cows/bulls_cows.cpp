#include <iostream>
#include <vector>
#include <random>
#include <string>
#include <algorithm>
#include <set>

using namespace std;

struct Result {
    int bulls;
    int cows;
};

class Number {
private:
    string num;
public:
    Number(string num) : num(num) {}

    Number() : num("") {}

    string getNum() {
        return this->num;
    }
};

class Validator {
public:
    static bool isValid(const string& guess, int length) {
        if (guess.size() != length) {
            return false;
        }
        set<char> uniqueDigits;
        for (char c : guess) {
            if (c < '0' || c > '9' || !uniqueDigits.insert(c).second) {
                return false;
            }
        }
        return true;
    }
};

class NumGenerator {
public:
    static string generate(int length) {
        vector<char> digits = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };
        random_device rd;
        mt19937 g(rd());
        shuffle(digits.begin(), digits.end(), g);

        return string(digits.begin(), digits.begin() + length);
    }
};

class Game {
private:
    Number targetNum;
    int targetLength;

public:
    void start(int length) {
        targetLength = length;
        targetNum = Number(NumGenerator::generate(length));
        cout << "Generated number: " << targetNum.getNum() << endl;
    }

    Result check(Number guess) {
        int bulls = 0, cows = 0;
        vector<int> t(10, 0);
        vector<int> g(10, 0);

        for (int i = 0; i < targetLength; i++) {
            if (targetNum.getNum()[i] == guess.getNum()[i]) {
                bulls++;
            } else {
                t[targetNum.getNum()[i] - '0']++;
                g[guess.getNum()[i] - '0']++;
            }
        }

        for (int i = 0; i < 10; i++) {
            cows += min(t[i], g[i]);
        }
        return { bulls, cows };
    }

    string getHint(){}

    int getTargetLength() const {
        return targetLength;
    }

    string getTargetNum(){
        return targetNum.getNum();
    }
};

extern "C" {
    Game* create_game() {
        return new Game();
    }

    void delete_game(Game* game) {
        delete game;
    }

    void initialize_game(Game* game, int length) {
        game->start(length);
    }

    bool validate_guess(const char* guess, int length) {
        string input(guess);
        return Validator::isValid(input, length);
    }

    Result check_guess(Game* game, const char* guess) {
        string input(guess);
        Number g = Number(input);
        return game->check(g);
    }
}
