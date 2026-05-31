#include "sortCPP.h"
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>



std::vector<std::string> SplitLine(const std::string& line) {
    std::vector<std::string> row;
    int a = 0;
    for (int i = 0; i < line.size(); i++) {
        if (line[i] == ',') {
            row.push_back(line.substr(a, i - a));
            a = i + 1;
        }
    }
    row.push_back(line.substr(a));
    return row;
}

void WriteRow(std::ofstream& file, const std::vector<std::string>& row) {
    for (int i = 0; i < row.size(); i++) {
        file << row[i];
        if (i != row.size() - 1) file << ',';
    }
    file << '\n';
}

void InternalSort(std::string filename, int column, bool rev) {
    std::vector<std::vector<std::string>> table;
    std::ifstream fileread(filename);
    std::string line;
    while (std::getline(fileread, line)) {
        table.push_back(std::move(SplitLine(line)));
    }
    fileread.close();
    std::sort(table.begin(), table.end(),
    [column, rev](const std::vector<std::string>& a, const std::vector<std::string>& b) {
        if (column == 3) {
            if (rev) return std::stoi(a[column]) > std::stoi(b[column]);
            else return std::stoi(a[column]) < std::stoi(b[column]);
        } else if (column == 4) {
            if (rev) return std::stof(a[column]) > std::stof(b[column]);
            else return std::stof(a[column]) < std::stof(b[column]);
        } else {
            if (rev) return a[column] > b[column];
            else return a[column] < b[column];
        }
    });
    std::ofstream file(filename);
    for (const auto& row : table) {
        WriteRow(file, row);
    }
    file.close();
}

std::vector<std::string> split(std::string filename) {
    std::ifstream rowFile(filename);
    std::string line;
    std::vector<std::string> first;
    int rows = 0;
    while (std::getline(rowFile, line)) {
        rows++;
    }
    rowFile.close();
    int rowsInFile = rows / 10;
    int row = 0;
    std::ifstream file(filename);
    for (int i = 0; i < 10; i++) {
        std::string f = "file" + std::to_string(i + 1) + ".txt";
        std::ofstream files(f);
        int lenF = rowsInFile;
        while (std::getline(file, line)) {
            std::vector<std::string> str = SplitLine(line);
            if (row == 0) {
                first = str;
            } else {
                WriteRow(files, str);
                if (lenF == 0) break;
                lenF--;
            }
            row++;
        }
        files.close();
    }
    file.close();
    return first;
}

void ExternalSortSTD(std::string filename, int column, bool rev) {
    std::vector<std::string> first = split(filename);
    for (int i = 0; i < 10; i++) {
        std::string f = "file" + std::to_string(i + 1) + ".txt";
        InternalSort(f, column, rev);
    }
    filename.replace(filename.find(".csv"), 4, ".txt");
    std::vector<std::ifstream*> files;
    std::vector<std::vector<std::string>> current;
    for (int i = 0; i < 10; i++) {
        std::string f = "file" + std::to_string(i + 1) + ".txt";
        std::ifstream* file = new std::ifstream(f);
        files.push_back(file);
        std::string line;
        if (std::getline(*file, line)) {
            current.push_back(
            std::move(SplitLine(line)));
        } else {
            current.push_back({});
        }
    }
    std::ofstream out(filename);
    WriteRow(out, first);
    while (true) {
        int best = -1;
        for (int i = 0; i < 10; i++) {
            if (current[i].empty())
                continue;
            if (best == -1) {
                best = i;
            } else {
                bool cond;
                if (column == 3) {
                    if (rev) {
                        cond = std::stoi(current[i][column]) > std::stoi(current[best][column]);
                    } else {
                        cond = std::stoi(current[i][column]) < std::stoi(current[best][column]);
                    }
                } else if (column == 4) {
                    if (rev) {
                        cond = std::stof(current[i][column]) > std::stof(current[best][column]);
                    } else {
                        cond = std::stof(current[i][column]) < std::stof(current[best][column]);
                    }
                } else {
                    if (rev) {
                        cond = current[i][column] > current[best][column];
                    } else {
                        cond = current[i][column] < current[best][column];
                    }
                } 
                if (cond) {
                    best = i;
                }
            }
        }
        if (best == -1) break;
        WriteRow(out, current[best]);
        std::string line;
        if (std::getline(*files[best], line)) {
            current[best] = std::move(SplitLine(line));
        } else {
            current[best].clear();
        }
    }
    out.close();
    for (int i = 0; i < 10; i++) {
        files[i]->close();
        delete files[i];
        std::string f = "file" + std::to_string(i + 1) + ".txt";
        remove(f.c_str());
    }
}

void ExternalSort(const char* filename, int column, bool rev) {
    std::string file(filename);
    ExternalSortSTD(file, column, rev);
}