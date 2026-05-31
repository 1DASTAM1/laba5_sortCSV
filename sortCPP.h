#pragma once

extern "C" {
    __declspec(dllexport) void ExternalSort(const char* filename, int column, bool rev);
}