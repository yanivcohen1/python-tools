#include <stdio.h>
#include <string.h>

// Example C function that processes JSON
const char* process_json(const char* input_json) {
    static char output_json[256];
    // For demonstration, just copy the input JSON to output
    strcpy(output_json, input_json);
    return output_json;
}
