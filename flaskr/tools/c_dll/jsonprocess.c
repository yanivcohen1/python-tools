#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Example C function that processes JSON
const char* process_json(const char* input_json) {
    const char* my_str = "my cmd_";

    // Calculate the size needed for the concatenated string
    size_t size = strlen(input_json) + strlen(my_str) + 1;

    // Allocate memory for the concatenated string
    char* utf8_str = (char*)malloc(size);

    if (utf8_str == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    // Concatenate the strings
    // Concatenate the parts into the new UTF-8 encoded string
    strcpy(utf8_str, my_str);
    strcat(utf8_str, input_json);

    // Print the concatenated string
    printf("c print: %s\n", utf8_str);

    // Free the allocated memory
    // free(utf8_str);

    return utf8_str;
}

// Example C function that processes JSON
const char* process_file(const char* input_json) {
    // Calculate the size of the original JSON string
    size_t size = strlen(input_json) + 1; // +1 for the null terminator

    // Allocate memory for the copy
    char* json_copy = (char*)malloc(size);

    if (json_copy == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    // Copy the original JSON string into the allocated memory
    strcpy(json_copy, input_json);

    // Free the allocated memory
    // free(utf8_str);

    return input_json;
}
